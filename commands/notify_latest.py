from discord import app_commands
import discord
import json
from utils.youtube import fetch_latest_video

OWNER_ID = 1105948117624434728

def setup_notify_latest(bot):
    @app_commands.command(name="notify_latest", description="最新の動画またはライブ配信を通知（開発者限定）")
    async def notify_latest(interaction: discord.Interaction):
        if interaction.user.id != OWNER_ID:
            await interaction.response.send_message("このコマンドは開発者のみ使用できます。", ephemeral=True)
            return

        await interaction.response.send_message("最新動画の通知を開始します...", ephemeral=True)

        guild_id = str(interaction.guild_id)

        with open("config.json", "r") as f:
            config = json.load(f)

        if guild_id not in config:
            await interaction.edit_original_response(content="このサーバーには設定が登録されていません。")
            return

        data = config[guild_id]
        channel = bot.get_channel(data["channel_id"])
        video_info = fetch_latest_video(data["youtube_channel_id"])

        if not video_info:
            await interaction.edit_original_response(content="最新動画が見つかりませんでした。")
            return

        # 通知文の分岐
        if video_info["is_live"]:
            msg = f"🔴 ライブ配信が始まりました！\n{video_info['url']}\n開始時刻：{video_info['published_at']}"
        else:
            msg = f"📺 新しい動画が公開されました！\n{video_info['url']}"

        await channel.send(msg)
        await interaction.edit_original_response(content="最新の動画通知を送信しました！")

    bot.tree.add_command(notify_latest)

            await channel.send(message)

        await interaction.edit_original_response(content="最新動画の通知を送信しました！")

    # 重複防止のため既存コマンドを削除
    existing = bot.tree.get_command("notify_latest")
    if existing:
        bot.tree.remove_command("notify_latest")

    bot.tree.add_command(notify_latest)
