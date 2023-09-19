import discord
from discord import app_commands
from discord.ext import commands, tasks 
from itertools import cycle
from colorama import Back, Fore, Style
import time
import platform

import os 
import TOKEN
from TOKEN import TOKEN

intents = discord.Intents.all()
intents.message_content = True

client = commands.Bot(command_prefix="?" , intents=discord.Intents.all())

bot_status = cycle(["Made by Trendsolate", "From The HEX Network", "Ready to help '?'", "Reading a book", "Waiting for requests", "Playing Fortnite"])

@tasks.loop(seconds=30)
async def change_status():
    await client.change_presence(activity=discord.Game(next(bot_status)))

@client.event
async def on_ready():
    # this runs when the account is logged into.
    prfx = (Back.BLACK + Fore.GREEN + time.strftime("%H:%M:%S UTC", time.gmtime()) + Back.RESET + Fore.WHITE + Style.BRIGHT)
    print("Hexa at your service and logged in as {0.user}".format(client))
    change_status.start()
    try:
        synced = await client.tree.sync()
        print(f"Synced {len(synced)} command(s)")

    except Exception as e:
        print(e) 
    # this is the code for commands and conversation.
@client.command()
async def hello(ctx):
    await ctx.send("hey wsg!")




client.run(TOKEN)