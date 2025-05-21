from discord import app_commands
import discord
from utils.youtube import fetch_latest_video
import json

OWNER_ID = 1105948117624434728

def setup_notify_latest(bot):
    @app_commands.command(name="notify_latest", description="最新の動画またはライブを即時通知（開発者限定）")
    async def notify_latest(interaction: discord.Interaction):
        if interaction.user.id != OWNER_ID:
            await interaction.response.send_message("このコマンドは開発者のみ使用できます。", ephemeral=True)
            return

        await interaction.response.send_message("最新動画の通知を送信中です...", ephemeral=True)

        with open("config.json", "r") as f:
            config = json.load(f)

        for guild_id, data in config.items():
            channel = bot.get_channel(data["channel_id"])
            if not channel:
                continue

            video = fetch_latest_video(data["youtube_channel_id"])
            if not video:
                continue

            if video["is_live"]:
                message = f'🔴 **ライブ配信が始まりました！**\n開始時刻: <t:{video["published_unix"]}:F>\n{video["url"]}'
            else:
                message = f'\n{video["title"]}\n{video["url"]}'

            await channel.send(message)

        await interaction.edit_original_response(content="最新動画の通知を送信しました！")

    # 重複防止のため既存コマンドを削除
    existing = bot.tree.get_command("notify_latest")
    if existing:
        bot.tree.remove_command("notify_latest")

    bot.tree.add_command(notify_latest)
