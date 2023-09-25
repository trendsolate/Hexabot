PREFIX = '?'
color = int('2383D0', 16)
devs = [
    1044817642143371364, # noerlol
    1095310535140057109, # trendsolate
    885036358467481601, # sexy sanskrit guy (rachil)
    825330059887509536, # bunkyeister
    805817228498436099, # admi
    1126175772546175036, # crystal
    587204069408636929, # exotic.js
    739548321336787247, # V1nSmoker
]

footertext = f'Hexabot - The HEX Network'

class helpMenu:
    all = f'''
Hey friend! All commands is getting phased out in favour of a more organized, shortner and concise, categorized help menu. Run `{PREFIX}help (category)` to see the specific category commands!
'''

    mod = f'''
```
[] means optional
() means required
```
**{PREFIX}verify_setup**
Sets up verification system

**{PREFIX}ban @user**
Bans specified user

**{PREFIX}kick @user**
Kicks specified user

**{PREFIX}purge (amount)**
Purges specified amount of messages
'''

    gen = f'''
```
[] means optional
() means required
```
**{PREFIX}help**
Returns help menu.

**{PREFIX}ping**
Returns client latency

**{PREFIX}about**
Returns information about the bot
'''

    utils = f'''
```
[] means optional
() means required
```
**{PREFIX}serverinfo**
Returns information of server

**{PREFIX}userinfo [@user]**
Returns user information about user mentioned or message author depending on who is pinged

**{PREFIX}ticket (action)**
Creates / Removes ticket based on provided in `(action)`, valid are `remove` and `add`.
'''

    fun = f'''
```
[] means optional
() means required
```
**{PREFIX}dog**
Returns random dog image

**{PREFIX}cat**
Returns random cat image
'''
    dev = f'''
```
[] means optional
() means required
```
**{PREFIX}eval [code]**
Evaluates and Runs code, in simpler words, run code which you give.

***More probably not coming soon but sure I guess***
'''
