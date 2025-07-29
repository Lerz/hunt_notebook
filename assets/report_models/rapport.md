\# 🕵️‍♂️ Rapport de Hunt – Suspicion de fuite de données



\## 🔒 Contexte de la chasse



\- \*\*Nom du Hunt\*\* : Suspicious Data Exfiltration via Guest WiFi  

\- \*\*Date de la campagne\*\* : du 15/07/2024 au 22/07/2024  

\- \*\*Analyste en charge\*\* : \_Prénom NOM\_  

\- \*\*Outil(s) utilisé(s)\*\* : Splunk, JupyterLab, Python, export CSV  

\- \*\*Objectif\*\* :  

&nbsp; Identifier d'éventuelles fuites de données via des services cloud accessibles depuis le réseau invité.



---



\## 🧠 Hypothèses de départ



\- Utilisation de services de transfert (Dropbox, Mega, Wetransfer…)

\- Transferts sortants élevés en volume

\- Accès réseau sur des plages horaires inhabituelles

\- Tentative d’évasion via VPN ou IP directe

\- Résolution DNS vers domaines exotiques



---



\## 🛠️ Méthodologie



\- \*\*Données analysées\*\* :

&nbsp; - `index=stormshield` (logs réseau)

&nbsp; - `index=portail\_captif` (authentification invité)

&nbsp; - `index=sysmon` (pour enrichissement des assets)

\- \*\*Période analysée\*\* : 15/07/2024 00:00 → 22/07/2024 23:59

\- \*\*Filtres appliqués\*\* :

&nbsp; - `action=accept`

&nbsp; - `volume\_total > 50 Mo`

&nbsp; - `url\_domain IN ("dropbox.com", "mega.nz", "transfer.sh", ...)`

\- \*\*Enrichissements\*\* :

&nbsp; - Mapping `src\_ip → user/host`

&nbsp; - Marquage IP publique/privée

&nbsp; - Catégorisation protocolaire (`dest\_port`)



---



\## 📊 Résultats



\### 🔹 Résumé global



| Indicateur                     | Valeur             |

|-------------------------------|--------------------|

| IPs analysées                 | 183                |

| IPs suspectes                 | 4                  |

| Volume total sortant détecté | 31,2 Go            |

| Accès à services cloud       | 134 événements     |



---



\### 🔹 Top IP par volume sortant



| IP source     | Volume sortant | Utilisateur    | IP type   |

|---------------|----------------|----------------|-----------|

| 172.22.11.42  | 6,2 Go         | wguest\_313     | Interne   |

| 172.22.15.77  | 4,8 Go         | wguest\_444     | Interne   |



---



\### 🔹 Accès aux services de transfert



| IP source     | Domaine        | Volume estimé | Date/Heure         |

|---------------|----------------|----------------|--------------------|

| 172.22.11.42  | dropbox.com     | 3.8 Go         | 2024-07-16 14:12   |

| 172.22.15.77  | wetransfer.com  | 4.1 Go         | 2024-07-18 03:47   |



---



\## 🧠 Analyse comportementale



\- Activité réseau nocturne entre 2h et 5h du matin

\- Résolution DNS vers `.xyz`, `.top` (potentiellement DGA ou malveillants)

\- Communication vers `vpnbook.com`, `protonvpn.com`

\- Tentatives d'accès à `file.io`, `gofile.io`



---



\## 🧩 Signaux faibles à surveiller



\- Accès HTTP vers IP directe (pas de domaine DNS)

\- Flux vers ports non standards : 22, 445, 8080

\- Postes avec comportement épisodique mais anormal



---



\## ✅ Conclusion



Des éléments convergent vers \*\*une suspicion de fuite de données volontaire\*\* via un poste sur réseau invité :

\- Volumes sortants significatifs

\- Accès répétés à services de transfert

\- Activité réseau hors heures normales

\- Tentative de camouflage via VPN/HTTPS



---



\## 🚨 Recommandations



| Action                                                      | Priorité |

|-------------------------------------------------------------|----------|

| Identifier les utilisateurs associés aux IPs concernées     | Haute    |

| Extraire les artefacts réseau pour investigation poussée    | Haute    |

| Bloquer temporairement les domaines détectés                | Moyenne  |

| Réviser les règles d'accès au réseau invité                 | Moyenne  |

| Mettre en place détection Splunk sur ces patterns           | Haute    |

| Informer le DPO si suspicion avérée                         | Selon contexte |



---



\## 📎

