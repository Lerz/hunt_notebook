
"""extract_docs.py

Script de prétraitement pour transformer divers formats de documents en `.txt` exploitables par le moteur RAG.
Formats supportés : PDF, HTML (avec titres structurés), YAML, Markdown, TXT, Python, epub, etc.
Sortie : un fichier `.txt` par document dans ./processed_docs/

Pré-requis :
- pdfplumber
- beautifulsoup4
- pyyaml
- html5lib
- lxml
- ebooklib
"""

import os
import hashlib
from pathlib import Path
import pdfplumber
import yaml
from ebooklib import epub
from ebooklib.epub import EpubHtml
from bs4 import BeautifulSoup

# Détermine le répertoire racine du projet (parent du dossier scripts)
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent

INPUT_DIRS = [
    PROJECT_ROOT / "docs", 
    PROJECT_ROOT / "cheatbooks", 
    PROJECT_ROOT / "scripts", 
    PROJECT_ROOT / "knowledge_base"
]
OUTPUT_DIR = PROJECT_ROOT / "processed_docs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

TEXT_EXT = [".txt", ".md", ".py"]
SPECIAL_EXT = [".pdf", ".html", ".htm", ".yaml", ".yml"]

def clean_filename(path):
    return f"{hashlib.sha256(str(path).encode('utf-8')).hexdigest()[:32]}.txt"

def extract_structured_html(html_text):
    soup = BeautifulSoup(html_text, "html.parser")
    parts = []

    for tag in soup.find_all(["h1", "h2", "h3", "p", "li"]):
        if tag.name == "h1":
            parts.append(f"# {tag.get_text(strip=True)}")
        elif tag.name == "h2":
            parts.append(f"## {tag.get_text(strip=True)}")
        elif tag.name == "h3":
            parts.append(f"### {tag.get_text(strip=True)}")
        else:
            txt = tag.get_text(strip=True)
            if txt:
                parts.append(txt)

    return "\n".join(parts)

# Statistiques
total_files = 0
processed_files = 0
skipped_files = 0
error_files = 0

print(f"Démarrage du traitement...")
print(f"Répertoire de sortie: {OUTPUT_DIR}")
print(f"Dossiers d'entrée:")
for input_dir in INPUT_DIRS:
    if input_dir.exists():
        print(f"{input_dir}")
    else:
        print(f"{input_dir} (n'existe pas)")

print("\n" + "="*50)

for folder in INPUT_DIRS:
    if not folder.exists():
        print(f"Dossier ignoré (inexistant): {folder}")
        continue

    print(f"\nTraitement du dossier: {folder}")
    folder_files = 0
    for root, _, files in os.walk(folder):
        for f in files:
            total_files += 1
            folder_files += 1
            ext = Path(f).suffix.lower()
            full_path = Path(root) / f
            out_path = OUTPUT_DIR / clean_filename(str(full_path))

            # Vérification si le fichier existe
            if not full_path.exists():
                print(f"Fichier introuvable: {full_path}")
                error_files += 1
                continue

            # Vérification de l'extension
            if ext not in TEXT_EXT + SPECIAL_EXT + [".epub"]:
                print(f"Extension non supportée ({ext}): {f}")
                skipped_files += 1
                continue

            try:
                text = ""
                print(f"Traitement: {f} ({ext})")

                if ext in TEXT_EXT:
                    text = Path(full_path).read_text(encoding="utf-8", errors="ignore")
                elif ext == ".pdf":
                    with pdfplumber.open(full_path) as pdf:
                        text = "\n".join(page.extract_text() or "" for page in pdf.pages)
                elif ext in [".html", ".htm"]:
                    html = Path(full_path).read_text(encoding="utf-8", errors="ignore")
                    text = extract_structured_html(html)
                elif ext in [".yaml", ".yml"]:
                    data = yaml.safe_load(Path(full_path).read_text(encoding="utf-8"))
                    text = str(data)
                elif ext == ".epub":
                    book = epub.read_epub(str(full_path))
                    parts = []
                    for item in book.get_items():
                        if isinstance(item, EpubHtml):
                            html = item.get_content().decode("utf-8")
                            parts.append(extract_structured_html(html))
                    text = "\n".join(parts)
                else:
                    skipped_files += 1
                    continue

                # Vérification que le texte extrait n'est pas vide
                if not text.strip():
                    print(f"Texte vide extrait de: {f}")
                    skipped_files += 1
                    continue

                out_path.write_text(text.strip(), encoding="utf-8")
                processed_files += 1
                print(f"{full_path.name} → {out_path.name} ({len(text)} caractères)")
            except Exception as e:
                error_files += 1
                print(f"❌ Erreur sur {f} : {e}")

    print(f"Dossier {folder.name}: {folder_files} fichiers trouvés")

print("\n" + "="*50)
print("RÉSUMÉ FINAL:")
print(f"Total de fichiers examinés: {total_files}")
print(f"Fichiers traités avec succès: {processed_files}")
print(f"Fichiers ignorés: {skipped_files}")
print(f"❌ Fichiers en erreur: {error_files}")
print(f"Fichiers de sortie dans: {OUTPUT_DIR}")

if processed_files > 0:
    print("\nTraitement terminé avec succès!")
else:
    print("\nAucun fichier n'a été traité. Vérifiez les chemins et les dépendances.")
