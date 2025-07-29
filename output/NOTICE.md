# output/ — Résultats générés lors des analyses et sessions de hunting

Ce répertoire contient les **fichiers produits automatiquement** lors de l'investigations : exports, rapports, visualisations, listings d’alertes ou d’IOCs générés.

Il sert de **zone de sortie par défaut** pour tous les notebooks, scripts ou outils intégrés au projet.

Il permet de structurer les annexes qui seront ajoutées au rapport final.
---

## Contenu typique

| Exemple de fichier            | Description                                        |
| ----------------------------- | -------------------------------------------------- |
| `hunt_summary_2024-07-29.pdf` | Rapport PDF généré depuis un notebook              |
| `exfil_candidates.csv`        | Liste des IP ou domaines suspects détectés         |
| `ioc_extracted.json`          | IOCs extraits depuis les logs                      |
| `volumes_by_ip.png`           | Graphique généré avec `matplotlib`                 |
| `enriched_results.parquet`    | Résultats enrichis à exploiter dans un autre outil |

---

## Génération

Les fichiers de ce dossier sont produits par :

* des **notebooks Jupyter** (visualisation, synthèse, scoring, pivot…)
* des **scripts Python** (détection, enrichissement, parsing)
* le **moteur de reporting** (`weasyprint`, `jinja2`) intégré au pipeline

---

## Bonnes pratiques

* Toujours nommer les fichiers de sortie avec un **suffixe explicite** (`_report`, `_ioc`, `_viz`, `_full`, etc.)
* Ajouter la **date de génération** au nom pour suivre l’historique
* Nettoyer régulièrement les sorties obsolètes
* Éviter de placer manuellement des fichiers dans ce dossier

---

## Utilisation dans le projet

Ce dossier est souvent lu par d'autres outils :

* Envois de rapports par mail ou dans une SIEM
* Réutilisation dans un second notebook
* Comparaison automatique entre sessions de hunting