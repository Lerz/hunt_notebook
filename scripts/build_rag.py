# build_rag_index.py

"""
Reconstruit et persiste l'index vectoriel FAISS à partir des fichiers `./processed_docs/*.txt`
- Utilise le moteur RAG optimisé avec BGE + chunking glissant
- Écrit l'index sur disque sous `./cache/rag_index.faiss`
- Écrit les sources et documents sous `./cache/rag_sources.json`
"""

import os
import json
import numpy as np
from pathlib import Path
import faiss
from sentence_transformers import SentenceTransformer

SCRIPT_DIR = Path(__file__).parent

PROJECT_ROOT = SCRIPT_DIR.parent
DOCS_PATH = PROJECT_ROOT / "processed_docs"
CACHE_PATH = PROJECT_ROOT / "cache"

CACHE_PATH.mkdir(exist_ok=True)
INDEX_FILE = CACHE_PATH / "rag_index.faiss"
SOURCE_FILE = CACHE_PATH / "rag_sources.json"

# === Modèle d'embedding optimisé CPU ===
model = SentenceTransformer("BAAI/bge-small-en-v1.5")

# === Chunking glissant ===
CHUNK_SIZE = 20
CHUNK_OVERLAP = 5

def sliding_chunks(text, path):
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    chunks = []
    for i in range(0, len(lines), CHUNK_SIZE - CHUNK_OVERLAP):
        chunk = "\n".join(lines[i:i + CHUNK_SIZE])
        label = f"{path.name} [lignes {i}–{i + CHUNK_SIZE}]"
        chunks.append((chunk, label))
    return chunks

# === Lecture & découpage ===
documents = []
sources = []

for f in DOCS_PATH.glob("*.txt"):
    try:
        text = f.read_text(encoding="utf-8")
        for chunk, label in sliding_chunks(text, f):
            documents.append(chunk)
            sources.append(label)
    except Exception as e:
        print(f"❌ Erreur lecture {f} : {e}")

# === Embedding & indexation ===
print(f"🔢 Encodage de {len(documents)} chunks...")
doc_vectors = model.encode(documents, show_progress_bar=True, batch_size=16)
doc_vectors_np = np.array(doc_vectors)

print("🧠 Construction de l'index FAISS...")
index = faiss.IndexFlatL2(doc_vectors_np.shape[1])
index.add(doc_vectors_np)

# === Sauvegarde ===
faiss.write_index(index, str(INDEX_FILE))
print(f"✅ Index FAISS sauvegardé : {INDEX_FILE}")

with open(SOURCE_FILE, "w", encoding="utf-8") as f:
    json.dump({"sources": sources, "documents": documents}, f, indent=2, ensure_ascii=False)
print(f"📚 Sources sauvegardées : {SOURCE_FILE}")
