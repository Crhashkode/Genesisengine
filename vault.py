import json
import os
from datetime import datetime

VAULT_PATH = "Vault/vault.json"

def log_event(event_type, data):
    log = {
        "type": event_type,
        "data": data,
        "timestamp": datetime.utcnow().isoformat()
    }

    if os.path.exists(VAULT_PATH):
        with open(VAULT_PATH, "r") as f:
            vault = json.load(f)
    else:
        vault = {"logs": []}

    vault["logs"].append(log)

    with open(VAULT_PATH, "w") as f:
        json.dump(vault, f, indent=2)