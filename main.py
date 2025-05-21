from keep_alive import keep_alive
from bot import bot
import os

keep_alive()
bot.run(os.getenv("DISCORD_TOKEN"))