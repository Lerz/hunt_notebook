
# 🧪 DuckDB Cookbook – Hunt réseau & exfiltration (Splunk exports)

Ce fichier est une collection de requêtes SQL optimisées pour analyser un export CSV Splunk (`stormshield_logs.csv`) avec **DuckDB**.

---

## 📁 Préparation (dans Python ou CLI)

```python
import duckdb

# Requête sur fichier CSV directement
duckdb.query("""
    SELECT * FROM 'datasets/stormshield_logs.csv'
""").df()
```

---

## 🔎 1. Top IP par volume total

```sql
SELECT src_ip,
       SUM(bytes_out + bytes_in) / 1024 / 1024 / 1024 AS total_Go,
       COUNT(*) AS connexions
FROM 'datasets/stormshield_logs.csv'
GROUP BY src_ip
ORDER BY total_Go DESC
LIMIT 20;
```

---

## 🌍 2. IP interne vs externe (simplifiée)

```sql
SELECT src_ip,
       SUM(bytes_out + bytes_in)/1024/1024 AS total_Mo,
       CASE
         WHEN src_ip LIKE '10.%' OR src_ip LIKE '192.168.%' OR src_ip BETWEEN '172.16.0.0' AND '172.31.255.255' THEN 'Interne'
         ELSE 'Externe'
       END AS ip_type
FROM 'datasets/stormshield_logs.csv'
GROUP BY src_ip, ip_type
ORDER BY total_Mo DESC;
```

---

## 🌐 3. Services cloud les plus utilisés (domaines suspects)

```sql
SELECT url_domain,
       COUNT(*) AS connexions,
       SUM(bytes_out + bytes_in)/1024/1024 AS total_Mo
FROM 'datasets/stormshield_logs.csv'
WHERE url_domain IN ('dropbox.com', 'mega.nz', 'wetransfer.com', 'file.io', 'gofile.io', 'anonfiles.com')
GROUP BY url_domain
ORDER BY total_Mo DESC;
```

---

## 🕒 4. Volume horaire (par heure UTC)

```sql
SELECT DATE_TRUNC('hour', _time) AS heure,
       SUM(bytes_out + bytes_in)/1024/1024 AS total_Mo
FROM 'datasets/stormshield_logs.csv'
GROUP BY heure
ORDER BY heure ASC;
```

---

## 🔁 5. Connexions vers plusieurs destinations uniques

```sql
SELECT src_ip,
       COUNT(DISTINCT dest_ip) AS nb_destinations,
       COUNT(*) AS total_connexions
FROM 'datasets/stormshield_logs.csv'
GROUP BY src_ip
HAVING nb_destinations > 10
ORDER BY nb_destinations DESC;
```

---

## 🧪 6. Suspicion de contournement (accès VPN / TOR)

```sql
SELECT src_ip, url_domain, COUNT(*) AS tentatives
FROM 'datasets/stormshield_logs.csv'
WHERE url_domain IN ('protonvpn.com', 'nordvpn.com', 'torproject.org', 'hide.me', 'vpnbook.com')
GROUP BY src_ip, url_domain
ORDER BY tentatives DESC;
```

---

## 🔐 7. Ports de destination suspects

```sql
SELECT dest_port,
       COUNT(*) AS connexions,
       SUM(bytes_out + bytes_in)/1024/1024 AS total_Mo
FROM 'datasets/stormshield_logs.csv'
WHERE dest_port NOT IN (80, 443, 53)
GROUP BY dest_port
ORDER BY total_Mo DESC;
```

---

## 📊 8. TOP utilisateurs (si enrichissement user présent)

```sql
SELECT user,
       SUM(bytes_out + bytes_in)/1024/1024 AS total_Mo,
       COUNT(*) AS connexions
FROM 'datasets/stormshield_logs.csv'
GROUP BY user
ORDER BY total_Mo DESC;
```

---

## 📎 Bonus : Export vers fichier parquet

```sql
COPY (
    SELECT src_ip, SUM(bytes_out) AS total_out
    FROM 'datasets/stormshield_logs.csv'
    GROUP BY src_ip
) TO 'output/top_ips.parquet' (FORMAT 'parquet');
```

---

💡 **Astuce** : DuckDB peut aussi lire des fichiers parquet, JSON, SQLite, ou pandas DataFrames directement.

