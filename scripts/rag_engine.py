"""
rag_engine.py

Version optimisée pour usage RAG sur CPU :
- Utilise BGE-Small pour de meilleurs embeddings sémantiques
- Chunking par glissement pour capturer plus de contexte
- Option de reranking local via un cross-encoder léger
- Cache persisté (shelve) pour accélérer les appels répétés
- Index FAISS et sources persistés
- Ne reprocess que les fichiers modifiés (via hash SHA256)
"""

import os
from pathlib import Path
import numpy as np
import re
import hashlib
import shelve
import json

from sentence_transformers import SentenceTransformer, CrossEncoder
import faiss

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
MODEL_DIR = PROJECT_ROOT / "models"

EMBED_MODEL = MODEL_DIR / "BAAI/bge-small-en-v1.5"
DOCS_PATH = PROJECT_ROOT / "processed_docs"
CACHE_PATH = PROJECT_ROOT / "cache"
CACHE_PATH.mkdir(exist_ok=True)
INDEX_FILE = CACHE_PATH / "rag_index.faiss"
SOURCE_FILE = CACHE_PATH / "rag_sources.json"
CACHE_SHELVE = CACHE_PATH / "rag_context_cache"

# === Chargement du modèle d'embedding ===
model = SentenceTransformer(EMBED_MODEL)

# === Chargement du reranker (optionnel) ===
try:
    reranker = CrossEncoder(MODEL_DIR / "cross-encoder/ms-marco-MiniLM-L-6-v2")
except Exception:
    reranker = None

# === Chargement des sources et de l'index ===
if INDEX_FILE.exists() and SOURCE_FILE.exists():
    index = faiss.read_index(str(INDEX_FILE))
    with open(SOURCE_FILE, "r", encoding="utf-8") as f:
        meta = json.load(f)
        documents = meta["documents"]
        sources = meta["sources"]
else:
    raise FileNotFoundError("Index ou sources manquantes. Lancez `build_rag_index.py` d'abord.")

# === Recherche de contexte (non cachee) ===
def _get_context_base(query: str, top_k=5, rerank=True) -> str:
    query_vec = model.encode([query])
    _, indices = index.search(np.array(query_vec), top_k * 3 if rerank and reranker else top_k)

    candidates = [(documents[i], sources[i]) for i in indices[0]]

    if reranker:
        scores = reranker.predict([(query, doc) for doc, _ in candidates])
        sorted_candidates = [x for _, x in sorted(zip(scores, candidates), reverse=True)]
    else:
        sorted_candidates = candidates

    result = []
    for doc, src in sorted_candidates[:top_k]:
        result.append(f"# Source: {src}\n{doc.strip()}\n")

    return "\n---\n".join(result)

# === Cache contextuel persisté ===
def get_context(query: str, top_k=5, rerank=True) -> str:
    key = hashlib.sha256(f"q:{query}|k:{top_k}|r:{rerank}".encode()).hexdigest()
    with shelve.open(str(CACHE_SHELVE)) as db:
        if key in db:
            return db[key]
        ctx = _get_context_base(query, top_k=top_k, rerank=rerank)
        db[key] = ctx
        return ctx
