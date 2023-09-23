import discord, time, platform, asyncio, os, TOKEN
from discord import app_commands
from discord.ext import commands, tasks
from itertools import cycle
from colorama import Back, Fore, Style
from TOKEN import TOKEN
from config import PREFIX, color, footertext

intents = discord.Intents.all()
intents.message_content = True

# Change prefix in config.py
client = commands.Bot(command_prefix=PREFIX , intents=intents, help_command=None) # Help command is custom
bot_status = cycle([f"Made by Trendsolate", "From The HEX Network", f"Ready to help '{PREFIX}'", "Reading a book", "Waiting for requests", "Playing Fortnite"])

# Continuously changes presence activity every 30 seconds to the ones in bot_status
@tasks.loop(seconds=30)
async def change_status():
    await client.change_presence(activity=discord.Game(next(bot_status)))

#
@client.event
async def on_ready():
    # this runs when the account is logged into.
    prfx = (Back.BLACK + Fore.GREEN + time.strftime("%H:%M:%S UTC", time.gmtime()) + Back.RESET + Fore.WHITE + Style.BRIGHT)
    print(Fore.GREEN + f"🚀 Logged in as {client.user} | HexaBot" + Style.RESET_ALL)
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
```General```
**{PREFIX}help**
Returns help menu.

**{PREFIX}ping**
Returns client latency

**{PREFIX}about**
Returns information about the bot
```Moderation and Administration```
**{PREFIX}verify_setup**
Sets up verification system

**{PREFIX}ban @user**
Bans specified user

**{PREFIX}kick @user**
Kicks specified user
''',
    color=discord.Color(color)
    )
    helpmenu.set_footer(text=f'Run by {ctx.author.name} | HexaBot')
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

@client.command()
async def ban(ctx, *args):
    if ctx.author.guild_permissions.ban_members:
        args = ctx.message.content.split()
        if len(args) < 2:
            await ctx.send(f'Usage: {PREFIX}ban @user')
            return

        user_id = args[1].strip('<@!>')
        try:
            member = await ctx.guild.fetch_member(int(user_id))
            if member:
                try:
                    await member.ban()
                    embed = discord.Embed(
                        description=f"<@{user_id}> ({member.display_name}) has been **banned** from the server.",
                    color=discord.Color(color)
                    )
                    embed.set_footer(text=f'Run by {ctx.author.name} | {footertext}')
                    await ctx.send(embed=embed)
                except discord.Forbidden:
                    await ctx.send("An error occurred and I couldn't ban the specified user at this time.")
            else:
                await channel.send("Not a valid user.")
                return
        except discord.NotFound:
            await ctx.send('Not a valid user')
    else:
        await ctx.send("You don't have permission to ban members as you need **ban members** permission.")

@client.command()
async def kick(ctx, *args):
    if ctx.author.guild_permissions.kick_members:
        args = ctx.message.content.split()
        if len(args) < 2:
            await ctx.send(f'Usage: {PREFIX}kick @user')
            return

        user_id = args[1].strip('<@!>')
        try:
            member = await ctx.guild.fetch_member(int(user_id))
            if member:
                try:
                    await member.kick()
                    embed = discord.Embed(
                        description=f"<@{user_id}> ({member.display_name}) has been **kicked** from the server.",
                    color=discord.Color(color)
                    )
                    embed.set_footer(text=f'Run by {ctx.author.name} | {footertext}')
                    await ctx.send(embed=embed)
                except discord.Forbidden:
                    await ctx.send("An error occurred and I couldn't kick the specified user at this time.")
            else:
                await ctx.send('Not a valid user.')
        except discord.NotFound:
            await ctx.send("Not a valid user.")
    else:
        await ctx.send("You don't have permission to kick members as you need **kick members** permission.")

@client.command()
async def about(ctx):
    embed = discord.Embed(
        title="About the bot",
        description="""
All-in-one moderation and utilities bot. Invite me today to make your server safer.

Important links:
[Invite link](<https://pornhub.com>)
[Bot website](<https://pornhub.com>)

Developers:

Team Leader:
Trendsolate

Lead Developers:
noerlol
Admi

Development Team:
Bunkiyiester
Crystal
ex6tic.js
rahil_salecha
""",
    color=discord.Color(color)
    )
    embed.set_footer(icon_url='https://i.imgur.com/i6gXIin.png', text="Made with Pycord")
    await ctx.send(embed=embed)
# When person joins, do... (invite tracker)
@client.event
async def on_member_join(member):
    # Check if the member was invited and get the invite code
    invite_code = None
    for invite in await member.guild.invites():
        if invite.uses > 1:
            invite_code = invite

    if invite_code:
        inviter = invite_code.inviter
        # Send a welcome message to the new member
        welcome_channel = member.guild.get_channel(1154658357119041596)
        if welcome_channel:
            await welcome_channel.send(f'Welcome to our Network, {member.mention}! You were invited by {inviter.mention}.')
    else:
        print(f"Couldn't find the invite code for {member.display_name}")

# Do not add commands here, add commands above this part (above On member join)

# Run the bot using the provided token
client.run(TOKEN)