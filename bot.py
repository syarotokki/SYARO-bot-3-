from discord.ext import commands
import discord
from commands.subscribe import setup_subscribe
from commands.notify_past import setup_notify_past
from commands.notify_latest import setup_notify_latest

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands.")
    except Exception as e:
        print(f"Sync failed: {e}")

setup_subscribe(bot)
setup_notify_past(bot)
setup_notify_latest(bot)
