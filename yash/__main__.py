import asyncio
from yash import app, user_db
import importlib
from yash.modules import ALL_MODULES
from pyrogram import idle
import config
from random import choice
from yash.data.characters import CHARACTERS

HELPABLE = {}

async def init():
    for module_name in ALL_MODULES:
        imported_module = importlib.import_module(module_name)
        if hasattr(imported_module, "__MODULE__") and imported_module.__MODULE__:
            if hasattr(imported_module, "__HELP__") and imported_module.__HELP__:
                HELPABLE[imported_module.__MODULE__.lower()] = imported_module
    print("sᴜᴄᴄᴇssғᴜʟʟʏ ɪᴍᴘᴏʀᴛᴇᴅ ᴍᴏᴅᴜʟᴇs...") 
    user_db.set_table("users")
    user_db.create_table("users", {
        "user_id": "INTEGER",
        "character": "TEXT",
        "level": "INTEGER DEFAULT 1",
        "xp": "INTEGER DEFAULT 0"
    }, primary_key="user_id")
    existing = user_db.find_by(user_id=config.OWNER_ID)
    
    if not existing:
        random_character = choice(list(CHARACTERS.keys()))
        user_db.insert({
            "user_id": config.OWNER_ID,
            "character": random_character,
            "level": 1,
            "xp": 0
        })
    
    await app.start()
    await app.send_message(config.LOGGER_ID, "Alive")
    print("Bot Started. Waiting for events...")
    await idle()
    await app.stop()

if __name__ == "__main__":
    asyncio.get_event_loop_policy().get_event_loop().run_until_complete(init())