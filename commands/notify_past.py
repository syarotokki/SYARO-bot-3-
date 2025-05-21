from discord import app_commands
import discord
from utils.youtube import fetch_past_videos
import json

OWNER_ID = 1105948117624434728

def setup_notify_past(bot):
    @app_commands.command(name="notify_past", description="過去の動画を通知（開発者限定）")
    async def notify_past(interaction: discord.Interaction):
        if interaction.user.id != OWNER_ID:
            await interaction.response.send_message("このコマンドは開発者のみ使用できます。", ephemeral=True)
            return

        await interaction.response.send_message("過去動画の通知を送信中です...", ephemeral=True)

        with open("config.json", "r") as f:
            config = json.load(f)

        for guild_id, data in config.items():
            channel = bot.get_channel(data["channel_id"])
            if not channel:
                continue

            videos = fetch_past_videos(data["youtube_channel_id"])

            # 古い順に送信
            for v in reversed(videos):
                await channel.send(v)

        # ここが正しくインデントされていなかった → 修正済み
        await interaction.edit_original_response(content="過去動画の通知を送信しました！")

    # 既存コマンドがある場合は削除（重複防止）
    existing = bot.tree.get_command("notify_past")
    if existing:
        bot.tree.remove_command("notify_past")

    bot.tree.add_command(notify_past)
