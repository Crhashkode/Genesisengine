import os
import discord
from discord.ext import commands
from quanta import Quanta
from forge import Forge
from snake import Snake
from Interface import interface_discord

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# AI Nodes
quanta = Quanta(bot)
forge = Forge()
snake = Snake()

@bot.event
async def on_ready():
    forge.ensure_vault()
    print(f"[TRINODE READY] Logged in as {bot.user}")
    channel_id = os.getenv("DISCORD_CHANNEL_ID")
    if channel_id:
        channel = bot.get_channel(int(channel_id))
        if channel:
            await channel.send("**[TRINODE ONLINE]** Quanta, Forge, and Snake operational.")

bot.load_extension("Interface.interface_discord")

def run():
    token = os.getenv("DISCORD_BOT_TOKEN")
    if not token:
        print("[ERROR] Missing DISCORD_BOT_TOKEN in environment.")
        return
    bot.run(token)

if __name__ == "__main__":
    run()