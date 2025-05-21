from discord import app_commands
import discord
from utils.youtube import fetch_latest_video
import json

OWNER_ID = 1105948117624434728

def setup_notify_latest(bot):
    @app_commands.command(name="notify_latest", description="最新の動画またはライブを通知（開発者限定）")
    async def notify_latest(interaction: discord.Interaction):
        if interaction.user.id != OWNER_ID:
            await interaction.response.send_message("このコマンドは開発者のみ使用できます。", ephemeral=True)
            return

        with open("config.json", "r") as f:
            config = json.load(f)

        for guild_id, data in config.items():
            channel = bot.get_channel(data["channel_id"])
            video = fetch_latest_video(data["youtube_channel_id"])
            if video:
                await channel.send(video)

        await interaction.response.send_message("通知を送信しました！", ephemeral=True)

    bot.tree.add_command(notify_latest)
