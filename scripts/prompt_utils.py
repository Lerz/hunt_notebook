"""
prompt_utils.py

Utilitaires pour formater un DataFrame réseau (e.g. export Splunk) en prompt lisible par LLM.
"""

import pandas as pd

def format_logs_for_prompt(df: pd.DataFrame, max_rows=5) -> str:
    output = []
    cols = df.columns.tolist()
    output.append("Colonnes : " + ", ".join(cols))
    output.append("Échantillon :")
    for _, row in df.head(max_rows).iterrows():
        line = " | ".join(str(row[c]) for c in cols)
        output.append("  - " + line)
    return "\n".join(output)
