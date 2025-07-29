# 📊 Utiliser un Dataset Splunk dans un RAG Tabulaire

Ce guide explique comment **exploiter un gros fichier CSV (>1 Go)** exporté depuis Splunk pour l’interroger efficacement avec un LLM, sans surcharge mémoire.

---

## 🧠 Objectif

- Ne **pas vectoriser ligne par ligne** (inefficace)
- Regrouper les données de logs par entité significative (ex : `src_ip`)
- Générer des **résumés sémantiques par groupe**
- Créer une base vectorielle exploitable via FAISS
- Interroger en langage naturel le dataset via un moteur RAG

---

## 🧰 Prérequis

Installe les librairies dans ton environnement airgapped (déjà couvert dans `requirements.txt`) :
```txt
duckdb
pandas
sentence-transformers
faiss-cpu
```

---

## 🔧 Étapes

### 1. Charger le fichier CSV en SQL via DuckDB

```python
import duckdb

df = duckdb.query("""
    SELECT src_ip,
           COUNT(*) AS nb_connexions,
           SUM(bytes_out) AS total_out,
           SUM(bytes_in) AS total_in,
           GROUP_CONCAT(DISTINCT url_domain, ', ') AS domaines
    FROM 'logs_splunk.csv'
    GROUP BY src_ip
""").to_df()
```

---

### 2. Générer les résumés sémantiques

```python
def create_summary(row):
    return f"""IP: {row['src_ip']}
- Connexions: {row['nb_connexions']}
- Sortant: {round(row['total_out']/1024/1024, 2)} Mo
- Entrant: {round(row['total_in']/1024/1024, 2)} Mo
- Domaines: {row['domaines']}
"""

texts = df.apply(create_summary, axis=1).tolist()
```

---

### 3. Vectoriser les résumés

```python
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")
vectors = model.encode(texts, show_progress_bar=True)
index = faiss.IndexFlatL2(vectors.shape[1])
index.add(np.array(vectors))
```

---

### 4. Interroger le corpus via LLM + FAISS

```python
def search_context(query, top_k=3):
    q_vec = model.encode([query])
    _, idxs = index.search(np.array(q_vec), top_k)
    return [texts[i] for i in idxs[0]]

print("\n---\n".join(search_context("Qui a exfiltré plus de 500 Mo ?")))
```

---

## ✅ Avantages

- Évite de surcharger la RAM
- Approche RAG exploitable même avec >1M logs
- Facilement intégrable dans un notebook ou LLM pipeline

---

## 📁 Exemple de pipeline complet disponible dans `notebooks/hunt_splunk_rag.ipynb`
