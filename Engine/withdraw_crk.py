import os
import base64
from solders.keypair import Keypair
from solders.pubkey import Pubkey as PublicKey
from solana.rpc.api import Client
from solders.transaction import VersionedTransaction
from spl.token.instructions import (
    get_associated_token_address,
    create_associated_token_account,
    transfer_checked,
)
from spl.token.constants import TOKEN_PROGRAM_ID

def withdraw_crk_token(client: Client, recipient: PublicKey):
    secret = os.getenv("SOLANA_PRIVATE_KEY")
    decoded = base64.b64decode(secret)
    wallet = Keypair.from_bytes(decoded[:32])
    mint = PublicKey(os.getenv("CRK_MINT_ADDRESS"))

    ata = get_associated_token_address(recipient, mint)
    sender_ata = get_associated_token_address(wallet.pubkey(), mint)

    blockhash = client.get_latest_blockhash().value.blockhash
    txn = VersionedTransaction.populate(
        payer=wallet.pubkey(),
        instructions=[
            transfer_checked(
                sender=sender_ata,
                recipient=ata,
                owner=wallet.pubkey(),
                amount=1,
                decimals=9,
                mint=mint,
                program_id=TOKEN_PROGRAM_ID
            )
        ],
        recent_blockhash=blockhash
    )
    txn.sign([wallet])
    response = client.send_transaction(txn)
    return response
