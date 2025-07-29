# datasets/

Ce répertoire contient les **données structurées (logs, exports, résultats de recherches)** utilisées comme base d’analyse dans les notebooks du projet.

Les fichiers sont typiquement au format `.csv`, mais d’autres formats tabulaires (`.parquet`, `.tsv`, `.json`) peuvent être utilisés selon les outils ou les cas d’usage.

---

## Contenu typique

| Nom du fichier             | Description                                           |
| -------------------------- | ----------------------------------------------------- |
| `stormshield_enriched.csv` | Logs réseau enrichis issus de firewall Stormshield    |
| `hunt_results.csv`         | Résultats d’une recherche Splunk exportée             |
| `notable_events.json`      | Événements notables extraits de Splunk ES             |
| `leak_candidates.parquet`  | Données suspectes issues d’un playbook d’exfiltration |

---

## Génération des fichiers

Les datasets peuvent provenir de :

* Recherches Splunk exportées au format `.csv`
* Extraction depuis l’API REST Splunk via `scripts/splunk_tools.py`
* Agrégation et enrichissement via des notebooks
* Résultats de détection (ex. : Sigma, règles internes)
* Données partagées manuellement (fichiers déposés localement)

---

## Bonnes pratiques

* Conserver un nom explicite (ex. : `source_enriched.csv`)
* Utiliser UTF-8 et un séparateur standard (`,` ou `;`)

---

## Rafraîchissement / nettoyage

Pensez à purger les fichiers temporaires ou obsolètes pour éviter la confusion lors des analyses.
