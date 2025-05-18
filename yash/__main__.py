import asyncio
import importlib
from random import choice

from pyrogram import idle
from yash import app
from yash.core import database
from yash.data.characters import CHARACTERS
from yash.modules import ALL_MODULES
import config

HELPABLE = {}

async def init():
    # Init MongoDB collection
    database.init_db("users")

    # Load modules with help text
    for module_name in ALL_MODULES:
        imported_module = importlib.import_module(module_name)
        if hasattr(imported_module, "__MODULE__") and imported_module.__MODULE__:
            if hasattr(imported_module, "__HELP__") and imported_module.__HELP__:
                HELPABLE[imported_module.__MODULE__.lower()] = imported_module
    print("sᴜᴄᴄᴇssғᴜʟʟʏ ɪᴍᴘᴏʀᴛᴇᴅ ᴍᴏᴅᴜʟᴇs...")

    # Check if OWNER exists in DB
    owner_exists = await database.exists({"user_id": config.OWNER_ID})

    if not owner_exists:
        random_character = choice(list(CHARACTERS.keys()))
        await database.insert({
            "user_id": config.OWNER_ID,
            "character": random_character,
            "level": 1,
            "xp": 0
        })

    # Start bot
    await app.start()
    await app.send_message(config.LOGGER_ID, "Alive")
    print("Bot Started. Waiting for events...")
    await idle()
    await app.stop()

if __name__ == "__main__":
    asyncio.run(init())
