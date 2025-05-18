import os
import base64
import json
from datetime import datetime
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solana.rpc.api import Client
from spl.token.instructions import get_associated_token_address
from Vault.vault import log_event

PRIVATE_KEY = os.getenv("SOLANA_PRIVATE_KEY")
RPC_URL = os.getenv("SOLANA_RPC_URL", "https://api.mainnet-beta.solana.com")
CRK_MINT = os.getenv("CRK_MINT_ADDRESS")
VAULT_PATH = "vault/vault.json"

decoded = base64.b64decode(PRIVATE_KEY)
wallet = Keypair.from_bytes(decoded)
client = Client(RPC_URL)

class FlameInterface:
    def __init__(self):
        self.mint_address = self.load_mint()
        self.owner_wallet = str(wallet.pubkey())
        self.balance = self.get_crk_balance()
        self.status = "LIVE"
        self.withdrawals_enabled = True
        self.last_withdrawal = self.get_last_withdrawal()

    def load_mint(self):
        if os.path.exists(VAULT_PATH):
            try:
                with open(VAULT_PATH, "r") as f:
                    data = json.load(f)
                    return data.get("crk_mint", CRK_MINT)
            except Exception:
                return CRK_MINT
        return CRK_MINT

    def get_crk_balance(self):
        try:
            mint = Pubkey.from_string(self.mint_address)
            ata = get_associated_token_address(wallet.pubkey(), mint)
            result = client.get_token_account_balance(ata)
            return float(result["result"]["value"]["uiAmount"])
        except Exception as e:
            print(f"[ERROR] Failed to fetch CRK balance: {e}")
            return 0.0

    def get_last_withdrawal(self):
        if not os.path.exists(VAULT_PATH):
            return "None"
        try:
            with open(VAULT_PATH, "r") as f:
                vault = json.load(f)
                events = vault.get("events", [])
                for e in reversed(events):
                    if e["type"] == "withdraw":
                        return e["timestamp"]
        except:
            pass
        return "None"
