import datetime

PREFIX = "?";
# Main HexaBot:
#TOKEN = 'MTE0ODQyNjg0MzIyMTkyNjAwOA.GswHe_.5be2ISJmRygY0Q3NrrcyyyXeLY1pJaO6NPHfjQ'
# Hexa Test:
TOKEN = "MTE3MDc2MzEyNDA3NzQ5ODUyMA.Gxfb3z.Po34kFvOaSUQjSeSMAr2y8hGGDnd8N8coKpTno";
devs = [
    1044817642143371364,  # noerlol
    1095310535140057109,  # trendsolate
    885036358467481601,  # sexy sanskrit guy (rachil)
    1126175772546175036,  # crystal
    587204069408636929  # exotic.js
]
#   825330059887509536, bunkyeister
#   805817228498436099, admi
#   739548321336787247, V1nSmoker
color: int = int("AF27E4", 16)
status_url: str = "https://xnoerplayscodes.github.io/luiobot/status.txt";
manage_messages_error_msg: str = "You must have the `MANAGE_MESSAGES` permission to run this command.";
# Functions
def log(x):
    print(x);
def footertext(embedvariable):
    embedvariable.set_footer(text="Luioverse", icon_url='https://i.imgur.com/Y98MWQW.png')
    #  Imgur image for Server PFP
def to_utc(epoch_timestamp):
    utc_datetime = datetime.datetime.utcfromtimestamp(epoch_timestamp)
    utc_time_24h = utc_datetime.strftime('%Y-%m-%d %H:%M:%S');
    return utc_time_24h;
def makeWarnID(number: int):
    base36 = ""
    chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    while number > 0:
        number, remainder = divmod(number, 36)
        base36 = chars[remainder] + base36

    return base36

# ---------
# Help Menu
args_help: str = "```\n[] - Optional Argument\n() - Required Argument\n```";
class helpMenu:
    mod: str = f"""
{args_help}
**{PREFIX}verify_setup**
Sets up verification system

**{PREFIX}ban (@user)**
Bans specified user

**{PREFIX}kick (@user)**
Kicks specified user

**{PREFIX}purge (amount)**
Purges specified amount of messages
"""
    gen: str = f"""
{args_help}
**{PREFIX}help**
Returns help menu.

**{PREFIX}ping**
Returns client latency

**{PREFIX}about**
Returns information about the bot
"""
    utils: str = f"""
{args_help}
**{PREFIX}serverinfo**
Returns information of server

**{PREFIX}userinfo [@user]**
Returns user information about user mentioned or message author depending on who is pinged

**{PREFIX}ticket (action)**
Creates / Removes ticket based on provided in `(action)`, valid are `remove` and `add`
"""
    fun: str = f"""
.none
"""
    dev: str = f"""
{args_help}
**{PREFIX}eval (code)**
Evaluates and Runs code, in simpler words, run code which you give.

// More Coming Soon
"""
# ---------
