# luiobot
The best bot.

# Installation Instructions
## Windows (x64)
Open command prompt and...<br>
Step 1. Install git using `winget`
```console
winget install git
```
Step 2. Git clone this repository
```console
mkdir luio
cd luio
git clone https://github.com/trendsolate/Hexabot.git .
```
Step 3. Run this command to make the directory structure
```
mkdir db
cd db
type nul > serversettings.sqlite3
type nul > economy.sqlite3
type nul > warns.sqlite3
cd ..
```

# Running the bot
## Windows
Run this command.<br>
```console
python bot.py
```
Make sure you have Python installed.<br>
## Linux and macOS
```console
python3 bot.py
```
Make sure you have Python installed <br>
