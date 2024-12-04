import os
import discord
from discord.ext import commands

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# Intents for bot
intents = discord.Intents.default()
intents.messages = True

# Bot prefix
bot = commands.Bot(command_prefix="!", intents=intents)

# In-memory task storage
todo_lists = {}

@bot.event
async def on_ready():
    print(f"{bot.user} biega i kika!")

# Command to add a task
@bot.command(name="dodaj")
async def add_task(ctx, *, task):
    user = ctx.author.id
    if user not in todo_lists:
        todo_lists[user] = []
    todo_lists[user].append(task)
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
        todo_lists[user].pop(task_number - 1)
        await ctx.send(f"Zrobione: {complete_task}")

# Run the bot
bot.run(DISCORD_BOT_TOKEN)