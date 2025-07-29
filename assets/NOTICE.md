# assets/

Ce répertoire contient des **ressources statiques** utilisées lors des analyses ou enrichissements, mais qui **ne sont pas générées automatiquement** : fichiers IOC, règles de détection, fichiers de configuration ou références partagées.

Il agit comme un répertoire **de support manuel** pour les sessions de hunting ou les playbooks.

---

## Contenu attendu

| Type de fichier         | Description                                                      |
| ----------------------- | ---------------------------------------------------------------- |
| `iocs.csv` / `iocs.txt` | Liste d'IOCs connus (IPs, domaines, hachés, etc.)                |
| `sigma_custom.yml`      | Règles Sigma spécifiques ou adaptées                             |
| `hunt_config.yaml`      | Paramètres de session (fenêtre de temps, sources, filtres, etc.) |
| `threat_groups.json`    | Référentiel MITRE ou groupe d’APT pour enrichissement            |
| `allowlist_domains.txt` | Liste blanche pour filtrer les faux positifs                     |

---

## Utilisation typique

* Enrichir ou filtrer les résultats d’une recherche
* Aligner le hunting avec un scénario spécifique (exfiltration, APT, etc.)
* Définir des **règles personnalisées** pour les notebooks ou outils RAG
* Fournir un référentiel **réutilisable entre sessions**

---

## Bonnes pratiques

* Versionner les IOCs et règles avec une date (`iocs_2025-07-29.txt`)
* Documenter tout format non trivial (README ou entête de fichier)
* Éviter de stocker des secrets ou credentials ici
* Ne pas confondre avec `/vendors` (règles Sigma sources)

---

## Intégration dans le pipeline

Certains notebooks ou scripts du dossier `scripts/` consomment ce répertoire :

* Chargement automatique des IOCs pour pivot
* Filtres personnalisés appliqués aux datasets
* Import de règles Sigma dans l’environnement d’analyse