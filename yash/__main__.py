import asyncio
import importlib
from datetime import datetime
from pyrogram import idle
from yash import app
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

    # Start bot
    await app.start()
    await app.send_message(config.LOGGER_ID, "Alive")
    print("Bot Started. Waiting for events...")
    await idle()
    await app.stop()

if __name__ == "__main__":
    asyncio.run(init())
