# packages/ — Dépendances Python pré-téléchargées pour environnement airgapped

Ce répertoire contient l’ensemble des **packages Python nécessaires** au fonctionnement du projet, stockés localement sous forme de fichiers `.whl` ou d’archives `.tar.gz`.

Il est destiné à être utilisé avec l’option `--find-links` de `pip`, afin d’installer les dépendances dans un environnement **sans accès Internet**.

---

## Contenu attendu

| Type de fichier    | Description                                 |
| ------------------ | ------------------------------------------- |
| `.whl`             | Fichiers wheel des packages Python          |
| `.tar.gz`          | Archives source pour installation manuelle  |-

---

## Installation typique (offline)

```bash
python -m venv a_hunt_venv_py310
source a_hunt_venv_py310/bin/activate  # Ou Scripts\Activate.ps1 sous Windows

pip install --no-index --find-links=packages/ -r requirements.txt
```

---

## Mise à jour des packages (depuis machine connectée)

Sur une machine avec accès internet :

```bash
mkdir packages
pip download -r requirements.txt -d packages/
```

Puis transférer le dossier `packages/` vers l’environnement cible.

---

## Bonnes pratiques

* Conserver ce répertoire synchronisé avec `requirements.txt`
* Éviter d’y ajouter manuellement des fichiers non liés à `pip`
* Supprimer les anciennes versions si nécessaire pour alléger la taille