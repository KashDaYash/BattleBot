# handlers/profile.py
from pyrogram import Client, filters
from db.users import users_collection, characters_collection

@Client.on_message(filters.command("profile"))
async def stats_handler(client, message):
    user_id = message.from_user.id

    # Fetch user profile
    user = await users_collection.find_one({"user_id": user_id})
    if not user:
        return await message.reply("❌ Aap abhi tak game me shamil nahi hue. Type /start to join.")

    # Fetch character based on user.character_id
    char = await characters_collection.find_one({"_id": user["character_id"]})
    if not char:
        return await message.reply("❌ Character data not found. Please contact support.")

    # Fallback HP to character default if undefined
    current_hp = user.get("hp", char["hp"])

    # Create message
    msg = (
        f"📊 <b>Your Stats</b>:\n\n"
        f"🎭 Character: {char['name']} {char['stars']}\n"
        f"📈 Level: {user['level']}\n"
        f"⭐ XP: {user['xp']}/{user['exp_max']}\n"
        f"💥 HP: {current_hp}\n"
        f"🛡 Defense: {char['defense']}\n"
        f"⚔ Damage: {char['damage'][0]} - {char['damage'][1]}\n\n"
        f"💥 Kills: {user['kills']}\n"
        f"🪙 Coins: {user['coins']}\n"
        f"🧿 Yashi: {user['yashi']}\n"
        f"📅 Joined: {user['joined_date']}\n\n"
        f"🎯 Abilities:\n{char['ability']}"
    )

    await client.send_photo(
        chat_id=message.chat.id,
        photo=char["image"],
        caption=msg,
        parse_mode="HTML"
    )