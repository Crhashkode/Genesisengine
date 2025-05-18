import os
import json
from datetime import datetime
from vault import log_event

VAULT_PATH = "Vault/vault.json"

def log_event(event_type, data):
    log_entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "type": event_type,
        "data": data
    }

    if not os.path.exists(VAULT_PATH):
        with open(VAULT_PATH, "w") as f:
            json.dump({"logs": [log_entry]}, f, indent=2)
    else:
        with open(VAULT_PATH, "r+") as f:
            try:
                existing = json.load(f)
                existing["logs"].append(log_entry)
                f.seek(0)
                json.dump(existing, f, indent=2)
                f.truncate()
            except json.JSONDecodeError:
                f.seek(0)
                json.dump({"logs": [log_entry]}, f, indent=2)
                f.truncate()