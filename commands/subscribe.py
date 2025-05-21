from discord import app_commands
import discord
import json

OWNER_ID = 1105948117624434728

def setup_subscribe(bot):
    @app_commands.command(name="subscribe", description="通知先チャンネルとYouTubeチャンネルIDを登録")
    @app_commands.describe(youtube_channel_id="YouTubeのチャンネルID")
    async def subscribe(interaction: discord.Interaction, youtube_channel_id: str):
        if not interaction.channel:
            await interaction.response.send_message("チャンネル情報が取得できませんでした。", ephemeral=True)
            return

        with open("config.json", "r") as f:
            config = json.load(f)

        config[str(interaction.guild_id)] = {
            "channel_id": interaction.channel.id,
            "youtube_channel_id": youtube_channel_id
        }

        with open("config.json", "w") as f:
            json.dump(config, f, indent=4)

        await interaction.response.send_message("登録が完了しました！", ephemeral=True)

    bot.tree.add_command(subscribe)
