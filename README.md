📊 CESU-EXTRACT - Extracteur de rapports qualité

🩺 Présentation du projet

Ce projet vise à automatiser l’analyse de rapports qualité au format PDF, en particulier dans des contextes institutionnels ou organisationnels, afin de transformer des documents complexes et hétérogènes en données structurées, fiables et exploitables.

L’application prend en charge l’ensemble du cycle de traitement :

- ingestion des rapports PDF,

- extraction intelligente des informations pertinentes,

- structuration normalisée des données,

- consolidation automatique dans des supports bureautiques standards.

Le projet est conçu comme un système modulaire et industrialisable, et non comme une simple application de démonstration.

🎯 Objectifs fonctionnels

- Réduire drastiquement le temps de traitement manuel des rapports

- Fiabiliser l’extraction et l’analyse des données qualité

- Centraliser les résultats dans des formats exploitables (Excel / Sheets)

- Garantir la cohérence des indicateurs dans le temps

- Proposer une solution compatible avec des environnements institutionnels
  

🚀 Fonctionnalités principales (vue fonctionnelle)

1️⃣ Ingestion et lecture des rapports PDF

- Import de rapports qualité au format PDF

- Gestion des documents textuels et scannés

- Extraction automatique du contenu pertinent

2️⃣ Structuration intelligente des données

- Analyse du contenu via des modèles de langage

- Transformation en données structurées normalisées

- Harmonisation des formats (notes, pourcentages, verbatims)

3️⃣ Calculs et synthèses automatiques

- Calcul d’indicateurs clés (satisfaction, impact, répartition)

- Nettoyage et regroupement des réponses textuelles

- Génération de synthèses exploitables

4️⃣ Export et consolidation

- Injection automatisée dans :

- un modèle Excel structuré

- un Google Sheets sécurisé

- Alignement strict avec des schémas de données prédéfinis

- Aucun retraitement manuel requis

🧩 Cas d’usage

- Analyse qualité de formations ou dispositifs

- Consolidation multi-périodes ou multi-sessions

- Préparation d’indicateurs de pilotage

- Appui à la prise de décision

- Réduction des erreurs liées à la ressaisie manuelle

🏗️ Architecture générale

- Le projet repose sur une architecture en pipeline, découpée en étapes indépendantes :

- Extraction du contenu PDF

- Analyse et structuration des données

- Validation via des schémas de données stricts

- Transformation métier (calculs, synthèses)

- Injection vers les supports d’exploitation

Chaque étape est isolée afin de garantir :

- maintenabilité,

- testabilité,

- évolutivité,

- robustesse en production.
  

🧠 Partie technique (niveau maîtrisé, non sensible)

🔹 Technologies clés

- Python (cœur applicatif)

- Streamlit (interface utilisateur)

- Pydantic (contrats et validation de données)

- LLM (OpenAI API) pour l’analyse sémantique et les synthèses

- Extraction PDF + OCR (documents textuels ou scannés)

- Excel (openpyxl) pour la consolidation locale

- Google Sheets API pour l’exploitation cloud

- Google Cloud Platform pour l’authentification sécurisée

🔹 Gestion des données

- Utilisation de schémas stricts pour éviter toute dérive des données

- Normalisation des formats numériques et textuels

- Séparation claire entre données intermédiaires et données finales

- Traçabilité complète du pipeline de transformation

Cette approche garantit des résultats cohérents, reproductibles et exploitables à grande échelle.

🔹 Sécurité et bonnes pratiques

- Accès aux ressources cloud via comptes de service

- Permissions limitées au périmètre strictement nécessaire

- Aucune clé ou information sensible versionnée

- Séparation des environnements (développement / démonstration / production)

- Aucun accès utilisateur direct aux ressources critiques

Les choix techniques sont pensés pour répondre aux contraintes d’environnements professionnels et institutionnels.

🔹 Déploiement

- Version locale pour développement et validation

- Version cloud (Streamlit) pour démonstration contrôlée

- Désactivation des écritures locales en environnement cloud

- Architecture compatible avec une montée en charge progressive

⭐ Points forts du projet

- Automatisation complète de bout en bout

- Architecture modulaire et industrialisable

- Forte fiabilité des données

- Sécurité intégrée dès la conception

- Compatible avec des environnements institutionnels

- Facilement extensible à d’autres formats ou cas d’usage

👨‍💻 À propos

Ce projet illustre une approche orientée :

- Ingénierie des données

- Automatisation intelligente

- Qualité et gouvernance des données

- Industrialisation des processus

Il a été conçu comme un système robuste, destiné à transformer des processus manuels complexes en chaînes de traitement fiables, reproductibles et scalables.

✍️ Auteur

Développé par Roméo Botuli

Ingénieur Data & Intelligence Artificielle

Projet réalisé dans un contexte institutionnel (CESU 83)



