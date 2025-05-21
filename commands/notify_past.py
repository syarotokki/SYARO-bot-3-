from discord import app_commands
import discord
import json
from utils.youtube import fetch_past_videos

OWNER_ID = 1105948117624434728

def setup_notify_past(bot):
    @app_commands.command(name="notify_past", description="過去の動画を通知（開発者限定）")
    async def notify_past(interaction: discord.Interaction):
        if interaction.user.id != OWNER_ID:
            await interaction.response.send_message("このコマンドは開発者のみ使用できます。", ephemeral=True)
            return

        await interaction.response.send_message("過去動画の通知を開始します...", ephemeral=True)

        with open("config.json", "r") as f:
            config = json.load(f)

        for guild_id, data in config.items():
            channel = bot.get_channel(data["channel_id"])
            videos = fetch_past_videos(data["youtube_channel_id"])
            if not videos:
                continue
            # 古い順に並び替えてから送信
            for v in videos:
                await channel.send(v)

        await interaction.edit_original_response(content="過去動画の通知を送信しました！")

    bot.tree.add_command(notify_past)

