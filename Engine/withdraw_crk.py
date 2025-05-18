import os
import json
from solana.rpc.api import Client
from solana.transaction import Transaction
from solana.keypair import Keypair
from solana.system_program import SYS_PROGRAM_ID
from spl.token.instructions import transfer_checked, get_associated_token_address, create_associated_token_account
from spl.token.constants import TOKEN_PROGRAM_ID

CRK_DECIMALS = 6
RPC_URL = os.getenv("SOLANA_RPC_URL", "https://api.mainnet-beta.solana.com")
MINT_ADDRESS = os.getenv("CRK_MINT_ADDRESS")

keypair_array = json.loads(os.getenv("WALLET_KEYPAIR"))
wallet = Keypair.from_bytes(bytes(keypair_array))
client = Client(RPC_URL)

def withdraw_crk_token(recipient_address: str, amount: float):
    try:
        from solana.publickey import PublicKey
        mint = PublicKey(MINT_ADDRESS)
        recipient = PublicKey(recipient_address)

        source_ata = get_associated_token_address(wallet.public_key, mint)
        dest_ata = get_associated_token_address(recipient, mint)

        tx = Transaction()

        # Check if recipient ATA exists
        resp = client.get_account_info(dest_ata)
        if resp["result"]["value"] is None:
            tx.add(
                create_associated_token_account(
                    payer=wallet.public_key,
                    owner=recipient,
                    mint=mint
                )
            )

        tx.add(
            transfer_checked(
                source=source_ata,
                dest=dest_ata,
                owner=wallet.public_key,
                amount=int(amount * 10**CRK_DECIMALS),
                decimals=CRK_DECIMALS,
                mint=mint,
                program_id=TOKEN_PROGRAM_ID
            )
        )

        tx_sig = client.send_transaction(tx, wallet)["result"]
        return tx_sig

    except Exception as e:
        print(f"[WITHDRAW ERROR] {str(e)}")
        return None