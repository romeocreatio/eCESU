# utils/llm_client.py
import json
from pathlib import Path

from openai import OpenAI
import streamlit as st


def load_prompt(path: str) -> str:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Prompt introuvable: {path}")
    return p.read_text(encoding="utf-8")


def _coerce_json(text: str) -> dict:
    # Essaie de parser un JSON propre ; sinon extrait le premier bloc {...}
    try:
        return json.loads(text)
    except Exception:
        pass
    # fallback simple
    start = text.find("{")
    end = text.rfind("}")
    if start >= 0 and end > start:
        try:
            return json.loads(text[start:end+1])
        except Exception:
            pass
    raise ValueError("Réponse LLM non JSON.")


def _get_openai_client_and_model() -> tuple[OpenAI, str]:
    """
    Récupère le client OpenAI et le modèle à partir des secrets Streamlit.

    secrets.toml attendu :

    [openai]
    API_KEY = "ta_cle_openai_ici"
    MODEL = "gpt-4.1-mini"  # par exemple
    """
    try:
        openai_section = st.secrets["openai"]
    except Exception as e:
        raise RuntimeError(
            "Section [openai] manquante dans les secrets Streamlit. "
            "Vérifie ton .streamlit/secrets.toml ou les secrets Streamlit Cloud."
        ) from e

    api_key = openai_section.get("API_KEY")
    if not api_key:
        raise RuntimeError(
            "Clé API OpenAI manquante dans les secrets (openai.API_KEY)."
        )

    # Modèle optionnel dans les secrets, avec une valeur par défaut
    model = openai_section.get("MODEL", "gpt-4.1-mini")

    client = OpenAI(api_key=api_key)
    return client, model


def call_llm_extract_json(prompt_master: str, full_text: str, meta: dict) -> dict:
    """
    Appelle un LLM avec response_format JSON.
    Utilise les secrets Streamlit : [openai].API_KEY et [openai].MODEL.
    """
    client, model = _get_openai_client_and_model()

    # Construit le prompt final
    system_msg = (
        "Tu es un extracteur documentaire strict. "
        "Tu renvoies uniquement du JSON conforme au schéma demandé."
    )

    user_content = (
        prompt_master.replace("{{PDF_TEXT}}", full_text)
        .replace("{{PDF_METADATA}}", json.dumps(meta, ensure_ascii=False))
    )

    # Appel
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_content},
        ],
        response_format={"type": "json_object"},
        temperature=0,
    )

    raw = resp.choices[0].message.content
    data = _coerce_json(raw)

    # Nettoyages simples (décimales FR, %)
    def _norm_numbers(obj):
        if isinstance(obj, dict):
            return {k: _norm_numbers(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [_norm_numbers(x) for x in obj]
        if isinstance(obj, str):
            s = obj.replace(",", ".").strip()
            return s
        return obj

    return _norm_numbers(data)
