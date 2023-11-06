import datetime

import aiosqlite as sql
import discord as dc
import colorama as clr
import itertools as it
import datetime as dt
import os, asyncio, requests
from discord.ext import commands, tasks
# Config
from config import *
intents = dc.Intents.default();
intents.message_content = True;
bot = commands.Bot(help_command=None, command_prefix=PREFIX, intents=intents);

if os.name == "posix":
    linux: bool = True;
elif os.name == "nt":
    linux: bool = False;
bot_statuses = it.cycle(["Made by Luio Development", f"My Prefix is {PREFIX}"]);
@tasks.loop(seconds=30)
async def change_status():
    await bot.change_presence(activity=dc.Game(next(bot_statuses)));

@bot.event
async def on_ready():
    print("------------------------ (Bot Logon Info)");
    print(f"Intents (MessageContent): {intents.message_content}\nPREFIX: {PREFIX}\nBot User: {bot.user}");
    print(clr.Fore.YELLOW + "Attempting connection to databases..." + clr.Style.RESET_ALL);
    try:
        global warnsdb;
        warnsdb = await sql.connect(os.path.join("db", "warns.sqlite3"));
        global genconf;
        genconf = await sql.connect(os.path.join("db", "genconf.sqlite3"));
        print(clr.Fore.GREEN + "Connection successful to 2/2 databases." + clr.Style.RESET_ALL);
    except Exception:
        print(clr.Fore.RED + "Connection refused." + clr.Style.RESET_ALL);
        # hewwo, hru?
    print(clr.Fore.GREEN + "ALL_SERVICES_OPERATIONAL" + clr.Style.RESET_ALL);

# .addwarn-config
async def addwarn(ctx, reason, user, guild):
    async with warnsdb.cursor() as cursor:
        warnid = makeWarnID(user.id * int(dt.datetime.now().timestamp()));
        await cursor.execute("INSERT INTO warns(user, reason, server, time, warnid) VALUES (?, ?, ?, ?, ?)", (user.id, reason, guild.id, int(dt.datetime.now().timestamp()), warnid));
    await warnsdb.commit();
    return warnid;
# .addwarn-config-end

# .gen
@bot.command()
async def ping(ctx):
    og_msg = await ctx.send(f"Pinging...")
    await asyncio.sleep(1)
    await og_msg.edit(content=f"Pong! {round(bot.latency * 1000)}ms")
@bot.command()
async def help(ctx):
    args = ctx.message.content.split();
    if len(args) < 2:
        await ctx.send(f"Usage: {PREFIX}help [category] *or `-c` to view all categories*")
    menu = args[1];

    if menu == '-c':
        embed = dc.Embed(title="All Categories", description="`mod`, `gen`, `utility` and `fun`", color=dc.Color(color));
        footertext(embed);
        await ctx.send(embed=embed)
    elif menu == 'mod':
        embed = dc.Embed(title='Moderation and Administration', description=helpMenu.mod, color=dc.Color(color))
        await ctx.send(embed=embed)
    elif menu == 'gen':
        embed = dc.Embed(title='General', description=helpMenu.gen, color=dc.Color(color))
        await ctx.send(embed=embed)
    elif menu == 'utility':
        embed = dc.Embed(title="Utility", description=helpMenu.utils, color=dc.Color(color))
        await ctx.send(embed=embed)
    elif menu == 'fun':
        embed = dc.Embed(title="Fun", description=helpMenu.fun, color=dc.Color(color))
        await ctx.send(embed=embed)
    elif menu == 'dev':
        if ctx.author.id not in devs:
            await ctx.send('Invalid category.')
        else:
            embed = dc.Embed(title="Developer-Only", description=helpMenu.dev, color=dc.Color(color))
            await ctx.send(embed=embed)
    else:
        await ctx.send('Invalid category')
@bot.command()
async def status(ctx):
    ogmsg = await ctx.send("Fetching status..");
    data = requests.get(status_url);
    if data.status_code == 200:
        embed = dc.Embed(title="Status of Luio Services", description=f"```\n{data.text}\n```", color=dc.Color(color));
        footertext(embed);
        await ogmsg.edit(content=None, embed=embed);
    else:
        await ogmsg.edit(content="Error while fetching status.");

# .gen-end
# .moderator
@bot.command()
async def ban(ctx, member: dc.Member):
    if ctx.author.guild_permissions.ban_members:
        args = ctx.message.content.split()
        if len(args) < 2:
            await ctx.send(f'Usage: {PREFIX}ban @user')
            return
        try:
            if member:
                try:
                    await member.ban()
                    embed = dc.Embed(
                        description=f"<@{member.id}> ({member.display_name}) has been **banned** from the server.",
                        color=dc.Color(color)
                    )
                    embed.set_footer(text=f'Run by {ctx.author.name} | Luio Development')
                    await ctx.send(embed=embed)
                except dc.Forbidden:
                    await ctx.send("An error occurred and I couldn't ban the specified user at this time.")
            else:
                await ctx.send("Not a valid user.")
                return
        except dc.NotFound:
            await ctx.send('Not a valid user')
    else:
        await ctx.send("You don't have permission to ban members as you need **ban members** permission.")

@bot.command()
async def kick(ctx, member: dc.Member):
    if ctx.author.guild_permissions.kick_members:
        args = ctx.message.content.split()
        if len(args) < 2:
            await ctx.send(f'Usage: {PREFIX}kick @user')
            return
        try:
            if member:
                try:
                    await member.kick()
                    embed = dc.Embed(
                        description=f"<@{member.id}> ({member.display_name}) has been **kicked** from the server.",
                        color=dc.Color(color)
                    )
                    embed.set_footer(text=f'Run by {ctx.author.name} | Luio Development')
                    await ctx.send(embed=embed)
                except dc.Forbidden:
                    await ctx.send("An error occurred and I couldn't kick the specified user at this time.")
            else:
                await ctx.send('Not a valid user.')
        except dc.NotFound:
            await ctx.send("Not a valid user.")
    else:
        await ctx.send("You don't have permission to kick members as you need **kick members** permission.")
@bot.command()
async def slowmode(ctx):
    args = ctx.message.content.split()
    if len(args) != 2:
        await ctx.send(f"Usage: {PREFIX}slowmode (duration) or `--reset` to reset slowmode to **0**.")
        return
    else:
        if ctx.author.guild_permissions.manage_messages:
            try:
                duration = args[1]
                if str(duration) == '--reset':
                    await ctx.channel.edit(slowmode_delay=0)
                    await ctx.send(f'Reset slowmode.')
                else:
                    if int(duration) > 21600 or int(duration) < 1:
                        await ctx.send("Maximum 6 hours (21600 seconds) or 1 second")
                        return
                    await ctx.channel.edit(slowmode_delay=int(duration))
                    await ctx.send(f'Set slowmode to {str(duration)} second')
            except ValueError:
                await ctx.send("Invalid duration, must be in seconds, without the `s`.")
        else:
            await ctx.send("Not enough permissions, must have `manage_messages`.")
@bot.command()
async def warn(ctx, member: dc.Member, *, reason: str = "No reason provided."):
    if not ctx.author.guild_permissions.manage_messages:
        await ctx.send(manage_messages_error_msg);
        return;
    warnid = await addwarn(ctx, reason, member, ctx.guild);
    embed = dc.Embed(title=f"Warned {member.display_name}",
                          description=f"Warned {member.mention} for reason `{reason}` and warn id `{warnid}`.",
                          color=dc.Color(color))
    embed.set_footer(text=f"Moderator: {ctx.author.display_name}", icon_url=ctx.author.avatar)
    await ctx.send(embed=embed)
    memberembed = dc.Embed(description=f"You have been warned in **{ctx.guild.name}** || **Reason:** {reason}",
                           color=dc.Color(color))
    await member.send(embed=memberembed)
@bot.command()
async def warnings(ctx, member: dc.Member):
    async with warnsdb.cursor() as c:
        await c.execute(f"SELECT reason, server FROM warns WHERE user = {member.id} AND server = {ctx.guild.id}");
        global data;
        data = await c.fetchall();
    if not ctx.author.guild_permissions.manage_messages:
        await ctx.send(manage_messages_error_msg);
        return;

    if not data:
        myass = dc.Embed(title=f"Warnings for {member.display_name}",
                         description=f"No warnings found for {member.mention}", color=dc.Color(color))
        myass.set_footer(text=f"Moderator: {ctx.author.display_name}", icon_url=ctx.author.avatar)
        await ctx.send(embed=myass);
        return;
    fdata = '';
    for item in data:
        warn = ''
        for thing in item:
            if isinstance(thing, int):
                continue;
            else:
                warn += f'{thing}';

        # Append the formatted string to 'fdata' with a newline character
        fdata += f'{warn}\n\n'

    total_warnings = len(data)
    embed = dc.Embed(title=f"Warnings for {member.display_name}", description=f"""
Total User Warnings: {total_warnings}
**Reason Only**
{fdata}
""", color=dc.Color(color))
    embed.set_footer(text=f"Moderator: {ctx.author.display_name}", icon_url=ctx.author.avatar)
    await ctx.send(embed=embed)

@bot.command()
async def clearwarns(ctx, member: dc.Member):
    if not ctx.author.guild_permissions.manage_guild:
        await ctx.send(manage_messages_error_msg);
    async with warnsdb.cursor() as cursor:
        await cursor.execute(f"SELECT reason FROM warns WHERE user = {member.id} AND server = {ctx.guild.id}");
        data = await cursor.fetchall()
    if data:
        await ctx.send(f"Cleared {len(data)} warnings from {member.mention}")
        async with warnsdb.cursor() as cursor:
            await cursor.execute(f"DELETE FROM warns WHERE user = {member.id} AND server = {ctx.guild.id}");
    if not data:
        await ctx.send("User has no warnings.");

@bot.command()
async def purge(ctx):
    args = ctx.message.content.split()
    if len(args) < 2:
        await ctx.send(f"Usage: {PREFIX}purge (amount of messages)")
    else:
        amount = args[1]
        if int(amount) < -1:
            await ctx.send("Provide a valid number of messages to delete.")
        elif int(amount) > 500:
            await ctx.send("Cannot exceed 500")
        else:
            if ctx.author.guild_permissions.manage_messages:
                try:
                    amount = int(amount)
                    await ctx.channel.purge(limit=amount + 1)
                    await ctx.send(f"Purged {amount} messages", delete_after=1)
                except dc.errors.Forbidden:
                    await ctx.send("Error.", delete_after=2)
            else:
                await ctx.send(f"You do not have `MANAGE_MESSAGES`.")
# .moderator-end
bot.run(TOKEN);