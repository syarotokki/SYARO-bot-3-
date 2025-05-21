from discord import app_commands
import discord
import json

def setup_subscribe(bot):
    @app_commands.command(name="subscribe", description="通知先チャンネルとYouTubeチャンネルIDを設定する")
    @app_commands.describe(channel="通知先チャンネル", youtube_channel_id="YouTubeチャンネルのID")
    async def subscribe(interaction: discord.Interaction, channel: discord.TextChannel, youtube_channel_id: str):
        with open("config.json", "r") as f:
            config = json.load(f)
        config[str(interaction.guild.id)] = {"channel_id": channel.id, "youtube_channel_id": youtube_channel_id}
        with open("config.json", "w") as f:
            json.dump(config, f, indent=2)
        await interaction.response.send_message("登録が完了しました！", ephemeral=True)

    bot.tree.add_command(subscribe)
