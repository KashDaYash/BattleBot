# handlers/start.py
from pyrogram import Client, filters
from db.users import users_collection, characters_collection
from datetime import datetime
import random

@Client.on_message(filters.command("start"))
async def start_handler(client, message):
    user_id = message.from_user.id

    # Check if user already exists
    user = await users_collection.find_one({"user_id": user_id})
    if user:
        return await message.reply("😎 Aap already game me ho!\nType /stats to see your stats.")

    # Get all characters from DB
    characters_cursor = characters_collection.find({})
    characters = await characters_cursor.to_list(length=100)
    
    if not characters:
        return await message.reply("❌ No characters found in database!")

    # Choose a random character
    char = random.choice(characters)

    # Create user profile
    profile = {
        "user_id": user_id,
        "character_id": char["_id"],
        "level": 1,
        "xp": 0,
        "exp_max": 100,
        "kills": 0,
        "coins": 100,
        "yashi": 0,
        "joined_date": datetime.utcnow().strftime("%Y-%m-%d"),
        "hp": char["hp"],
        "defense": char["defense"]
    }

    # Insert into MongoDB
    await users_collection.insert_one(profile)

    # Prepare welcome message
    msg = (
        f"🎮 Welcome to Battle Bot!\n\n"
        f"🎭 Character: {char['name']} {char['stars']}\n"
        f"💥 HP: {char['hp']} | 🛡 Defense: {char['defense']}\n"
        f"⚔ Damage: {char['damage'][0]} - {char['damage'][1]}\n\n"
        f"🗨 Quote: \"{char['quote']}\"\n\n"
        f"🎯 Abilities:\n{char['ability']}\n\n"
        f"🪙 Coins: 100\n"
        f"🧿 Yashi: 0\n\n"
        f"Type /stats to view your progress."
    )

    # Send photo
    await client.send_photo(
        chat_id=message.chat.id,
        photo=char["image"],
        caption=msg
    )