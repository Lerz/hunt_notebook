# SPLUNK HUNT Cheatsheet – Fuite de données / Exfiltration

Ce document contient une série de requêtes SPL utiles pour détecter des scénarios courants de fuite ou exfiltration de données.

---

## 1. Top IP par volume sortant (détection brute)

```spl
index=stormshield sourcetype=stormshield* action=accept
| stats sum(bytes_out) as total_out by src_ip
| where total_out > 50000000
| eval total_out_MB=round(total_out/1024/1024, 2)
| sort - total_out_MB
```

---

## 2. Requêtes vers des services de partage de fichiers (cloud / dropzone)

```spl
index=stormshield sourcetype=stormshield* action=accept
url_domain IN ("dropbox.com", "gofile.io", "wetransfer.com", "mega.nz", "anonfiles.com", "file.io")
| stats count, sum(bytes_out) as volume by src_ip, url_domain
| eval volume_MB=round(volume/1024/1024, 2)
| sort - volume_MB
```

---

## 3. DNS tunneling (requêtes longues ou nombreuses)

```spl
index=dns sourcetype=*dns*
| eval label_count = mvcount(split(query, "."))
| eval fqdn_len = len(query)
| stats count by query, label_count, fqdn_len
| where label_count > 6 OR fqdn_len > 80
| sort - fqdn_len
```

---

## 4. Multi-destinations (scan, beacon, exfil)

```spl
index=stormshield sourcetype=stormshield* action=accept
| stats dc(dest_ip) as nb_dest, count by src_ip
| where nb_dest > 10
| sort - nb_dest
```

---

## 5. Volume réseau par TLD

```spl
index=stormshield sourcetype=stormshield* action=accept
| eval tld=lower(replace(url_domain, ".*\.(\w+)$", "\1"))
| stats sum(bytes_out) as out_bytes by tld
| eval out_MB=round(out_bytes/1024/1024, 2)
| sort - out_MB
```

---

## 6. Analyse temporelle (volume par heure)

```spl
index=stormshield sourcetype=stormshield* action=accept
| bin _time span=1h
| stats sum(bytes_out) as volume_out by _time
| eval MB_out=round(volume_out/1024/1024, 2)
| sort _time
```

---

## 7. Mapping IP → Utilisateur

```spl
index=stormshield sourcetype=stormshield* action=accept
| lookup local=true sysmon_identity_map src_ip OUTPUT user, host
| stats sum(bytes_out) as total_out by src_ip, user, host
| eval MB_out=round(total_out/1024/1024, 2)
| sort - MB_out
```

---

## 8. Pattern répétitif (fréquence + volume)

```spl
index=stormshield sourcetype=stormshield* action=accept
| timechart span=5m sum(bytes_out) as volume_out by src_ip
```

---

## 9. Exfiltration vers ports non standards

```spl
index=stormshield sourcetype=stormshield* action=accept
| search dest_port!=443 dest_port!=80
| stats sum(bytes_out) as out_bytes by src_ip, dest_port
| eval out_MB=round(out_bytes/1024/1024, 2)
| sort - out_MB
```

---

## 10. Utilisation de VPN ou TOR (enrichissement requis)

```spl
index=stormshield sourcetype=stormshield* action=accept
| lookup vpn_domains url_domain OUTPUT url_domain as match
| search match=*
| stats sum(bytes_out) as out_volume by src_ip, url_domain
| eval out_MB=round(out_volume/1024/1024, 2)
```

---

## Tips

- Utilise `| lookup` avec enrichissement pour `user`, `host`, `IOC`, `majestic_million`
- Trie toujours par `bytes_out` ou `volume` pour prioriser

