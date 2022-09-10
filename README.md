# Aiogram — Farm-Game bot
[![versions](https://img.shields.io/badge/python-3.9%20%7C%203.10-blue)](https://github.com/gh0sth4ckk/aiogram-farm-bot)
[![license](https://img.shields.io/github/license/gh0sth4ckk/aiogram-fakeperson-bot)](https://github.com/gh0sth4ckk/aiogram-farm-bot/blob/main/LICENSE)

Small farm mini-game. Implemented such things as:
* Level system
* Buying and selling resources and animals
* Buying buildings

Accordingly, there is also a database, sqlite (There is a dump in the models / dump.sql folder).

# Installation
0. Requires Python 3.9+
1. Git clone project into directory:
```shell
git clone https://github.com/gh0sth4ckk/aiogram-farm-bot.git
```
2. Install all requirements:
```shell
pip install -r requirements.txt
```
3. Get personal bot token from @BotFather in telegram and past him into .env file instead of "YOURTOKEN":
```env
BOT_TOKEN=<past token here>
```
4. Start `bot.py` file and send `/start` command
# Commands
`/start` - Start game \
`/help` - Get help \
`/profile` - Open player profile 
# Deeplink with bonuses
You can setting special link which going, user will get bonuse resources to start.\
To create deep link enter to `aiogram-farm-bot/handlers/users/` and open `start.py` file. Go to 9 line and set `deep_link` to your custom value. \
The next time, user which enter to bot with deep link(`https://t.me/<botname>?start=<your deeplink value here>`), get bonus resources.
