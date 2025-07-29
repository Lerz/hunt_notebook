"""
rag_engine_optimized.py

Version optimisée pour usage RAG sur CPU :
- Utilise BGE-Small pour de meilleurs embeddings sémantiques
- Chunking par glissement pour capturer plus de contexte
- Option de reranking local via un cross-encoder léger
- Cache persisté (shelve) pour accélérer les appels répétés
"""

import os
from pathlib import Path
import numpy as np
import re
import hashlib
import shelve

from sentence_transformers import SentenceTransformer, CrossEncoder
import faiss

EMBED_MODEL = "../models/BAAI/bge-small-en-v1.5"  # ~100M params, CPU-friendly
model = SentenceTransformer(EMBED_MODEL)

# Optionnel : reranker cross-encoder
try:
    reranker = CrossEncoder("../models/cross-encoder/ms-marco-MiniLM-L-6-v2")  # ~60MB, très rapide sur CPU
except Exception:
    reranker = None

DOCS_PATH = Path("../processed_docs")
CACHE_PATH = Path("../cache/rag_context_cache")
CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)

documents = []
sources = []

CHUNK_SIZE = 20  # nombre de lignes par chunk
CHUNK_OVERLAP = 5

def sliding_chunks(text, path):
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    chunks = []
    for i in range(0, len(lines), CHUNK_SIZE - CHUNK_OVERLAP):
        chunk = "\n".join(lines[i:i + CHUNK_SIZE])
        label = f"{path.name} [lignes {i}–{i + CHUNK_SIZE}]"
        chunks.append((chunk, label))
    return chunks

# Lecture + chunking
for f in DOCS_PATH.glob("*.txt"):
    try:
        text = f.read_text(encoding="utf-8")
        for chunk, label in sliding_chunks(text, f):
            documents.append(chunk)
            sources.append(label)
    except Exception as e:
        print(f"❌ Erreur lecture {f} : {e}")

# Encodage vectoriel
doc_vectors = model.encode(documents, show_progress_bar=True, batch_size=16)
doc_vectors_np = np.array(doc_vectors)

# Index FAISS
index = faiss.IndexFlatL2(doc_vectors_np.shape[1])
index.add(doc_vectors_np)

# Recherche contextuelle (non cachee)
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
    with shelve.open(str(CACHE_PATH)) as db:
        if key in db:
            return db[key]
        ctx = _get_context_base(query, top_k=top_k, rerank=rerank)
        db[key] = ctx
        return ctx