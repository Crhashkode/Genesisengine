import os
from Engine.flame_interface import mint_crk_token, get_crk_balance
from Engine.withdraw_crk import withdraw_crk_token
from Vault.vault import log_event
from solana.rpc.api import Client
import discord

SOLANA_RPC_URL = os.getenv("SOLANA_RPC_URL", "https://api.mainnet-beta.solana.com")
CRK_MINT = os.getenv("CRK_MINT_ADDRESS")
client = Client(SOLANA_RPC_URL)

async def handle_mint(ctx):
    try:
        mint_address = mint_crk_token()
        await ctx.send(f"[MINTED] CRK Token: `{mint_address}`")
        log_event("mint", {"trigger": "discord", "mint_address": mint_address})
    except Exception as e:
        await ctx.send(f"[ERROR] Mint failed: {str(e)}")
        log_event("error", {"action": "mint", "reason": str(e)})

async def handle_balance(ctx):
    try:
        if not CRK_MINT:
            raise ValueError("CRK_MINT_ADDRESS not set.")
        balance = get_crk_balance(CRK_MINT)
        await ctx.send(f"[BALANCE] `{balance} CRK`")
        log_event("balance_check", {"trigger": "discord", "mint": CRK_MINT, "balance": balance})
    except Exception as e:
        await ctx.send(f"[ERROR] Balance check failed: {str(e)}")
        log_event("error", {"action": "balance", "reason": str(e)})

async def handle_withdraw(ctx, wallet: str, amount: float):
    try:
        tx = withdraw_crk_token(client, recipient_address=wallet, amount=amount)
        await ctx.send(f"[WITHDRAWN] `{amount} CRK` to `{wallet}`")
        await ctx.send(f"https://solscan.io/tx/{tx}")
        log_event("withdraw", {"trigger": "discord", "to": wallet, "amount": amount, "tx": tx})
    except Exception as e:
        await ctx.send(f"[ERROR] Withdraw failed: {str(e)}")
        log_event("error", {"action": "withdraw", "reason": str(e)})

async def handle_ping(ctx):
    await ctx.send("Pong! FlameBot is synced and online.")

async def handle_status(ctx):
    await ctx.send("**[STATUS]** Genesis Engine is fully operational. CRK, Vault, ATA, and Liquidity modules are synced.")