import discord
from discord.ext import commands
import os
from commands.subscribe import setup_subscribe
from commands.notify_latest import setup_notify_latest
from commands.notify_past import setup_notify_past

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await bot.tree.sync()

setup_subscribe(bot)
setup_notify_latest(bot)
setup_notify_past(bot)