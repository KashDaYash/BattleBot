from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery 

@app.on_message(filters.command("help"))
async def help_command(client, message: Message):
    text = """
<b>🤖 PvP Fight Bot Commands Help:</b>

<b>🧍 User Commands:</b>
/start - Register yourself in the bot.
/profile - View your user stats like coins, level, kills.
/daily - Claim daily coins (cooldown: 24h).
/pay <amount> - Send coins to another user (reply to user).

<b>⚔️ PvP Commands:</b>
/fight - Challenge another user (reply to their message).
/accept_pvp - Accept a PvP challenge.
/cancel_pvp - Decline a PvP challenge.
/attack - Perform your turn attack in battle.

<b>🏆 Leaderboard:</b>
/leaderboard - View top users by Coins, Kills, Yashi, or Levels.

<b>🐾 Pet System:</b>
/pets - Browse and buy pets (with pagination).
/mypets - View your owned pets.
/feedpet - Feed and level up your pet.
/petbattle - Battle wild enemies using your pet.

<b>💬 Notes:</b>
- Always reply to a user for PvP or /pay.
- You must /start before using most features.
- Each command uses MongoDB for persistent data.

🔒 Admins or the owner can extend this bot with more features like trading pets, skill boosts, team battles, etc.
"""
    await message.reply(text, parse_mode="html")