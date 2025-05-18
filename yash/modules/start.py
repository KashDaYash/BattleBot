from pyrogram import filters
from pyrogram.types import Message
from yash import app, user_db
from random import choice
from datetime import datetime
from yash.data.characters import CHARACTERS

__MODULE__ = "Start"
__HELP__ = """
/start - Bot start karne par ek random warrior assign karta hai agar pehle se assigned nahi hai.
"""

@app.on_message(filters.command("start") & filters.private)
async def start_handler(client, message: Message):
    user = message.from_user
    user_id = user.id
    name = user.first_name

    user_db.set_table("users")
    user_db.create_table("users", {
        "user_id": "INTEGER",
        "character": "TEXT",
        "level": "INTEGER",
        "xp": "INTEGER",
        "exp_max": "INTEGER",
        "kills": "INTEGER",
        "coins": "INTEGER",
        "yadle": "INTEGER",
        "joined_date": "TEXT"
    }, primary_key="user_id")

    existing = user_db.find_by(user_id=user_id)
    if not existing:
        random_character = choice(list(CHARACTERS.keys()))
        user_db.insert({
            "user_id": user_id,
            "character": random_character,
            "level": 1,
            "xp": 0,
            "exp_max": 5000,
            "kills": 0,
            "coins": 0,
            "yadle": 0,
            "joined_date": datetime.now().strftime("%m/%d/%y")
        })
        await message.reply_text(
            f"Hello {name}, welcome to Yashi Bot!\n"
            f"You have been assigned **{random_character}**!"
        )
    else:
        character_name = existing[1]
        await message.reply_text(
            f"Hello {name}, welcome back!\n"
            f"You are currently assigned to **{character_name}**."
        )
