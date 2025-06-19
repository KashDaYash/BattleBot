from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery 
import asyncio



@Client.on_message(filters.command("convert") & filters.user(OWNER_ID))
async def convert_menu(client, message):
    buttons = [
        [InlineKeyboardButton("🔄 Yashi ➝ Coins", callback_data="yashi_to_coins")],
        [InlineKeyboardButton("🔄 Coins ➝ Yashi", callback_data="coins_to_yashi")]
    ]
    await message.reply(
        "<b>Choose Conversion Type:</b>",
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode="html"
    )
    
    
@Client.on_callback_query(filters.regex("^(yashi_to_coins|coins_to_yashi)$"))
async def convert_balances(client, callback_query):
    user_id = callback_query.from_user.id
    if user_id != OWNER_ID:
        return await callback_query.answer("⚠️ Only Owner can use this.", show_alert=True)

    conversion_type = callback_query.data
    text = ""
    users = db.users.find()

    async for user in users:
        uid = user["_id"]
        coins = user.get("coins", 0)
        yashi = user.get("yashi", 0)

        if conversion_type == "yashi_to_coins" and yashi > 0:
            new_coins = coins + (yashi * 10)  # 1 yashi = 10 coins
            await db.users.update_one({"_id": uid}, {
                "$set": {"coins": new_coins, "yashi": 0}
            })
            text = "✅ All users' Yashi converted to Coins."

        elif conversion_type == "coins_to_yashi" and coins >= 10:
            new_yashi = coins // 10
            new_coins = coins % 10
            await db.users.update_one({"_id": uid}, {
                "$set": {"yashi": new_yashi, "coins": new_coins}
            })
            text = "✅ All users' Coins converted to Yashi."

    await callback_query.message.edit_text(text)
    await callback_query.answer("Done!", show_alert=False)    