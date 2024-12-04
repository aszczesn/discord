import discord
from config.logger_config import setup_logger
from discord.ext import commands
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

if not DISCORD_BOT_TOKEN:
    raise ValueError("DISCORD_BOT_TOKEN is not set in the environment variables")

# Logger setup
logger = setup_logger("todoPrezesy")

# Bot setup
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# Import commands
from commands.tasks import add_task, list_tasks, complete_task
bot.add_command(add_task)
bot.add_command(list_tasks)
bot.add_command(complete_task)


# Events
@bot.event
async def on_ready():
    logger.info(f"{bot.user} is ready and running!")

# Run the bot
bot.run(DISCORD_BOT_TOKEN)