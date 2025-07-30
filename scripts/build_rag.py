# build_rag_index.py

"""
Reconstruit et persiste l'index vectoriel FAISS à partir des fichiers `./processed_docs/*.txt`
- Utilise le moteur RAG optimisé avec BGE + chunking glissant
- Ne reprocess que les fichiers modifiés (via hash SHA256)
- Sauvegarde FAISS + sources + hashes dans ./cache/
- Écrit les sources et documents sous `./cache/rag_sources.json`
"""

import os
import json
import numpy as np
from pathlib import Path
import faiss
from sentence_transformers import SentenceTransformer
import hashlib
import argparse


SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
DOCS_PATH = PROJECT_ROOT / "processed_docs"
MODEL_PATH = PROJECT_ROOT / "models"
CACHE_PATH = PROJECT_ROOT / "cache"
CACHE_PATH.mkdir(exist_ok=True)
INDEX_FILE = CACHE_PATH / "rag_index.faiss"
SOURCE_FILE = CACHE_PATH / "rag_sources.json"
HASH_FILE = CACHE_PATH / "hashes.json"


model = SentenceTransformer(MODEL_PATH / "BAAI/bge-small-en-v1.5")


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

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

if HASH_FILE.exists():
    with open(HASH_FILE, "r") as f:
        old_hashes = json.load(f)
else:
    old_hashes = {}

# Argument --force
parser = argparse.ArgumentParser()
parser.add_argument("--force", action="store_true", help="Reprocess tous les fichiers")
args = parser.parse_args()


documents = []
sources = []
new_hashes = {}

for f in DOCS_PATH.glob("*.txt"):
    file_hash = sha256_file(f)
    new_hashes[str(f)] = file_hash
    if args.force or old_hashes.get(str(f)) != file_hash:
        print(f"Reprocessing: {f.name}")
        try:
            text = f.read_text(encoding="utf-8")
            for chunk, label in sliding_chunks(text, f):
                documents.append(chunk)
                sources.append(label)
        except Exception as e:
            print(f"🔥Erreur lecture {f} : {e}")
    else:
        print(f"Inchangé: {f.name} (skip)")

if not documents:
    print("Aucun document modifié. Index conservé.")
    exit(0)

# === Embedding & indexation ===
print(f"Encodage de {len(documents)} chunks...")
doc_vectors = model.encode(documents, show_progress_bar=True, batch_size=16)
doc_vectors_np = np.array(doc_vectors)

print("Construction de l'index FAISS...")
index = faiss.IndexFlatL2(doc_vectors_np.shape[1])
index.add(doc_vectors_np)

# === Sauvegarde ===
faiss.write_index(index, str(INDEX_FILE))
print(f"Index FAISS sauvegardé : {INDEX_FILE}")

with open(SOURCE_FILE, "w", encoding="utf-8") as f:
    json.dump({"sources": sources, "documents": documents}, f, indent=2, ensure_ascii=False)
print(f"Sources sauvegardées : {SOURCE_FILE}")

with open(HASH_FILE, "w") as f:
    json.dump(new_hashes, f, indent=2)
print(f"Hashes mis à jour : {HASH_FILE}")
