from pyrogram import Client, filters
from pyrogram.types import Message
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timedelta

db = AsyncIOMotorClient().fight_db

@Client.on_message(filters.command("daily"))
async def daily_command(client, message: Message):
    user_id = message.from_user.id
    user = await db.users.find_one({"_id": user_id})
    if not user:
        return await message.reply("❌ First use /start to register.")

    now = datetime.utcnow()
    cooldown_key = f"daily_{user_id}"
    cooldown = await db.cooldowns.find_one({"_id": cooldown_key})

    if cooldown and cooldown.get("expires_at") > now:
        remaining = cooldown["expires_at"] - now
        hours, rem = divmod(remaining.seconds, 3600)
        minutes, seconds = divmod(rem, 60)
        return await message.reply(
            f"⏳ You already claimed. Try again in {hours}h {minutes}m {seconds}s."
        )

    coins = 50  # Fixed daily reward, can also be random
    await db.users.update_one({"_id": user_id}, {"$inc": {"coins": coins}})
    
    await db.cooldowns.replace_one(
        {"_id": cooldown_key},
        {"_id": cooldown_key, "expires_at": now + timedelta(hours=24)},
        upsert=True
    )

    await message.reply(
        f"🎁 You claimed your daily reward!\nYou received <b>{coins} coins</b> 🪙",
        parse_mode="html"
    )