from discord.ext import commands
import json

TASKS_FILLE = "data/tasks.json"

def load_tasks():
    try:
        with open(TASKS_FILLE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}
    
def save_tasks(todo_lists):
    with open(TASKS_FILLE, "w") as file:
        json.dump(todo_lists, file)

# In-memory task storage, loaded from file
todo_lists = load_tasks()

# Command to add a task
@commands.command(name="dodaj")
async def add_task(ctx, *, task):
    user = ctx.author.id
    if user not in todo_lists:
        todo_lists[user] = []
    todo_lists[user].append({"task": task, "completed_by": None, "compleded_at": None})
    save_tasks(todo_lists)
    await ctx.send(f"Dodano zadanie: {task}")

# Commands to list tasks
@commands.command(name="poka")
async def list_tasks(ctx):
    user = ctx.author.id
    if user not in todo_lists or len(todo_lists[user]) == 0:
        await ctx.send("Nie masz nic do roboty!")
    else:
        tasks = "\n".join([f'{idx + 1}. {task["task"]}' for idx, task in enumerate(todo_lists[user])])
        await ctx.send(f"No to zasuwaj:\n{tasks}")

# Command to mark a task as completed
@commands.command(name="zrobione")
async def complete_task(ctx, task_number: int):
    user = ctx.author.id
    if user not in todo_lists or len(todo_lists[user]) < task_number or task_number <= 0:
        await ctx.send("A o co chodzi?")
    else:
        completed_task = todo_lists[user].pop(task_number - 1)
        completed_task["completed_by"] = ctx.author.name
        completed_task["completed_at"] = str(ctx.message.created_at)
        todo_lists[user].append(completed_task)
        save_tasks(todo_lists)
        await ctx.send(f"Zrobione: {completed_task['task']}")