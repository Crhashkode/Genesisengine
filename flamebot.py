import os
import discord
import asyncio
from discord.ext import commands
from Interface.interface_discord import (
    handle_mint, handle_balance, handle_withdraw,
    handle_ping, handle_status
)
from Vault.vault import log_event  # <<== Vault logging added

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
bot = commands.Bot(command_prefix='!', intents=intents)

DISCORD_CHANNEL_ID = os.getenv("DISCORD_CHANNEL_ID")
if not DISCORD_CHANNEL_ID or not DISCORD_CHANNEL_ID.isdigit():
    print("[ERROR] DISCORD_CHANNEL_ID is missing or invalid")
    DISCORD_CHANNEL_ID = 0
else:
    DISCORD_CHANNEL_ID = int(DISCORD_CHANNEL_ID)

@bot.event
async def on_ready():
    print(f"[READY] FlameBot is online as {bot.user}")
    try:
        channel = bot.get_channel(DISCORD_CHANNEL_ID)
        if channel:
            await channel.send("**[FLAMEBOT ONLINE]** Ready to ignite. All systems synced with Genesis Engine.")
            log_event("flamebot_start", {"status": "ready", "bot_id": str(bot.user.id)})
        else:
            print("[WARNING] Could not find the channel.")
    except Exception as e:
        print(f"[ERROR] Discord message failed: {str(e)}")

@bot.command()
async def mint(ctx):
    await handle_mint(ctx)

@bot.command()
async def balance(ctx):
    await handle_balance(ctx)

@bot.command()
async def withdraw(ctx, wallet: str, amount: float):
    await handle_withdraw(ctx, wallet, amount)

@bot.command()
async def ping(ctx):
    await handle_ping(ctx)

@bot.command()
async def status(ctx):
    await handle_status(ctx)

def run_bot():
    token = os.getenv("DISCORD_BOT_TOKEN")
    if not token:
        print("[ERROR] Missing DISCORD_BOT_TOKEN in environment.")
        return
    bot.run(token)

if __name__ == "__main__":
    run_bot()