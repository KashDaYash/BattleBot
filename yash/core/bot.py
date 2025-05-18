# Sample content for bot.py
from pyrogram import Client, enums 
from config import API_ID, API_HASH, BOT_TOKEN
from yash import modules

class Yaara(Client):
    def __init__(self):
        super().__init__(
            "BattleBot",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
        )

    async def start(self):
        await super().start()
        bot_me = await self.get_me()
        print(f"{bot_me.first_name} Started Successfully!")

    async def stop(self):
        await super().stop()
        print("Bot Stopped.")
