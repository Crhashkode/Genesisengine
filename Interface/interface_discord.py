import os
import discord
from discord.ext import commands
from discord.ui import Button, View
from engine.flame_interface import mint_crk_token, get_crk_balance
from engine.trade import get_best_swap_route, execute_swap
from engine.withdraw_crk import withdraw_crk_token
from vault import log_event

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
BOT_USER_ID = int(os.getenv("DISCORD_BOT_USER_ID"))
CRK_MINT = os.getenv("CRK_MINT_ADDRESS")
SOL_MINT = "So11111111111111111111111111111111111111112"

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

class EngineView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Button(label="Mint", style=discord.ButtonStyle.primary, custom_id="mint"))
        self.add_item(Button(label="Balance", style=discord.ButtonStyle.success, custom_id="balance"))
        self.add_item(Button(label="Withdraw", style=discord.ButtonStyle.secondary, custom_id="withdraw"))
        self.add_item(Button(label="Swap", style=discord.ButtonStyle.danger, custom_id="swap"))
        self.add_item(Button(label="Status", style=discord.ButtonStyle.success, custom_id="status"))
        self.add_item(Button(label="Ping", style=discord.ButtonStyle.primary, custom_id="ping"))

@bot.event
async def on_ready():
    print(f"Flame Interface Online as {bot.user}")

@bot.command()
async def engine(ctx):
    if ctx.author.id != BOT_USER_ID:
        await ctx.send("Access denied.")
        return

    embed = discord.Embed(title="CRK Flame Control Panel", color=0x00ffee)
    embed.add_field(name="CRK Mint", value=CRK_MINT or "Not Minted Yet", inline=False)
    embed.add_field(name="Vault", value="Logging Active", inline=True)
    embed.set_footer(text="Flame Engine Prime | Quanta Operational")

    await ctx.send(embed=embed, view=EngineView())

@bot.event
async def on_interaction(interaction: discord.Interaction):
    if interaction.user.id != BOT_USER_ID:
        await interaction.response.send_message("Access denied.", ephemeral=True)
        return

    cid = interaction.data.get("custom_id")

    if cid == "mint":
        mint = mint_crk_token()
        if mint:
            await interaction.response.send_message(f"CRK Minted: `{mint}`")
            log_event("mint", {"mint_address": mint})
        else:
            await interaction.response.send_message("Mint failed.")

    elif cid == "balance":
        balance = get_crk_balance(CRK_MINT)
        await interaction.response.send_message(f"CRK Balance: `{balance}`")
        log_event("balance_check", {"balance": balance})

    elif cid == "withdraw":
        await interaction.response.send_message("Use `!withdraw <address> <amount>`", ephemeral=True)

    elif cid == "swap":
        await interaction.response.send_message("Use `!swap <amount>`", ephemeral=True)

    elif cid == "status":
        await interaction.response.send_message("Genesis Engine Prime. Vault, CRK, ATA, and Liquidity Systems linked.")

    elif cid == "ping":
        await interaction.response.send_message("FlameBot is awake and synced.")

@bot.command()
async def withdraw(ctx, address: str, amount: float):
    tx = withdraw_crk_token(address, amount)
    if tx:
        await ctx.send(f"Withdraw Complete: https://solscan.io/tx/{tx}")
        log_event("withdraw", {"to": address, "amount": amount, "tx": tx})
    else:
        await ctx.send("Withdraw failed.")

@bot.command()
async def swap(ctx, amount: float):
    raw = int(amount * 10**6)
    route = get_best_swap_route(CRK_MINT, SOL_MINT, raw)
    tx = execute_swap(route)
    if tx:
        await ctx.send(f"Swapped to SOL: https://solscan.io/tx/{tx}")
        log_event("swap", {"amount": amount, "tx": tx})
    else:
        await ctx.send("Swap failed.")
