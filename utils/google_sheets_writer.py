# utils/google_sheets_writer.py

from __future__ import annotations

from typing import Dict, Any, List, Optional
from pathlib import Path
import json
import os

import gspread
from google.oauth2.service_account import Credentials

# Streamlit est optionnel: le module doit pouvoir tourner en local sans Streamlit
try:
    import streamlit as st
except Exception:  # pragma: no cover
    st = None  # type: ignore


###############################################
# CONFIG (sécurisée)
###############################################

# Fallback local (facultatif)
SERVICE_ACCOUNT_FILE = Path("gcp_service_account.json")

# Scopes: Drive est parfois trop large. Si tu fais seulement Sheets, ce scope suffit.
# Si tu as des opérations Drive (copie, permissions, etc.), garde drive.
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    # "https://www.googleapis.com/auth/drive",  # à activer seulement si nécessaire
]


###############################################
# UTILITAIRES
###############################################

def _coerce_cell_value(v: Any) -> str:
    """Convertit proprement les valeurs du JSON Excel en valeurs cellule."""
    if v is None:
        return ""
    if isinstance(v, list):
        return " • ".join(str(x) for x in v if x is not None and str(x).strip() != "")
    if isinstance(v, dict):
        try:
            return json.dumps(v, ensure_ascii=False)
        except Exception:
            return str(v)
    return str(v)


def _get_secret(name: str, default: Optional[str] = None) -> Optional[str]:
    """
    Récupère un secret depuis:
    1) st.secrets (si Streamlit disponible)
    2) variables d'environnement
    """
    if st is not None:
        try:
            if name in st.secrets:
                return str(st.secrets[name])
        except Exception:
            pass
    return os.getenv(name, default)


def _get_service_account_info() -> Optional[Dict[str, Any]]:
    """
    Retourne les infos du compte de service depuis:
    - st.secrets["GCP_SERVICE_ACCOUNT_JSON"] (string JSON)
    - ou st.secrets["gcp_service_account"] (dict TOML)
    - ou variables env
    - ou fichier local (fallback)
    """
    # 1) Streamlit secrets: JSON string
    sa_json = _get_secret("GCP_SERVICE_ACCOUNT_JSON")
    if sa_json:
        try:
            return json.loads(sa_json)
        except json.JSONDecodeError as e:
            raise RuntimeError("GCP_SERVICE_ACCOUNT_JSON n'est pas un JSON valide.") from e

    # 2) Streamlit secrets: dict TOML (ex: [gcp_service_account] ...)
    if st is not None:
        try:
            if "gcp_service_account" in st.secrets:
                # st.secrets section -> mapping
                return dict(st.secrets["gcp_service_account"])
        except Exception:
            pass

    # 3) Fallback local: fichier JSON
    if SERVICE_ACCOUNT_FILE.exists():
        try:
            return json.loads(SERVICE_ACCOUNT_FILE.read_text(encoding="utf-8"))
        except Exception as e:
            raise RuntimeError(f"Impossible de lire {SERVICE_ACCOUNT_FILE}.") from e

    return None


###############################################
# INITIALISATION CLIENT (cachable)
###############################################

def _build_gspread_client() -> gspread.Client:
    sa_info = _get_service_account_info()
    if not sa_info:
        raise FileNotFoundError(
            "Aucune config GCP trouvée. "
            "Ajoute GCP_SERVICE_ACCOUNT_JSON dans Streamlit Secrets "
            "ou fournis un fichier gcp_service_account.json en local."
        )

    creds = Credentials.from_service_account_info(sa_info, scopes=SCOPES)
    return gspread.authorize(creds)


# Cache Streamlit (évite de ré-auth à chaque interaction)
if st is not None:
    @st.cache_resource
    def get_gspread_client() -> gspread.Client:
        return _build_gspread_client()
else:
    def get_gspread_client() -> gspread.Client:
        return _build_gspread_client()


###############################################
# FONCTION PRINCIPALE
###############################################

def append_json_to_google_sheet(
    json_excel: Dict[str, Any],
    spreadsheet_id: Optional[str] = None,
    worksheet_name: Optional[str] = None,
) -> int:
    """
    Ajoute json_excel comme nouvelle ligne dans un Google Sheets.
    La ligne 1 du Google Sheets doit contenir les en-têtes (noms de colonnes).
    Retourne le numéro de ligne insérée (1-based).
    """

    spreadsheet_id = spreadsheet_id or _get_secret("SPREADSHEET_ID")
    worksheet_name = worksheet_name or _get_secret("WORKSHEET_NAME", "Formations")

    if not spreadsheet_id:
        raise RuntimeError("SPREADSHEET_ID manquant (Streamlit Secrets ou env var).")

    client = get_gspread_client()
    sh = client.open_by_key(spreadsheet_id)

    try:
        ws = sh.worksheet(worksheet_name)
    except gspread.WorksheetNotFound as e:
        raise RuntimeError(
            f"Feuille '{worksheet_name}' introuvable dans le Google Sheets."
        ) from e

    headers: List[str] = ws.row_values(1)
    if not headers:
        raise RuntimeError(
            "La première ligne du Google Sheets est vide. "
            "Elle doit contenir les noms de colonnes."
        )

    row_values: List[str] = []
    for h in headers:
        val = json_excel.get(h.strip())
        row_values.append(_coerce_cell_value(val))

    ws.append_row(row_values, value_input_option="USER_ENTERED")

    # Méthode simple: récupérer le nombre total de lignes après append
    inserted_row_idx = len(ws.get_all_values())
    return inserted_row_idx
