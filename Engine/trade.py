import os
import requests
from solana.keypair import Keypair
from solana.rpc.api import Client
from solana.rpc.types import TxOpts
import base64
from vault.vault import log_event

RPC_URL = os.getenv("SOLANA_RPC_URL", "https://api.mainnet-beta.solana.com")
PRIVATE_KEY = os.getenv("PRIVATE_KEY_BASE64")
CRK_MINT = os.getenv("CRK_MINT_ADDRESS")
SOL_MINT = "So11111111111111111111111111111111111111112"

if not PRIVATE_KEY:
    raise Exception("PRIVATE_KEY_BASE64 is not set.")
decoded = base64.b64decode(PRIVATE_KEY)
keypair = Keypair.from_secret_key(decoded)
client = Client(RPC_URL)

def get_best_swap_route(input_mint: str, output_mint: str, amount: int):
    url = f"https://quote-api.jup.ag/v6/quote?inputMint={input_mint}&outputMint={output_mint}&amount={amount}&slippageBps=50"
    res = requests.get(url)
    return res.json()["data"][0] if "data" in res.json() else None

def execute_swap(route: dict):
    if not route:
        return None
    swap_url = "https://quote-api.jup.ag/v6/swap"
    swap_body = {
        "route": route,
        "userPublicKey": str(keypair.public_key),
        "wrapUnwrapSOL": True,
        "feeAccount": None
    }
    headers = {"Content-Type": "application/json"}
    res = requests.post(swap_url, json=swap_body, headers=headers)
    swap_tx = res.json()["swapTransaction"]
    from base64 import b64decode
    from solana.transaction import Transaction
    tx_bytes = b64decode(swap_tx)
    txn = Transaction.deserialize(tx_bytes)
    sig = client.send_transaction(txn, keypair, opts=TxOpts(skip_preflight=True, preflight_commitment="processed"))
    log_event("crk_swap", {"route": route, "tx": sig["result"]})
    return sig["result"]