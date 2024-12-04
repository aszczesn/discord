# main.py
from logger_config import setup_logger
from dotenv import load_dotenv
import os
import discord
from discord.ext import commands
import json

# Create a logger for your application
logger = setup_logger("todoPrezesy")

load_dotenv()  # Load variables from .env file

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

if not DISCORD_BOT_TOKEN:
    raise ValueError("DISCORD_BOT_TOKEN is not set in the environment variables")

logger.info("Token loaded successfully!")

# Path to the JSON file
TASKS_FILLE = "tasks.json"

def load_tasks():
    try:
        with open(TASKS_FILLE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        logger.error("JSON File not found")
        return {}
    
def save_tasks():
    with open(TASKS_FILLE, "w") as file:
        json.dump(todo_lists, file)

# Intents for bot
intents = discord.Intents.default()
intents.messages = True

# Bot prefix
bot = commands.Bot(command_prefix="!", intents=intents)

# In-memory task storage, loaded from file
todo_lists = load_tasks()

@bot.event
async def on_ready():
    logger.info(f"{bot.user} biega i kika!")

# Command to add a task
@bot.command(name="dodaj")
async def add_task(ctx, *, task):
    user = ctx.author.id
    if user not in todo_lists:
        todo_lists[user] = []
    todo_lists[user].append({"task": task, "completed_by": None, "compleded_at": None})
    save_tasks()
    await ctx.send(f"Dodano zadanie: {task}")

# Commands to list tasks
@bot.command(name="poka")
async def list_tasks(ctx):
    user = ctx.author.id
    if user not in todo_lists or len(todo_lists[user]) == 0:
        await ctx.send("Nie masz nic do roboty!")
    else:
        tasks = "\n".join([f'{idx + 1}. {task}' for idx, task in enumerate(todo_lists[user])])
        await ctx.send(f"No to zasuwaj:\n{tasks}")

# Command to mark a task as completed
@bot.command(name="zrobione")
async def complete_task(ctx, task_number: int):
    user = ctx.author.id
    if user not in todo_lists or len(todo_lists[user]) < task_number or task_number <= 0:
        await ctx.send("A o co chodzi?")
    else:
        completed_task = todo_lists[user].pop(task_number - 1)
        completed_task["completed_by"] = ctx.author.name
        completed_task["completed_at"] = str(ctx.message.created_at)
        save_tasks()
        await ctx.send(f"Zrobione: {completed_task['task']}")

# Run the bot
bot.run(DISCORD_BOT_TOKEN)