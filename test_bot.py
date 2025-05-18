import discord
import os

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")

token = os.getenv("DISCORD_BOT_TOKEN")
bot.run(token)