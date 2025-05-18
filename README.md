# BattleBot - Warrior Duel Game on Telegram

**BattleBot** is a Telegram game bot where users get assigned a warrior and battle others using unique abilities, leveling up over time. Built using [Pyrogram](https://docs.pyrogram.org/), this bot offers fun, anime-inspired character combat in a sleek, modular structure.

## Features

- **Automatic Character Assignment**: New users receive a random warrior upon starting the bot.
- **Unique Warriors**: Each character has its own stats, level scaling, and special abilities.
- **User Profiles**: View your warrior's stats, level, and avatar.
- **Duel System**: Challenge other users to fights and compete for glory.
- **MongoDB Integration**: Stores user data efficiently in a flexible document database.

## Characters

Each warrior has different:
- HP, Damage, Speed
- Level scaling
- Abilities like dodge, heal, stun, or lifesteal

## Tech Stack

- Python 3.10
- Pyrogram
- MongoDB (via Motor)
- Heroku / Docker-ready deployment

---

## Setup Instructions

### 1. Clone the Repo
```bash
git clone https://github.com/yourusername/BattleBot.git
cd BattleBot

2. Install Requirements

pip install -r requirements.txt

3. Setup Environment Variables

Edit the config.py file:

API_ID = "your_api_id"
API_HASH = "your_api_hash"
BOT_TOKEN = "your_bot_token"
OWNER_ID = your_user_id
LOGGER_ID = your_log_channel_id
MONGO_URL = "your_mongo_connection_string"

4. Run the Bot

python -m yash


---

Deploy to Heroku

Option 1: Using heroku.yml

1. Make sure your Heroku app has:

Heroku Container Registry enabled

MongoDB set via MongoDB Atlas



2. Push to Heroku:



heroku container:push worker -a your-app-name
heroku container:release worker -a your-app-name

Option 2: Traditional Buildpack

Make sure you have:

Procfile:

worker: python -m yash

requirements.txt

runtime.txt (e.g., python-3.10.12)



---

Directory Structure

BattleBot/
├── config.py
├── requirements.txt
├── Procfile
├── Dockerfile
├── yash/
│   ├── __main__.py
│   ├── __init__.py
│   ├── core/
│   │   ├── bot.py
│   │   └── database.py
│   ├── modules/
│   │   ├── start.py
│   │   ├── profile.py
│   │   ├── battle_commands.py
│   ├── utils/
│   │   └── tools.py
│   └── data/
│       ├── characters.py
│       └── images/


---

Credits

Built by [Your Name or Team]

Characters & concept inspired by anime battle tropes

Thanks to Pyrogram for the amazing framework



---

License

This project is licensed under the MIT License. Feel free to fork and expand!

---

Let me know if you want it in Hindi or want to add badges, GIF previews, or contribution instructions too.

