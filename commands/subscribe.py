import discord
from discord import app_commands
from discord.ext import commands
import json
import os

CONFIG_FILE = "config.json"

class Subscribe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="subscribe", description="通知先チャンネルとYouTubeチャンネルIDを登録します。")
    async def subscribe(self, interaction: discord.Interaction, youtube_channel_id: str, notify_channel: discord.TextChannel):
        await interaction.response.send_message("登録処理中...", ephemeral=True)

        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as f:
                config = json.load(f)
        else:
            config = {}

        config[str(interaction.guild.id)] = {
            "youtube_channel_id": youtube_channel_id,
            "notify_channel_id": notify_channel.id
        }

        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=4)

        await interaction.edit_original_response(content="登録が完了しました！")

async def setup(bot):
    await bot.add_cog(Subscribe(bot))
