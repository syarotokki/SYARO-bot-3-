from discord import app_commands
import discord
import json
from utils.youtube import fetch_latest_video

OWNER_ID = 1105948117624434728

def setup_notify_latest(bot):
    @app_commands.command(name="notify_latest", description="最新動画を通知（開発者限定）")
    async def notify_latest(interaction: discord.Interaction):
        if interaction.user.id != OWNER_ID:
            await interaction.response.send_message("このコマンドは開発者のみ使用できます。", ephemeral=True)
            return

        await interaction.response.send_message("最新動画の通知を開始します...", ephemeral=True)

        with open("config.json", "r") as f:
            config = json.load(f)

        for guild_id, data in config.items():
            channel = bot.get_channel(data["channel_id"])
            message = fetch_latest_video(data["youtube_channel_id"])
            if not message:
                continue
            await channel.send(message)

        await interaction.edit_original_response(content="最新動画の通知を送信しました！")

    bot.tree.add_command(notify_latest)
