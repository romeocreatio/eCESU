📄 CESU 83 · Extracteur Automatisé de Rapports Qualité (Version Streamlit)

🩺 Présentation du projet

Ce projet permet au CESU 83 d’extraire automatiquement les données des rapports qualité Digiforma, puis de les transformer en format JSON v2.1, JSON Excel, et enfin d’injecter les données dans un modèle Excel consolidé.

L’application propose une interface Streamlit, utilisable :

En local (mode développement)

Sur Streamlit Cloud (mode démo pour la responsable CESU)

L’objectif est de fournir une version simple, stable et prête à l’emploi afin de centraliser et d’analyser les feedbacks des formations CESU.

🚀 Fonctionnalités principales

**1. Extraction PDF (Phase 1)**

Upload d’un PDF Digiforma (Rapport Qualité)

Lecture intelligente via :

pdfplumber (texte direct)

OCR automatique en fallback (si disponible)

Appel d’un LLM (OpenAI) avec un prompt structuré

Génération d’un JSON v2.1 propre, conforme au schéma OutputPayload

**2. Transformation en JSON Excel (Phase 2)**

Nettoyage et harmonisation complète des données

Synthèses médicalisées ou professionnelles générées par l’IA

Calculs automatiques : pourcentages, notes, impact, satisfaction, etc.

Production d’un JSON Excel prêt à être injecté

**3. Génération Excel consolidé (Phase 3)**

Injection du JSON Excel dans un template Excel

Version cloud-friendly :

Aucune écriture sur disque

Génération d’un fichier Excel en mémoire

Téléchargement direct du fichier .xlsx final

🧱 Architecture du projet

cesu-rapport-qualite-demo/
│
├── streamlit_app.py        → Interface Streamlit principale
├── requirements.txt        → Dépendances projet
├── .streamlit/             → Fichiers secrets (ignorés par Git)
│    └── secrets.toml
│
├── utils/                  → Modules internes
│    ├── pdf_reader.py
│    ├── llm_client.py
│    ├── convert_v2_to_excel.py
│    ├── excel_writer.py
│    └── schema.py
│
├── templates/
│    └── maquette.xlsx      → Modèle Excel consolidé
│
├── prompts/
│    └── prompt_reference.txt
│
├── assets/
│    └── logo_cesu83.jpeg
│
├── json_v2/                → JSON v2.1 générés (local)
├── json_excel/             → JSON Excel générés (local)
└── README.md

**🔐 Gestion des clés API (OpenAI)**

Local (mode dev)

Créer un .env à la racine :

OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxx
OPENAI_MODEL=gpt-4.1-mini

Streamlit Cloud (mode démo)

Dans Settings → Secrets, ajouter :

OPENAI_API_KEY = "sk-xxxxxxxxxxxxxxxx"
OPENAI_MODEL   = "gpt-4.1-mini"
USERNAME       = "xxx"
PASSWORD       = "xxx"

🔑 Sécurisation de l’application

L’accès à l’app est protégé par une authentification simple :

Login : configurable dans secrets.toml

Mot de passe : configurable dans secrets.toml

Le code lit les credentials via :

[auth]
USERNAME = "xxx"
PASSWORD = "xxx"

📦 Installation (mode local)
1. Cloner le repo
git clone https://github.com/<votre-user>/cesu-rapport-qualite-demo.git
cd cesu-rapport-qualite-demo

2. Créer un environnement virtuel
python -m venv .venv
.\.venv\Scripts\activate

3. Installer les dépendances
pip install -r requirements.txt

4. Lancer l’application
streamlit run streamlit_app.py

📤 Déploiement Streamlit Cloud

Aller sur : https://share.streamlit.io

Connecter votre GitHub

Sélectionner le repo

Entrypoint :

streamlit_app.py


Ajouter les secrets (OpenAI + login)

Cliquer sur Deploy 🚀

🛡️ .gitignore (sécurisé)

Le projet ignore uniquement :

.streamlit/ → contient les clés API locales

.venv/ → venv local

__pycache__/ → fichiers Python compilés

fichiers systèmes / logs

Tous les fichiers nécessaires au déploiement sont versionnés.

🧪 Tests réalisés

Extraction PDF → OK

Transformation JSON → OK

Génération Excel → OK

Authentification → OK

Compatibilité Streamlit Cloud → OK

👨‍💻 Auteur

Développé par Roméo Botuli, Ingénieur Data & IA.

Projet réalisé pour le CESU 83.