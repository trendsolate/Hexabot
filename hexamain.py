import discord, time, platform, asyncio, os, TOKEN
from discord import app_commands
from discord.ext import commands, tasks
from itertools import cycle
from colorama import Back, Fore, Style
from TOKEN import TOKEN
from config import PREFIX, color, devs

intents = discord.Intents.all()
intents.message_content = True

# Change prefix in config.py
client = commands.Bot(command_prefix=PREFIX , intents=intents, help_command=None) # Help command is custom
bot_status = cycle([f"Made by Trendsolate", "From The HEX Network", f"Ready to help '{PREFIX}'", "Reading a book", "Waiting for requests", "Playing Fortnite"])

# Continuously changes presence activity every 30 seconds to the ones in bot_status
@tasks.loop(seconds=30)
async def change_status():
    await client.change_presence(activity=discord.Game(next(bot_status)))

# When bot is ready and logged in:
@client.event
async def on_ready():
    # this runs when the account is logged into.
    prfx = (Back.BLACK + Fore.GREEN + time.strftime("%H:%M:%S UTC", time.gmtime()) + Back.RESET + Fore.WHITE + Style.BRIGHT)
    print(f"🚀 Logged in as {client.user} | HexaBot")
    change_status.start()
    try:
        synced = await client.tree.sync()
        print(f"Synced {len(synced)} command(s)")

    except Exception as e:
        print(e) 
    client.add_view(Verification())

# This is the code for commands
@client.command()
async def help(ctx):
    helpmenu = discord.Embed(
        title='Help Menu',
        description=f'''
{PREFIX}help - This!
{PREFIX}ping - Returns client latency
{PREFIX}verify_setup - Sets up verification
''',
    color=discord.Color(color)
    )
    helpmenu.set_footer(text='Hexabot | [PLACEHOLDER TEXT]')
    await ctx.send(embed=helpmenu)

@client.command()
async def ping(ctx):
    og_msg = await ctx.send(f"Calculating....")
    await asyncio.sleep(1)
    await og_msg.edit(content=f"Pong! {round(client.latency * 1000)}ms")


# !! DO NOT TOUCH !! THIS IS CODE FOR VERIFICATION

class Verification(discord.ui.View):
    def __init__(self):
        super().__init__(timeout = None)
    @discord.ui.button(label="Verify", custom_id="Verify", style=discord.ButtonStyle.success)
    async def verify(self, interaction, button):
        role = 1144021740331225098
        user = interaction.user
        if role not in [y.id for y in user.roles]:
            await user.add_roles(user.guild.get_role(role))
            await user.send(f"You've been verified in {ctx.guild.name}!")

@client.command()
async def verify_setup(ctx):
    embed = discord.Embed(
        title='Verification',
        description='Use the menu below to verify yourself to get access to the server! 👇✅',
    color=discord.Color(color)
    )
    embed.set_footer(text=f'{ctx.guild.name} • Verification')

    await ctx.send(embed=embed, view=Verification())

# Run the bot using the provided token
client.run(TOKEN)
