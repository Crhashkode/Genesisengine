from solana.rpc.api import Client
from solana.rpc.types import TxOpts
from solana.transaction import Transaction
from solana.keypair import Keypair
from spl.token.instructions import (
    get_associated_token_address, create_associated_token_account,
    transfer_checked
)
import base64, os
from Vault.vault import log_event

RPC_URL = os.getenv("SOLANA_RPC_URL", "https://api.mainnet-beta.solana.com")
PRIVATE_KEY = os.getenv("PRIVATE_KEY_BASE64")
CRK_MINT = os.getenv("CRK_MINT_ADDRESS")

if not PRIVATE_KEY:
    raise Exception("PRIVATE_KEY_BASE64 is not set.")
decoded = base64.b64decode(PRIVATE_KEY)
keypair = Keypair.from_secret_key(decoded)
client = Client(RPC_URL)

def withdraw_crk_token(recipient_address: str, amount: float) -> str:
    try:
        mint = CRK_MINT
        from_pub = keypair.public_key
        to_pub = recipient_address

        from_ata = get_associated_token_address(from_pub, mint)
        to_ata = get_associated_token_address(to_pub, mint)

        # Create to_ata if needed
        info = client.get_account_info(to_ata)
        txn = Transaction()
        if not info["result"]["value"]:
            txn.add(create_associated_token_account(from_pub, to_pub, mint))

        txn.add(transfer_checked(
            source=from_ata,
            dest=to_ata,
            owner=from_pub,
            mint=mint,
            amount=int(amount * 10**6),
            decimals=6
        ))

        res = client.send_transaction(txn, keypair, opts=TxOpts(skip_preflight=True, preflight_commitment="processed"))
        tx_sig = res["result"]
        log_event("withdraw_crk", {"to": recipient_address, "amount": amount, "tx": tx_sig})
        return tx_sig
    except Exception as e:
        log_event("withdraw_error", {"to": recipient_address, "error": str(e)})