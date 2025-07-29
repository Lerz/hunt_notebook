# knowledge\_base/ — Base documentaire pour enrichissement contextuel

Ce répertoire contient les **documents techniques et sources de référence** utilisés par le moteur RAG (Retrieval-Augmented Generation) pour fournir un contexte lors des interrogations du LLM.

Les fichiers placés ici seront analysés, découpés en blocs, vectorisés, puis indexés pour permettre une recherche contextuelle rapide et pertinente dans les notebooks d’analyse.

---

## Contenu attendu

Les fichiers doivent être **en format texte interprétable**. Les formats supportés incluent :

| Type de fichier  | Description                       |
| ---------------- | --------------------------------- |
| `.pdf`           | Documents PDF (ex. : whitepapers) |
| `.epub`          | Documentation                     |
| `.html` / `.htm` | Pages web sauvegardées            |
| `.txt`           | Notes, extraits simples           |
| `.md`            | Documentation Markdown            |
| `.yaml` / `.yml` | Fichiers de règles ou de config   |

---

## Utilisation typique

Quelques exemples de contenu à stocker ici :

* Documentation Splunk (offline ou PDF)
* Règles Sigma documentées
* Cheat sheets de détection ou d’analyse
* Guides internes de threat hunting
* Notes techniques d’expert ou rapports internes
* Documents réglementaires (PDIS, ISO, etc.)

---

## Indexation automatique

Les fichiers seront automatiquement traités lors de l’exécution des scripts RAG du projet :

```bash
scripts/
├── extract_docs.py       # Extraction + découpage
├── rag_engine.py         # Vectorisation et interrogation
```