# Documentation – Intégration RAG local pour environnement de Hunt (Airgapped)

Ce guide explique comment utiliser un moteur **RAG (Retrieval-Augmented Generation)** local pour enrichir le LLM avec des documents Splunk, règles Sigma, scripts, etc.

---

## Structure du projet

```
/docs/                ← documentation brute (.pdf, .md, .html, .yaml…)
/scripts/             ← tes scripts Python ou techniques utiles
/knowledge_base/      ← autre contenu technique ou sources personnelles
/processed_docs/      ← texte plat généré automatiquement (utilisé par RAG)
/scripts/rag_engine.py        ← moteur RAG basé sur FAISS
/scripts/extract_docs.py      ← script pour transformer et préparer les documents
```

---

## Étapes d’utilisation

### 1. Préparer les documents

Place tous tes fichiers dans :
- `./docs/` (Markdown du projet hunt)
- `./scripts/` (fichiers `.py`)
- `./knowledge_base/` (fichiers YAML, PDF, Markdown, HTML… autres contenus)

---

### 2. Transformer les documents

```bash
python extract_docs.py
```

Ce script génère un `.txt` pour chaque document lisible et le place dans `./processed_docs/`.

---

### 3. Charger le moteur RAG

Dans ton notebook :

```python
from rag_engine import get_context
ctx = get_context("comment écrire une macro Splunk")
```

---

### 4. Appeler ton LLM local

```python
from llm_wrapper import HuntLLM
llm = HuntLLM(model_path="../models/gemma-2b-it.Q4_K_M.gguf")
llm.ask("Explique le champ sourcetype", context=ctx)
```

---

## Exemple de questions utiles

```text
- Comment fonctionne le SPL `stats count by` ?
- Quels ports sont utilisés pour du DNS tunneling ?
- Explique la différence entre macro et lookup dans Splunk
- Donne une règle Sigma pour détecter exfiltration HTTP
```

---

## Résumé du flux RAG

| Étape                 | Outil                     | Dossier concerné           |
|-----------------------|---------------------------|-----------------------------|
| Dépôt documentaire    | `/docs`, `/scripts`, etc. | Fichiers source             |
| Extraction texte      | `extract_docs.py`         | Génère `./processed_docs/`  |
| Recherche contextuelle| `rag_engine.py`           | Via `get_context(query)`    |
| Appel LLM             | `llm.ask(..., context=…)` | Interprétation augmentée    |

---
