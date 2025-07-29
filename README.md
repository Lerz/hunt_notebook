# `hunt-lab` — Environnement d’analyse de logs pour le threat hunting et la détection de fuites

Ce projet fournit un environnement complet, autonome et fonctionnel pour l’investigation de logs en environnement sensible (airgapped). Il permet de traiter efficacement des exports Splunk (ou équivalents), d’enrichir les données, d’exécuter des détections avancées et d'interagir avec un moteur de raisonnement local basé sur modèle.

## Fonctionnalités principales

* Import, transformation et requêtage de jeux de données Splunk ou CSV
* Recherche efficace via **DuckDB** et `pandas` pour l’analyse tabulaire
* Outils d’enrichissement local (GeoIP, TLD, IP internes/externes)
* Visualisation interactive avec `matplotlib`, `seaborn` ou `plotly`
* Détection basée sur :

  * **Notebooks d’investigation personnalisés**
  * **Règles Sigma** intégrées (converties localement)
* Interrogation via un **LLM local CPU** avec support contextuel (RAG)
* Génération automatisée de rapports PDF
* Entièrement utilisable sans connexion internet

---

## Organisation du projet

```bash
hunt/
├── assets/               # Assets utils à la session de hunt (iocs, sigma...)
├── cheatbooks/           # Cheatsheets d’investigation thématiques
├── data/                 # Données temporaires ou intermédiaires
├── datasets/             # Jeux de données (exports Splunk, logs enrichis)
├── docs/                 # Documentation du projet
├── knowledge_base/       # Corpus RAG (fichiers exploitables par LLM)
├── models/               # Modèles LLM
├── notebooks/            # Notebooks Jupyter d’investigation
├── output/               # Résultats, visualisations, rapports
├── packages/             # Librairies externes embarquées (offline)
├── scripts/              # Scripts Python pour enrichissement, LLM, RAG
├── vendors/              # Modules/Datasets tiers (ex : Sigma, parsing YAML, rules)
├── LICENSE
├── README.md
└── requirements.txt
```

---

## Installation hors ligne

Cet environnement est conçu pour être **entièrement fonctionnel sans connexion internet**. Toutes les dépendances nécessaires doivent être préalablement téléchargées depuis une machine connectée, puis transférées.
Pour les dépendances non-libres ou volumineuses pour ce dépôt, se référer au TODO.md dans le repertoire.

---

### 1. **Se placer à la racine du projet**

```bash
cd hunt-lab/
```

---
### 2. **Créer un environnement virtuel**

> Python 3.10 recommandé

```bash
python -m venv a_hunt_venv_py310
```

> Sous Windows :

```ps
a_hunt_venv_py310\Scripts\Activate.ps1
```

> Sous Linux/macOS :

```bash
source a_hunt_venv_py310/bin/activate
```

---

### 3. **Installer les dépendances (offline)**

Les dépendances doivent avoir été pré-téléchargées sous forme de `wheels` ou via un `pip download` depuis un environnement connecté.
```bash
pip download -r requirements.txt -d ./packages
```
Sur l'environnement airgapped :
```bash
pip install --no-index --find-links=packages/ -r requirements.txt
```

Cela installe tous les modules nécessaires à l’environnement Jupyter, l’enrichissement, le moteur RAG, le support du LLM local, les visualisations et la détection.

---

### 4. **Démarrer l’interface JupyterLab**

```bash
jupyter lab
```

Un serveur local s’ouvrira sur `http://localhost:8888`.
Naviguez ensuite dans le dossier `notebooks/` pour lancer vos analyses.

---

### 5. **(Optionnel) Regénérer le cache pour les modèles LLM**

Si vous utilisez un modèle `.gguf` avec `ctransformers`, le premier appel le compilera (quelques secondes), puis sera mis en cache localement dans `~/.cache/`.

---
