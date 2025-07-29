# 📦 offline_enrichment – Librairie d’enrichissement réseau offline (airgapped)

## 🔍 Objectif

Permet d’enrichir des jeux de données réseau (ex. : export Splunk) avec :

- Type d’IP : `Interne`, `Externe`, `Invalide`
- Service standard du port destination (ex : 22 → SSH)
- ASN et nom d'organisation (si base MaxMind ASN dispo)
- Appartenance au **Majestic Million** (réputation du domaine)

---

## 📁 Dépendances

```txt
ipaddress
geoip2            # (optionnel, pour GeoLite2 ASN)
pandas
```

---

## 📂 Structure attendue

- `./data/GeoLite2-ASN.mmdb` *(optionnel)* : base ASN MaxMind
- `./lookups/majestic_million.csv` *(optionnel)* : fichier CSV contenant les domaines connus
- Un DataFrame avec au moins `src_ip`, `dest_port` et `url_domain`

---

## ✅ Utilisation

```python
import pandas as pd
from offline_enrichment import enrich_dataframe

df = pd.read_csv("stormshield_logs.csv")
df = enrich_dataframe(df, ip_col="src_ip", port_col="dest_port", domain_col="url_domain")
df[["src_ip", "ip_type", "port_type", "asn_desc", "in_majestic"]].head()
```

---

## ✍️ Résultat attendu

| src_ip       | ip_type | port_type | asn_desc              | in_majestic |
|--------------|---------|-----------|------------------------|-------------|
| 172.22.0.1   | Interne | HTTPS     | Orange S.A. (AS3215)   | Oui         |
| 8.8.8.8      | Externe | DNS       | Google LLC (AS15169)   | Oui         |
| 193.56.88.88 | Externe | HTTP      | OVH SAS (AS16276)      | Non         |

---

## 📝 Notes

- Si `geoip2` ou le fichier `.mmdb` n’est pas dispo, la colonne `asn_desc` retournera `"GeoIP non disponible"`.
- Si le fichier `majestic_million.csv` est absent, la colonne `in_majestic` retournera `"Inconnu"`.

---

## 📘 Exemple de ligne dans `majestic_million.csv`

```csv
GlobalRank,Domain
1,google.com
2,youtube.com
...
```

Téléchargeable depuis : https://majestic.com/reports/majestic-million
