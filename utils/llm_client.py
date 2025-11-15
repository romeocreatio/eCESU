# utils/llm_client.py
import json
from pathlib import Path
import os

from openai import OpenAI


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
    start = text.find("{")
    end = text.rfind("}")
    if start >= 0 and end > start:
        try:
            return json.loads(text[start : end + 1])
        except Exception:
            pass
    raise ValueError("Réponse LLM non JSON.")


def _get_openai_client_and_model():
    """
    Stratégie de récupération des credentials :
    1) Variables d'environnement (.env ou secrets cloud exposés en env) :
       - OPENAI_API_KEY
       - OPENAI_MODEL
    2) Secrets Streamlit "plats" (cloud ou local):
       - st.secrets["OPENAI_API_KEY"]
       - st.secrets["OPENAI_MODEL"]
    3) Secrets Streamlit sectionnés (local) :
       - st.secrets["openai"]["API_KEY"]
       - st.secrets["openai"]["MODEL"]
    """

    api_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("OPENAI_MODEL")

    # Essayer les secrets Streamlit s'ils existent
    try:
        import streamlit as st  # import local pour que ce module reste utilisable hors Streamlit

        # Forme "plate" (cloud)
        if not api_key and "OPENAI_API_KEY" in st.secrets:
            api_key = st.secrets["OPENAI_API_KEY"]
        if not model and "OPENAI_MODEL" in st.secrets:
            model = st.secrets["OPENAI_MODEL"]

        # Forme sectionnée (local: [openai])
        if "openai" in st.secrets:
            sec = st.secrets["openai"]
            if not api_key:
                api_key = sec.get("API_KEY", api_key)
            if not model:
                model = sec.get("MODEL", model)
    except Exception:
        # Si Streamlit n'est pas dispo (scripts unitaires), on ignore
        pass

    if not api_key:
        raise RuntimeError(
            "Aucune clé API OpenAI trouvée.\n"
            "Configure OPENAI_API_KEY dans ton .env ou dans les secrets Streamlit Cloud."
        )

    if not model:
        model = "gpt-4.1-mini"

    client = OpenAI(api_key=api_key)
    return client, model


def call_llm_extract_json(prompt_master: str, full_text: str, meta: dict) -> dict:
    """
    Appelle un LLM avec response_format JSON.
    Utilise :
      - OPENAI_API_KEY / OPENAI_MODEL (env)
      - ou les secrets Streamlit (plats ou sectionnés).
    """
    client, model = _get_openai_client_and_model()

    system_msg = (
        "Tu es un extracteur documentaire strict. "
        "Tu renvoies uniquement du JSON conforme au schéma demandé."
    )

    user_content = prompt_master.replace("{{PDF_TEXT}}", full_text).replace(
        "{{PDF_METADATA}}", json.dumps(meta, ensure_ascii=False)
    )

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
