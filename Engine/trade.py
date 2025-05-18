import requests
import os
from solana.rpc.api import Client
from solana.keypair import Keypair
from solana.publickey import PublicKey
from solana.transaction import Transaction
from solana.rpc.types import TxOpts
import base64

# Load environment
RPC_URL = os.getenv("SOLANA_RPC_URL", "https://api.mainnet-beta.solana.com")
PRIVATE_KEY = os.getenv("SOLANA_PRIVATE_KEY")
CRK_MINT = os.getenv("CRK_MINT_ADDRESS")  # Set this in secrets

wallet = Keypair.from_secret_key(base64.b64decode(PRIVATE_KEY))
client = Client(RPC_URL)

def get_best_swap_route(input_mint, output_mint, amount):
    url = f"https://quote-api.jup.ag/v6/quote?inputMint={input_mint}&outputMint={output_mint}&amount={amount}&slippage=1"
    res = requests.get(url)
    return res.json()['data'][0]  # Top route

def execute_swap(route):
    swap_tx_url = "https://quote-api.jup.ag/v6/swap"
    swap_request = {
        "route": route,
        "userPublicKey": str(wallet.public_key),
        "wrapUnwrapSOL": True,
        "feeAccount": None
    }

    response = requests.post(swap_tx_url, json=swap_request)
    swap_data = response.json()

    if 'swapTransaction' not in swap_data:
        print("[ERROR] Swap transaction not returned")
        return None

    tx_base64 = swap_data["swapTransaction"]
    tx_bytes = base64.b64decode(tx_base64)
    tx = Transaction.deserialize(tx_bytes)

    tx.sign(wallet)
    result = client.send_transaction(tx, wallet, opts=TxOpts(skip_confirmation=False, preflight_commitment="confirmed"))
    print(f"[SWAP SUCCESS] Tx: https://solscan.io/tx/{result['result']}")
    return result["result"]

# Example usage
if __name__ == "__main__":
    CRK = CRK_MINT
    SOL = "So11111111111111111111111111111111111111112"
    lamports = 1000000  # 1 CRK assuming 6 decimals

    route = get_best_swap_route(CRK, SOL, lamports)
    execute_swap(route)
