"""
splunk_export.py

Outil minimal pour récupérer une recherche Splunk (via REST API) et sauvegarder le résultat en CSV local.
"""

import requests
import time
import urllib3
urllib3.disable_warnings()

def download_search_to_csv(host, token, search_query, output_file, earliest_time="-24h", latest_time="now"):
    headers = {
        "Authorization": f"Bearer {token}"
    }

    # Step 1: Create search job
    search_url = f"{host}/services/search/jobs"
    payload = {
        "search": f"search {search_query}",
        "earliest_time": earliest_time,
        "latest_time": latest_time,
        "output_mode": "json"
    }
    response = requests.post(search_url, headers=headers, data=payload, verify=False)
    response.raise_for_status()
    sid = response.json()["sid"]

    # Step 2: Poll until ready
    while True:
        status_url = f"{host}/services/search/jobs/{sid}"
        r = requests.get(status_url, headers=headers, params={"output_mode": "json"}, verify=False)
        done = r.json()["entry"][0]["content"]["isDone"]
        if done:
            break
        time.sleep(2)

    # Step 3: Get results
    results_url = f"{host}/services/search/jobs/{sid}/results"
    r = requests.get(results_url, headers=headers, params={"output_mode": "csv"}, verify=False)
    with open(output_file, "wb") as f:
        f.write(r.content)
    print(f"[✓] Résultats sauvegardés dans {output_file}")
