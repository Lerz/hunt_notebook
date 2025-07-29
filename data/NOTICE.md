# data/

Ce répertoire contient les **données générées automatiquement** par les scripts, notebooks ou étapes d'enrichissement, mais qui ne sont **ni versionnées**, ni considérées comme finalisées.

Il s'agit en général de fichiers :

* temporaires,
* bruts (non nettoyés),
* extraits d’une source mais pas encore enrichis,
* ou issus d’un traitement en cours (cache, batch, résultat partiel…).

---

## Contenu typique

| Exemple de fichier         | Description                                   |
| -------------------------- | --------------------------------------------- |
| `extracted_logs_raw.json`  | Export brut depuis Splunk ou une autre source |
| `dns_unfiltered.csv`       | Dump complet non filtré d’événements DNS      |
| `raw_sysmon_logs.parquet`  | Données Sysmon avant parsing / enrichissement |
| `temp_processing_file.tmp` | Fichier temporaire en cours de traitement     |

---

## Rôle du dossier

* Permet de **séparer clairement** les données en transit ou à traiter
* Évite de polluer `datasets/` avec des fichiers incomplets
* Sert souvent de **buffer intermédiaire** pour la chaîne d’analyse

---

## Bonnes pratiques

* Ne pas stocker ici de résultats finaux ou enrichis (utiliser `datasets/`)
* Purger régulièrement les fichiers obsolètes ou trop volumineux
* Utiliser des noms explicites pour faciliter la reprise d’analyse (`source_type_date.raw`, etc.)

---

## Nettoyage automatique

Un script de ménage `clean_temp_data.py` est fourni pour :

* Supprimer les fichiers > N jours
* Identifier les fichiers inutilisés depuis X temps
* Vider les caches optionnels