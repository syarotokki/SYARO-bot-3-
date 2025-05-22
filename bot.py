from discord.ext import commands, tasks
import discord
import json
from utils.youtube import fetch_latest_video  # 要確認

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
    check_new_videos.start()  # ✅ 自動通知開始

@tasks.loop(minutes=5)
async def check_new_videos():
    with open("config.json", "r") as f:
        config = json.load(f)

    for guild_id, data in config.items():
        channel = bot.get_channel(data["channel_id"])
        latest_video = fetch_latest_video(data["youtube_channel_id"])
        if latest_video:
            await channel.send(latest_video)

# コマンドセットアップはそのまま
from commands.subscribe import setup_subscribe
from commands.notify_past import setup_notify_past
from commands.notify_latest import setup_notify_latest

setup_subscribe(bot)
setup_notify_past(bot)
setup_notify_latest(bot)
