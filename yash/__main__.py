import asyncio
import importlib
from random import choice
from datetime import datetime
from pyrogram import idle
from yash import app
from yash.data.characters import CHARACTER_BASES
from yash.modules import ALL_MODULES
import config
from yash import database 


HELPABLE = {}

async def init():
    # Load modules with help text
    for module_name in ALL_MODULES:
        imported_module = importlib.import_module(module_name)
        if hasattr(imported_module, "__MODULE__") and imported_module.__MODULE__:
            if hasattr(imported_module, "__HELP__") and imported_module.__HELP__:
                HELPABLE[imported_module.__MODULE__.lower()] = imported_module
    print("sᴜᴄᴄᴇssғᴜʟʟʏ ɪᴍᴘᴏʀᴛᴇᴅ ᴍᴏᴅᴜʟᴇs...")

    # Init MongoDB collection 
    database.init_db("users")
    owner_exists = await database.exists({"_id": config.OWNER_ID})
    
    if not owner_exists:
        random_character = choice(list(CHARACTER_BASES.keys()))
        await database.insert({
            "_id": user_id,
            "character": random_character,
            "level": 1,
            "xp": 0,
            "exp_max": 5000,
            "kills": 0,
            "coins": 0,
            "yadle": 0,
            "joined_date": datetime.now().strftime("%m/%d/%y")
        })

    # Start bot
    await app.start()
    await app.send_message(config.LOGGER_ID, "Alive")
    print("Bot Started. Waiting for events...")
    await idle()
    await app.stop()

if __name__ == "__main__":
    asyncio.run(init())
