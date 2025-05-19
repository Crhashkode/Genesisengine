import os
import base64
from solders.transaction import Transaction
from solana.rpc.api import Client
from solana.keypair import Keypair
from spl.token.instructions import get_associated_token_address
from Vault.vault import log_event
from Engine.ws_confirm import confirm_signature
import asyncio

# === ENV SETUP ===
PRIVATE_KEY = os.getenv("PRIVATE_KEY_BASE64")
CRK_MINT_ADDRESS = os.getenv("CRK_MINT_ADDRESS")
RPC_URL = os.getenv("SOLANA_RPC_URL", "https://api.mainnet-beta.solana.com")
client = Client(RPC_URL)

# === WALLET SETUP ===
if not PRIVATE_KEY:
    raise Exception("PRIVATE_KEY_BASE64 is not set.")
decoded = base64.b64decode(PRIVATE_KEY)
keypair = Keypair.from_secret_key(decoded)

def mint_crk_token():
    tx_sig = "SimulatedMintSignature"
    log_event("mint_crk_token", {"tx": tx_sig})
    asyncio.run(confirm_signature(tx_sig))  # Real logic would await real tx
    return tx_sig

def get_crk_balance(mint_address: str):
    ata = get_associated_token_address(owner=keypair.public_key, mint=mint_address)
    resp = client.get_token_account_balance(ata)
    if resp.get("result"):
        return resp["result"]["value"]["uiAmount"]
    return 0.0

def transfer_crk(to_wallet: str, amount: float):
    tx_sig = "SimulatedTransferSignature"
    log_event("transfer_crk", {"to": to_wallet, "amount": amount, "tx": tx_sig})
    return tx_sig