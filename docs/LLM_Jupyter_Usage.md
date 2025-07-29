# 📘 Documentation – Utilisation d’un LLM local avec JupyterLab (Airgapped)

Ce guide explique comment utiliser efficacement un **LLM 3B** (Gemma, Mistral…) en local avec `llama-cpp-python` dans un environnement de hunt offline sous **JupyterLab**.

---

## 🎯 Objectif

- Interroger un modèle local (format `.gguf`) depuis Jupyter
- Ne charger le modèle **qu’une seule fois** pour optimiser les performances
- Faciliter l’analyse automatique des logs réseau enrichis

---

## 📁 Organisation des fichiers

```
/models/
    gemma-2b-it.Q4_K_M.gguf
/datasets/
    stormshield_logs.csv
/output/
    stormshield_enriched.csv
/llm_wrapper.py
/prompt_utils.py
/llm_hunt_notebook.ipynb
```

---

## ⚙️ Prérequis

Librairies Python :

```
llama-cpp-python
pandas
jupyterlab
```

Installe-les via `pip` :

```bash
pip install llama-cpp-python pandas jupyterlab
```

---

## 🧠 Chargement du modèle

Dans une cellule Jupyter :

```python
from llm_wrapper import HuntLLM

# Crée une instance globale du modèle (chargé une seule fois en RAM)
llm = HuntLLM(model_path="./models/gemma-2b-it.Q4_K_M.gguf", threads=8)
print("✅ Modèle chargé.")
```

---

## 📊 Formater les logs pour le prompt

```python
import pandas as pd
from prompt_utils import format_logs_for_prompt

df = pd.read_csv("./output/stormshield_enriched.csv")
context = format_logs_for_prompt(df)
```

---

## 💬 Interroger le modèle

```python
question = "Quels signes d’exfiltration observes-tu dans ces logs réseau ?"
response = llm.ask(question, context=context, max_tokens=300)
print(response)
```

Tu peux appeler `llm.ask(...)` autant de fois que nécessaire **sans relancer l’initialisation**.

---

## 💡 Exemples de questions utiles

```text
- Décris les comportements réseau suspects dans cet extrait
- Y a-t-il du DNS tunneling ?
- Quelles IP semblent suspectes ?
- Quels domaines sont potentiellement des dropzones ?
- Propose une règle SPL de détection
```

---

## 🧠 Boucle interactive (optionnelle)

```python
while True:
    q = input("Ta question > ")
    print(llm.ask(q, context=context))
```

---

## ✅ Résumé

| Étape                   | Action                                        |
|-------------------------|-----------------------------------------------|
| Charger le modèle       | `llm = HuntLLM(...)`                          |
| Créer un contexte       | `context = format_logs_for_prompt(df)`       |
| Poser une question      | `llm.ask("...", context=context)`            |
| Réutilisable ?          | Oui, tant que le kernel n’est pas redémarré |

---

