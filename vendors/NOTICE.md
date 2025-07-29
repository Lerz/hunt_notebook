# vendors/ — Dépendances embarquées hors ligne

Ce dossier contient les **dépendances critiques** nécessaires à l'exécution des fonctions de détection, d'enrichissement et d'analyse du projet, **sans accès à Internet**.
Les fichiers et projets listés ci-dessous doivent être téléchargés manuellement depuis une machine connectée, puis copiés dans ce répertoire.

---

## 1. Base ASN/IP

**Fichier :** `GeoLite2-ASN.mmdb`
**Source :** [MaxMind GeoLite2 ASN](https://dev.maxmind.com/geoip/geolite2-free-geolocation-data)
**Utilisation :**
Permet d'enrichir les adresses IP avec leur ASN (Autonomous System Number), utile pour identifier les fournisseurs réseau et repérer des comportements suspects.

*Licence requise : création d’un compte gratuit MaxMind pour générer un token et télécharger le fichier.*

---

## 2. Liste des sites populaires

**Fichier :** `majestic_million.csv`
**Source :** [Majestic Million - Majestic.com](https://majestic.com/reports/majestic-million)
**Utilisation :**
Permet de vérifier si un domaine contacté figure parmi les sites web les plus populaires, utile pour filtrer ou hiérarchiser les destinations réseau.

---

## 3. Règles Sigma (détection comportementale)

**Dossier :** `sigma/`
**Source :** [SigmaHQ - GitHub](https://github.com/SigmaHQ/sigma)
**Utilisation :**
Contient les règles Sigma (`.yml`) utilisées pour la détection de comportements suspects dans les logs. Ces règles sont ensuite converties (localement) en expressions exploitables par pandas/DuckDB ou transformées pour correspondre à des requêtes Splunk.

*Il est recommandé de cloner le dépôt complet pour bénéficier des convertisseurs, outils et règles à jour.*

```bash
git clone https://github.com/SigmaHQ/sigma vendors/sigma
```

---

## Résumé du contenu attendu dans `vendors/`

```
vendors/
├── GeoLite2-ASN.mmdb       # Base IP ↔ ASN
├── majestic_million.csv    # Liste des 1M de domaines populaires
└── sigma/                  # Règles Sigma + convertisseurs
```