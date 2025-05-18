from pyrogram import filters
from yash import app
from yash.core import database
from yash.data.characters import get_character
from yash.utils.tools import user_check
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

@app.on_message(filters.command("profile"))
@user_check()
async def profile_handler(client, message):
    user_id = message.from_user.id

    user_data = await database.collection.find_one({"user_id": user_id})
    if not user_data or "character" not in user_data:
        Btn = InlineKeyboardMarkup(
            [[InlineKeyboardButton("Start Me", url=f"https://t.me/{app.username}")]]
        )
        await message.reply("Character Nhi Mila Start Me", reply_markup=Btn, disable_web_page_preview=True)
        return

    character_name = user_data["character"]
    level = user_data.get("level", 1)

    character = get_character(character_name)
    if not character:
        return await message.reply("Character data load nahi ho paya!")

    character.level = level
    character.update_stats()

    caption = character.display_info()

    try:
        await message.reply_photo(photo=character.image_path, caption=caption)
    except Exception as e:
        await message.reply(f"Image bhejne me problem aayi: {e}")
