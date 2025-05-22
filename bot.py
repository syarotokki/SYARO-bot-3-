from discord.ext import commands, tasks
import discord
import json
from utils.youtube import fetch_latest_video  # ← URLだけでなく video_id など含む dict を返す関数
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
    check_new_videos.start()

@tasks.loop(minutes=5)
async def check_new_videos():
    try:
        with open("config.json", "r") as f:
            config = json.load(f)
    except FileNotFoundError:
        return

    try:
        with open("notified.json", "r") as f:
            notified = json.load(f)
    except FileNotFoundError:
        notified = {}

    for guild_id, data in config.items():
        channel = bot.get_channel(data["channel_id"])
        latest = fetch_latest_video(data["youtube_channel_id"])

        if not latest:
            continue

        video_id = latest["video_id"]
        if notified.get(guild_id) == video_id:
            continue  # 通知済みなのでスキップ

        message = (
            f'📢 新しい動画が投稿されました！\n'
            f'{latest["title"]}\n{latest["url"]}'
        )
        await channel.send(message)

        notified[guild_id] = video_id
        with open("notified.json", "w") as f:
            json.dump(notified, f, indent=4)

# スラッシュコマンド登録
setup_subscribe(bot)
setup_notify_past(bot)
setup_notify_latest(bot)


setup_subscribe(bot)
setup_notify_past(bot)
setup_notify_latest(bot)
