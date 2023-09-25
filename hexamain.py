import discord, time, platform, asyncio, os, TOKEN, json, requests
from discord import app_commands
from discord.ext import commands, tasks
from itertools import cycle
from colorama import Back, Fore, Style
from TOKEN import TOKEN
from config import PREFIX, color, footertext, devs, helpMenu

intents = discord.Intents.all()
intents.message_content = True

def saveHasTicket(data):
    filename = "user_tickets.json"
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

def loadHasTicket():
    filename = "user_tickets.json"
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"users_with_tickets": {}}

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
    args = ctx.message.content.split()
    if len(args) < 2:
        await ctx.send('Specify a help menu category to view, `mod` for Moderation and Administration, or `gen` for General Commands or `utility` for Utility Commands or `fun` for fun commands.')
    else:
        menu = args[1]
        if menu == 'all':
            embed = discord.Embed(title='All commands', description=helpMenu.all, color=discord.Color(color))
            await ctx.send(embed=embed)
        elif menu == 'mod':
            embed = discord.Embed(title='Moderation and Administration', description=helpMenu.mod, color=discord.Color(color))
            await ctx.send(embed=embed)
        elif menu == 'gen':
            embed = discord.Embed(title='General', description=helpMenu.gen, color=discord.Color(color))
            await ctx.send(embed=embed)
        elif menu == 'utility':
            embed = discord.Embed(title="Utility", description=helpMenu.utils, color=discord.Color(color))
            await ctx.send(embed=embed)
        elif menu == 'fun':
            embed = discord.Embed(title="Fun", description=helpMenu.fun, color=discord.Color(color))
            await ctx.send(embed=embed)
        elif menu == 'dev':
            if ctx.author.id not in devs:
                await ctx.send('Invalid category.')
            else:
                embed = discord.Embed(title="Developer-Only", description=helpMenu.dev, color=discord.Color(color))
                await ctx.send(embed=embed)
        else:
            await ctx.send('Invalid category.')

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
I'm Hexa, Your All-in-one moderator bot, I'll keep your server clean of spammers and make sure people follow the rules.

Important links:
[Invite link](<https://discord.gg/6g6862qDnn>)
[Bot website](<https://example.com>)

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
    embed.set_footer(icon_url='https://images-ext-1.discordapp.net/external/GqUszJ95QLfyR6y9lIRQsiXgd8JDQhC_7PDnmYo_oa4/%3Fsize%3D1024/https/cdn.discordapp.com/icons/1134337027278643333/d16fa877a398f2f2071fb04c4a4d8f2c.png', text="Made by The HEX Network")
    await ctx.send(embed=embed)

@client.command()
async def purge(ctx):
    if len(ctx.message.content.split()) < 2:
        await ctx.send('Specify an amount of messages to purge.')
    else:
        args = ctx.message.content.split()
        amount = args[1]
        if int(amount) < int(-1):
            await ctx.send("Specify a valid amount of messages to delete.")
            return
        elif int(amount) > 500:
            await ctx.send(f"{amount} is greater than the limit of 500.")
        else:
            if ctx.author.guild_permissions.manage_messages:
                try:
                    amount = int(amount)
                    await ctx.channel.purge(limit=amount + 1)
                    await ctx.send(f"Purged {amount} messages", delete_after=1)
                except discord.errors.Forbidden:
                    await ctx.send('Error occurred and the command could not be executed.')
            else:
                await ctx.send("You do not have the `manage_messages` permission required to run this command.")
                return

@client.command()
async def eval(ctx):
    if ctx.author.id not in devs:
        await ctx.send("Developer command only")
        return
    else:
        evalCMD = ctx.message.content[len(f"{PREFIX}eval "):]
        if evalCMD == '':
            await ctx.send("add some code bro")
            return
        else:
            try:
                result = exec(evalCMD)
                embed = discord.Embed(
                    title="Result of code",
                    description=f'```\n{result}\n```',
                color=discord.Color(color)
                )
                await ctx.send(embed=embed)
            except Exception as e:
                await ctx.send(f'An error occurred {e}')

@client.command()
async def serverinfo(ctx):
        guild = ctx.guild
        # Gets emojis as formatted
        emojis = ", ".join([str(emoji) for emoji in guild.emojis])

        # Gets roles as formatted
        roles = ", ".join([role.mention for role in guild.roles])
        embed = discord.Embed(
            title="Server Information",
            description=f"""
```Main Info```
Guild is {guild}
Server ID - {guild.id}
Server Name - {guild.name}
Server Description - {guild.description}
```Other```
Server Member Count - {str(guild.member_count)}
Server Boost Count - {int(guild.premium_subscription_count)}
Server Boost Level - {guild.premium_tier}
""",
color=discord.Color(color),
    )
        embed.set_thumbnail(url=f"{guild.icon}")
        embed.set_footer(text=footertext)
        await ctx.send(embed=embed)

@client.command()
async def userinfo(ctx):
    user_mentions = ctx.message.mentions  # Get mentioned users

    if len(user_mentions) == 0:
        user = ctx.author
    else:
        user = user_mentions[0]  # Consider only the first mentioned user
    is_bot = "Yes" if user.bot else "No"
    embed = discord.Embed(
        title="User Information",
        description=f"""
Is Bot?: {is_bot}
User Mention: <@{user.id}>
User Name: {user.name}#{user.discriminator}
User ID: {user.id}
Display Name: {user.display_name}
""",
        color=discord.Color(color),
    )
    embed.set_footer(text=footertext)
    embed.set_thumbnail(url=user.avatar)

    await ctx.send(embed=embed)

@client.command()
async def ticket(ctx):
    args = ctx.message.content.split()
    if len(args) < 2:
        await ctx.send(f"Usage: {PREFIX}ticket add / remove")
        return

    if args[1] == 'add':
        author_id = ctx.author.id
        user_data = loadHasTicket()

        if user_data["users_with_tickets"].get(str(author_id)):  # Convert author_id to string
            await ctx.send("You already have a ticket.")
        else:
            user_data["users_with_tickets"][str(author_id)] = True  # Store True
            saveHasTicket(user_data)
            await ctx.send("Ticket created.")
            guild = ctx.guild
            await guild.create_text_channel(f"ticket-{ctx.author.name}")

    elif args[1] == 'remove':
        author_id = ctx.author.id
        user_data = loadHasTicket()

        author_id_int = int(author_id)  # Convert author_id to an integer

        if user_data["users_with_tickets"].get(str(author_id_int)):  # Convert author_id_int to string
            user_data["users_with_tickets"].pop(str(author_id_int))
            saveHasTicket(user_data)

            # Find the channel associated with the user's ticket
            for channel in ctx.guild.channels:
                if channel.name.startswith(f"ticket-{ctx.author.name}"):
                    try:
                        await channel.delete()
                        await channel.send("Ticket removed.")
                        await ctx.message.delete()
                        return
                    except discord.errors.NotFound:
                        print("Ticket channel not found.")
            await ctx.send("Ticket removed.")
        else:
            await ctx.send("You don't have a ticket to remove.")

    else:
        await ctx.send("Invalid option.")

@client.command()
async def dog(ctx):
    url = "https://dog.ceo/api/breeds/image/random"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        image_url = data["message"]
        embed = discord.Embed(title="A dog for you!", color=discord.Color(color))
        embed.set_image(url=image_url)
        await ctx.send(embed=embed)
    else:
        await ctx.send(f"Error Code: {response.status_code}")

@client.command()
async def cat(ctx):
    url = "https://api.thecatapi.com/v1/images/search"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()[0]
        image_url = data["url"]
        embed = discord.Embed(title="A cat for you!", color=discord.Color(color))
        embed.set_image(url=image_url)
        await ctx.send(embed=embed)
    else:
        await ctx.send(f"Error code: {response.status_code}")


# Define your loadHasTicket and saveHasTicket functions here
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
        # Send an invite tracker message in the specified channel
        invite_tracker_channel = member.guild.get_channel(1143147859789754440)
        if invite_tracker_channel:
            await invite_tracker_channel.send(f"{member.mention} was invited by {inviter.display_name}.")

        # Send a welcome message with a banner in the specified channel
        welcome_channel = member.guild.get_channel(1154658357119041596)
        if welcome_channel:
            # banner code
            welcome_banner = discord.File("hexbanner.hexbanner.png")
            welcome_embed = discord.Embed(
                title=f"Welcome to our network, {member.mention}!, you did the best thing you've ever done now",
                description=f"You were invited by {inviter.display_name}.",
                color=0x00ff00
            )
            welcome_embed.set_thumbnail(url=member.avatar)
            await welcome_channel.send(embed=welcome_embed, file=welcome_banner)
    else:
        print(f"Couldn't find the invite code for {member.mention}")
# Do not add commands here, add commands above this part (above On member join)

# Run the bot using the provided token
client.run(TOKEN)