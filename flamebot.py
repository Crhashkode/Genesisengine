import os
import discord
from discord.ext import commands
from engine.flame_interface import mint_crk_token, get_crk_balance
from engine.withdraw_crk import withdraw_crk_token
from vault import log_event
from solana.rpc.api import Client

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

SOLANA_RPC_URL = os.getenv("SOLANA_RPC_URL", "https://api.mainnet-beta.solana.com")
CRK_MINT = os.getenv("CRK_MINT_ADDRESS")
client = Client(SOLANA_RPC_URL)

@bot.event
async def on_ready():
    print(f"FlameBot is online as {bot.user}")

@bot.command()
async def mint(ctx):
    try:
        mint_address = mint_crk_token()
        await ctx.send(f"**[MINTED]** CRK Token: `{mint_address}`")
        log_event("mint", {"trigger": "bot", "mint_address": mint_address})
    except Exception as e:
        await ctx.send(f"[ERROR] Mint failed: {str(e)}")
        log_event("error", {"action": "mint", "reason": str(e)})

@bot.command()
async def balance(ctx):
    try:
        if not CRK_MINT:
            raise ValueError("CRK_MINT_ADDRESS not set.")
        balance = get_crk_balance(CRK_MINT)
        await ctx.send(f"**[BALANCE]** `{balance} CRK`")
        log_event("balance_check", {"trigger": "bot", "mint": CRK_MINT, "balance": balance})
    except Exception as e:
        await ctx.send(f"[ERROR] Balance check failed: {str(e)}")
        log_event("error", {"action": "balance", "reason": str(e)})

@bot.command()
async def withdraw(ctx, wallet: str, amount: float):
    try:
        tx = withdraw_crk_token(client, recipient_address=wallet, amount=amount)
        await ctx.send(f"**[WITHDRAWN]** `{amount} CRK` to `{wallet}`")
        await ctx.send(f"**TX:** https://solscan.io/tx/{tx}")
        log_event("withdraw", {"trigger": "bot", "to": wallet, "amount": amount, "tx": tx})
    except Exception as e:
        await ctx.send(f"[ERROR] Withdraw failed: {str(e)}")
        log_event("error", {"action": "withdraw", "reason": str(e)})

def run_bot():
    bot.run(os.getenv("DISCORD_BOT_TOKEN"))