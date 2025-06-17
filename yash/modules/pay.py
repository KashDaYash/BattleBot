from pyrogram import filters
from pyrogram.types import Message

@app.on_message(filters.command("pay") & filters.reply)
async def pay_command(client, message: Message):
    sender = message.from_user
    receiver = message.reply_to_message.from_user

    if sender.id == receiver.id:
        return await message.reply("❌ You can't send coins to yourself.")

    try:
        amount = int(message.text.split()[1])
        if amount <= 0:
            return await message.reply("❌ Invalid amount.")
    except (IndexError, ValueError):
        return await message.reply("❌ Usage: /pay <amount> (by replying to user)")

    sender_data = await db.users.find_one({"_id": sender.id})
    receiver_data = await db.users.find_one({"_id": receiver.id})

    if not sender_data or sender_data.get("coins", 0) < amount:
        return await message.reply("❌ You don't have enough coins.")

    # Transaction
    await db.users.update_one({"_id": sender.id}, {"$inc": {"coins": -amount}})
    await db.users.update_one({"_id": receiver.id}, {"$inc": {"coins": amount}}, upsert=True)

    await message.reply(
        f"✅ <a href='tg://user?id={sender.id}'>{sender.first_name}</a> sent <b>{amount}</b> coins to <a href='tg://user?id={receiver.id}'>{receiver.first_name}</a>!",
        parse_mode="html"
    )