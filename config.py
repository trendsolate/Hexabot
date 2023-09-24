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
]

footertext = f'Hexabot - The HEX Network'

class helpMenu:
    all = f'''
```Argument help:
[] means optional
() means required
```

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

**{PREFIX}ban (@user)**
Bans specified user

**{PREFIX}kick (@user)**
Kicks specified user

**{PREFIX}purge (amount)**
Purges specified amount of messages
```Utility```
**{PREFIX}serverinfo**
Returns information of server

**{PREFIX}userinfo [@user]**
Returns user information about user mentioned or message author depending on who is pinged
'''

    mod = f'''
```Argument help:
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
```Argument help:
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
```Argument help:
[] means optional
() means required
```
**{PREFIX}serverinfo**
Returns information of server

**{PREFIX}userinfo [@user]**
Returns user information about user mentioned or message author depending on who is pinged
'''
