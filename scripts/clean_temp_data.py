import os
import time
from pathlib import Path

DATA_DIR = Path("data")
MAX_AGE_DAYS = 7           # Supprime les fichiers modifiés il y a plus de X jours
MAX_SIZE_MB = 100          # Supprime les fichiers plus gros que X Mo

max_age_seconds = MAX_AGE_DAYS * 86400
max_size_bytes = MAX_SIZE_MB * 1024 * 1024
now = time.time()

def clean_data_folder():
    deleted_files = []

    for file in DATA_DIR.glob("*"):
        if not file.is_file():
            continue

        file_age = now - file.stat().st_mtime
        file_size = file.stat().st_size

        if file_age > max_age_seconds or file_size > max_size_bytes:
            print(f"Suppression : {file.name} (age: {int(file_age)}s, size: {file_size // 1024} Ko)")
            file.unlink()
            deleted_files.append(file.name)

    if not deleted_files:
        print("Aucun fichier à supprimer.")
    else:
        print(f"\n {len(deleted_files)} fichier(s) supprimé(s).")

if __name__ == "__main__":
    if DATA_DIR.exists():
        clean_data_folder()
    else:
        print(f"Dossier introuvable : {DATA_DIR.resolve()}")
