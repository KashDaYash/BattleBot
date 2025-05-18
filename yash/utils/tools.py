import random
import string
from pyrogram.errors import PeerIdInvalid
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import enums
from functools import wraps
from yash import app
from yash.core.database import init_db, exists

def user_check():
    def decorator(func):
        @wraps(func)
        async def wrapper(client, message: Message, *args, **kwargs):
            try:
                await init_db("users")
                user_exists = await exists({"user_id": message.from_user.id})

                bot_info = await app.get_me()
                Btn = InlineKeyboardMarkup(
                    [[InlineKeyboardButton("Start Me", url=f"https://t.me/{bot_info.username}")]]
                )

                if not user_exists:
                    await message.reply(
                        "❌ Aapne abhi tak mujhe private me start nahi kiya.\n",
                        reply_markup=Btn,
                        disable_web_page_preview=True
                    )
                    return

                await client.send_chat_action(message.from_user.id, enums.ChatAction.TYPING)

            except PeerIdInvalid:
                bot_info = await app.get_me()
                await message.reply(
                    "❌ Aapne abhi tak mujhe private me start nahi kiya.\n",
                    reply_markup=Btn,
                    disable_web_page_preview=True
                )
                return

            return await func(client, message, *args, **kwargs)

        return wrapper
    return decorator
