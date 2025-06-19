from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery

# Common Function for Leaderboard Message
async def get_leaderboard(metric: str) -> str:
    metric_name = {
        "coins": "🪙 Coins",
        "levels": "🧬 Levels",
        "kills": "🔥 Kills",
        "yashi": "💠 Yashi"
    }.get(metric, metric)

    leaderboard_text = f"🏆 <b>Top 10 {metric_name} Leaderboard</b>\n\n"
    top_users = db.users.find({metric: {"$exists": True}}).sort(metric, -1).limit(10)

    async for i, user in enumerate(top_users, start=1):
        mention = f"<a href='tg://user?id={user['_id']}'>User</a>"
        value = user.get(metric, 0)
        leaderboard_text += f"{i}. {mention} — <b>{value}</b>\n"

    return leaderboard_text

# /leaderboard Command
@Client.on_message(filters.command("leaderboard"))
async def leaderboard_command(client, message: Message):
    await message.reply(
        "📊 Choose a leaderboard type:",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🪙 Coins", callback_data="leaderboard_coins"),
                InlineKeyboardButton("🧬 Levels", callback_data="leaderboard_levels"),
            ],
            [
                InlineKeyboardButton("🔥 Kills", callback_data="leaderboard_kills"),
                InlineKeyboardButton("💠 Yashi", callback_data="leaderboard_yashi"),
            ]
        ])
    )

# Callback Handler
@Client.on_callback_query(filters.regex(r"^leaderboard_(coins|levels|kills|yashi)$"))
async def leaderboard_callback(client, callback_query: CallbackQuery):
    metric = callback_query.data.split("_")[1]
    text = await get_leaderboard(metric)
    await callback_query.message.edit(text, parse_mode="html")