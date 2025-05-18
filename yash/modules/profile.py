from pyrogram import filters
from yash import user_db, app
from yash.data.characters import get_character
from yash.utils.tools import user_check
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery 

@app.on_message(filters.command("profile"))
@user_check()
async def profile_handler(client, message):
    user_id = message.from_user.id
    user_db.set_table("users")
    user_data = user_db.find_by(user_id=user_id)
    if len(user_data) <= 2:
                    Btn = InlineKeyboardMarkup(
                    [[InlineKeyboardButton("Start Me", url=f"https://t.me/{app.get_me().username}")]]
                )
                    await message.reply("Character Nhi Mila Start Me", reply_markup=Btn, disable_web_page_preview=True)
    character_name = user_data[1]
    level = user_data[2] if len(user_data) > 3 else 1

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