"""
offline_enrichment.py

Module d'enrichissement local pour analyse réseau offline (airgapped).
Ajoute :
- type IP (interne/externe)
- port/service standard
- ASN depuis GeoLite2 ASN
- réputation domaine (Majestic Million)
"""

import ipaddress
import pandas as pd
import os

# --- 1. Détection IP privée/public ---
PRIVATE_CIDRS = [
    ipaddress.ip_network('10.0.0.0/8'),
    ipaddress.ip_network('172.16.0.0/12'),
    ipaddress.ip_network('192.168.0.0/16')
]

def get_ip_type(ip):
    try:
        ip_obj = ipaddress.ip_address(ip)
        if any(ip_obj in cidr for cidr in PRIVATE_CIDRS):
            return "Interne"
        return "Externe"
    except:
        return "Invalide"

# --- 2. Mapping port standard ---
PORT_SERVICE_MAP = {
    21: "FTP", 22: "SSH", 25: "SMTP", 53: "DNS", 80: "HTTP",
    110: "POP3", 123: "NTP", 143: "IMAP", 443: "HTTPS",
    445: "SMB", 993: "IMAPS", 995: "POP3S", 3306: "MySQL",
    3389: "RDP", 5060: "SIP", 8080: "HTTP-Alt"
}

def get_port_type(port):
    try:
        return PORT_SERVICE_MAP.get(int(port), "Autre")
    except:
        return "Inconnu"

# --- 3. Enrichissement ASN (GeoLite2 ASN local) ---
try:
    import geoip2.database
    READER = geoip2.database.Reader('./data/GeoLite2-ASN.mmdb')

    def get_asn_desc(ip):
        try:
            response = READER.asn(ip)
            return f"{response.autonomous_system_organization} (AS{response.autonomous_system_number})"
        except:
            return "Inconnu"
except ImportError:
    READER = None
    def get_asn_desc(ip):
        return "GeoIP non disponible"

# --- 4. Enrichissement domaine : présence dans Majestic Million ---
MAJESTIC_PATH = "./lookups/majestic_million.csv"
if os.path.exists(MAJESTIC_PATH):
    majestic_df = pd.read_csv(MAJESTIC_PATH)
    majestic_set = set(majestic_df["Domain"].str.lower())
else:
    majestic_set = set()

def is_majestic(domain):
    try:
        return "Oui" if domain.lower() in majestic_set else "Non"
    except:
        return "Inconnu"

# --- 5. Fonction principale ---
def enrich_dataframe(df, ip_col='src_ip', port_col='dest_port', domain_col='url_domain'):
    df['ip_type'] = df[ip_col].apply(get_ip_type)
    df['port_type'] = df[port_col].apply(get_port_type)
    df['asn_desc'] = df[ip_col].apply(get_asn_desc)
    if domain_col in df.columns:
        df['in_majestic'] = df[domain_col].apply(is_majestic)
    return df
