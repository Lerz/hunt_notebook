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
from pathlib import Path
import pdfplumber
import yaml
from ebooklib import epub
from bs4 import BeautifulSoup

INPUT_DIRS = ["../docs", "../cheatbooks", "../scripts", "../knowledge_base"]
OUTPUT_DIR = Path("./processed_docs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

TEXT_EXT = [".txt", ".md", ".py"]
SPECIAL_EXT = [".pdf", ".html", ".htm", ".yaml", ".yml"]

def clean_filename(path):
    return path.replace("/", "_").replace("\\", "_").replace(":", "_")

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

for folder in INPUT_DIRS:
    for root, _, files in os.walk(folder):
        for f in files:
            ext = Path(f).suffix.lower()
            full_path = Path(root) / f
            out_path = OUTPUT_DIR / f"{clean_filename(str(full_path))}.txt"

            try:
                text = ""
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
                        if item.get_type() == epub.ITEM_DOCUMENT:
                            html = item.get_content().decode("utf-8")
                            parts.append(extract_structured_html(html))
                    text = "\n".join(parts)
                else:
                    continue

                out_path.write_text(text.strip(), encoding="utf-8")
                print(f"✅ {full_path} → {out_path}")
            except Exception as e:
                print(f"❌ Erreur sur {f} : {e}")
