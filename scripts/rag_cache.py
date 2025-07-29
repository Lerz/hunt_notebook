# rag_cache.py

import hashlib
import shelve
from rag_engine import get_context

CACHE_PATH = "../cache/rag_context_cache.db"


def _make_key(query: str, top_k: int) -> str:
    # Clé explicite + hash pour éviter conflits ou doublons
    raw = f"q:{query}|k:{top_k}"
    return hashlib.sha256(raw.encode()).hexdigest()


def get_cached_context(query: str, top_k: int = 3) -> str:
    """Renvoie un contexte depuis le cache ou l'index FAISS si besoin."""
    key = _make_key(query, top_k)
    with shelve.open(CACHE_PATH) as db:
        if key in db:
            return db[key]
        ctx = get_context(query, top_k=top_k)
        db[key] = ctx
        return ctx


def cache_info():
    """Affiche un aperçu des clés présentes dans le cache."""
    with shelve.open(CACHE_PATH) as db:
        print(f"{len(db)} entrées en cache.")
        for k in list(db.keys())[:5]:
            print(f"- {k[:8]}... : {db[k][:80].replace('\n', ' ')}...")


def clear_cache(confirm=False):
    """Purge manuelle du cache."""
    if not confirm:
        print("Utilise clear_cache(confirm=True) pour confirmer.")
        return
    with shelve.open(CACHE_PATH) as db:
        db.clear()
        print("Cache vidé.")