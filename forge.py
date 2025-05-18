import os
import json

class Forge:
    def ensure_vault(self):
        path = "Vault/vault.json"
        os.makedirs("Vault", exist_ok=True)
        if not os.path.exists(path):
            with open(path, "w") as f:
                json.dump({"logs": []}, f)