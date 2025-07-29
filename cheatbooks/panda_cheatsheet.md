# Pandas Cheatsheet — Investigation & Hunting

## 1. Chargement & aperçu des données

```python
import pandas as pd

df = pd.read_csv("mon_dataset.csv")               # Charger un CSV
df = pd.read_parquet("mon_dataset.parquet")       # Charger un Parquet

df.head(5)                                         # Les 5 premières lignes
df.tail(3)                                         # Les 3 dernières
df.sample(10)                                      # 10 lignes aléatoires
df.columns.tolist()                                # Liste des colonnes
df.info()                                          # Structure (types, null)
df.describe()                                      # Statistiques num (moy, min, etc.)
```

---

## 2. Filtrage, recherche, slicing

```python
df[df["src_ip"] == "10.0.0.1"]                     # Filtrer une IP
df[df["bytes_out"] > 1_000_000]                    # Volume > 1Mo
df[df["url_domain"].str.contains("facebook")]      # Domaine spécifique
df[df["port"].isin([80, 443, 22])]                 # Ports connus
df[~df["country"].isin(["FR", "BE"])]              # Exclure pays

df.loc[:, ["src_ip", "dest_ip", "bytes_out"]]      # Sélection de colonnes
df.iloc[0:5]                                       # Lignes 0 à 4 (par index)
```

---

## 3. Agrégation & statistiques

```python
df.groupby("src_ip")["bytes_out"].sum().sort_values(ascending=False)  # Volume par IP
df.groupby("url_domain").size().sort_values(ascending=False)          # Domaines les plus appelés
df.groupby("user")["src_ip"].nunique()                                # Nb d’IP par user

df["hour"] = pd.to_datetime(df["timestamp"]).dt.hour                  # Extraire heure
df.groupby("hour")["bytes_out"].sum().plot()                          # Trafic par heure
```

---

## 4. Nettoyage et transformation

```python
df.drop_duplicates(inplace=True)
df.dropna(subset=["user"], inplace=True)
df["bytes_total"] = df["bytes_in"] + df["bytes_out"]
df["Go_total"] = round(df["bytes_total"] / (1024**3), 2)
df["is_external"] = df["src_ip"].str.startswith("192.") == False
```

---

## 5. Enrichissement & feature engineering

```python
df["port_type"] = df["dest_port"].map({
    53: "DNS", 80: "HTTP", 443: "HTTPS", 22: "SSH"
}).fillna("Autre")

df["domain_score"] = df["url_domain"].apply(lambda d: 10 if "tiktok" in d else 0)
df["volume_level"] = pd.qcut(df["bytes_total"], q=4, labels=["low", "mid", "high", "very high"])
```

---

## 6. Recherche d'anomalies simples

```python
df[df["bytes_out"] > df["bytes_out"].quantile(0.99)]          # Top 1% en sortie
df[df["url_domain"].str.count("\.") > 4]                      # Domaines très imbriqués (ex: DGA)
df[df["bytes_in"] == 0]                                       # Trafic unidirectionnel
```

---

## 7. Export

```python
df.to_csv("output/volumes_by_ip.csv", index=False)
df.to_parquet("output/volumes_enriched.parquet", index=False)
```

---

## 8. Utilitaires fréquents

```python
df["timestamp"] = pd.to_datetime(df["timestamp"])             # Convertir en datetime
df.columns = df.columns.str.lower().str.replace(" ", "_")     # Nettoyer noms colonnes
df.sort_values("bytes_total", ascending=False, inplace=True)  # Tri
```

---

## 9. Pivot et analyse croisée

```python
pd.crosstab(df["user"], df["is_external"])                    # Nb d’IP internes/externes par user
df.pivot_table(index="src_ip", values="bytes_out", aggfunc="sum")
```

---