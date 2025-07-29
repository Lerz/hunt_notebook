# ROADMAP — Projet Hunt-Lab

Cette roadmap présente les principales évolutions prévues pour le projet `hunt-lab`, réparties par domaine fonctionnel et priorité. Elle évolue en fonction des besoins d'analyse, de performance, et des retours utilisateurs.

---

## Analyse & Détection (Hunting Logic)

- [ ] Intégration de règles Sigma dans le pipeline (via SigmaHQ et `sigmac`)
- [ ] Générateur de requêtes Splunk depuis règles Sigma + mapping maison
- [ ] Implémentation d’un moteur de scoring comportemental simple (baseline de trafic)
- [ ] Ajout de détections orientées IoT / VPN / DNS tunneling
- [ ] Détection automatique de données sensibles exfiltrées (regex e-mail, RIB, identifiants)

---

## Interface & Notebooks

- [ ] Centralisation des notebooks par type de use-case (`dns`, `vpn`, `upload`, etc.)
- [ ] Ajout d’un notebook "Dashboard" interactif avec widgets (via `voila` ou `panel`)
- [ ] Notebooks de visualisation comparative entre plusieurs sessions (baseline vs anomalie)
- [ ] Ajout de notebook sur la partie analyse comportementale avec un peu de détection automatique

---

## Enrichissement & Règles

- [ ] Ajout d’un parseur YARA pour enrichir les IOC collectés
- [ ] Mise à jour automatique des listes `majestic_million`, GeoIP2, et ASNs
- [ ] Support des enrichissements via données MITRE ATT&CK + TTP scoring
- [ ] Génération automatique de rapports IOC + enrichissements type Sigma-like

---

## LLM / IA locale

- [ ] RAG hybride : tabulaire + vectoriel basé sur logs + playbooks
- [ ] Fine-tuning léger pour adapter les réponses à un environnement spécifique
- [ ] Notebook interactif LLM + interface de contrôle du contexte d'analyse

---

## Gestion des données & performance

- [ ] Implémentation d’un cache de features enrichies (`datasets/features_cache.parquet`)
- [ ] Support complet du format Parquet dans toute la chaîne
- [ ] Compression automatique des résultats volumineux dans `data/`
- [ ] Ajout de metadata (SHA256, timestamp, source) à chaque export pour traçabilité

---

## Utilitaires & outils CLI

- [ ] CLI de lancement de notebooks en ligne de commande avec paramètres
- [ ] CLI de "hunt session init" pour créer automatiquement les dossiers, NOTICE.md, etc.
- [ ] Script de purge intelligente des anciens résultats

---

## Documentation

- [ ] Générateur statique de doc (Markdown → HTML/PDF)
- [ ] Mode offline complet avec téléchargement des docs Splunk, MITRE, etc.
- [ ] Exemple de cas d’usage documenté : *DNS exfiltration* pas à pas

---

## Long terme

- [ ] Interface web de consultation des résultats (via Streamlit ou Flask)
- [ ] Support multi-utilisateur avec sessions, tagging et historisation
- [ ] Intégration d’exports vers Splunk/Elastic pour retour dans le pipeline SOC

---

_Mise à jour : 29 juillet 2025_
