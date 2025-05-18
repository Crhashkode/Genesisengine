import os
import discord
import asyncio
from discord.ext import commands
from Interface.interface_discord import (
    handle_mint, handle_balance, handle_withdraw,
    handle_ping, handle_status
)

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
bot = commands.Bot(command_prefix='!', intents=intents)

DISCORD_CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID", "0"))

@bot.event
async def on_ready():
    print(f"FlameBot is online as {bot.user}")
    channel = bot.get_channel(DISCORD_CHANNEL_ID)
    if channel:
        asyncio.ensure_future(channel.send("**[FLAMEBOT ONLINE]** Ready to ignite. All systems synced with Genesis Engine.**"))

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