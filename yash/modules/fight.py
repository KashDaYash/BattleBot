from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery 
import random, asyncio


@app.on_message(filters.command("fight")) async def fight_handler(client, message: Message): users = await db.users.find_one({"_id": message.from_user.id}) if not users: return await message.reply("❌ First use /start to register.")

if not message.reply_to_message:
    return await message.reply("❌ Reply to someone's message to challenge them.")

opponent = message.reply_to_message.from_user
if opponent.id == message.from_user.id:
    return await message.reply("❌ Invalid opponent!")

opponent_data = await db.users.find_one({"_id": opponent.id})
if not opponent_data:
    return await message.reply("❌ Opponent is not registered.")

await db.pvp_requests.replace_one({"_id": opponent.id}, {
    "_id": opponent.id,
    "challenger_id": message.from_user.id,
    "opponent_id": opponent.id
}, upsert=True)

await client.send_message(
    chat_id=opponent.id,
    text=f"⚔️ <a href=\"tg://user?id={message.from_user.id}\">{message.from_user.first_name}</a> challenged you to a PvP battle!\nDo you accept? (expires in 60 sec)",
    parse_mode="html",
    reply_markup=InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ Accept", callback_data="accept_pvp"),
            InlineKeyboardButton("❌ Cancel", callback_data="cancel_pvp")
        ]
    ])
)

await asyncio.sleep(60)
request = await db.pvp_requests.find_one({"_id": opponent.id})
if request:
    await db.pvp_requests.delete_one({"_id": opponent.id})
    await client.send_message(
        chat_id=message.chat.id,
        text=f"⌛ PvP request expired – no confirmation received.",
    )

Accept PvP

@app.on_callback_query(filters.regex("^accept_pvp$")) async def accept_pvp(client, callback_query: CallbackQuery): user_id = callback_query.from_user.id request = await db.pvp_requests.find_one({"_id": user_id}) if not request: return await callback_query.answer("❌ No fight request pending.", show_alert=True)

challenger = request["challenger_id"]
opponent = request["opponent_id"]

await db.pvp_requests.delete_one({"_id": user_id})
fight_key = f"{challenger}_{opponent}"

await db.fights.replace_one({"_id": fight_key}, {
    "_id": fight_key,
    "hp1": 100,
    "hp2": 100,
    "user1": challenger,
    "user2": opponent,
    "turn": challenger
}, upsert=True)

await client.send_message(
    chat_id=challenger,
    text=f"🔥 PvP Battle Started with <a href=\"tg://user?id={opponent}\">Opponent</a>!\n❤️ Player 1: 100 HP\n❤️ Player 2: 100 HP\n👊 Your Turn!",
    parse_mode="html",
    reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton("Attack 👊", callback_data=f"attack_{challenger}_{opponent}")]
    ])
)

Cancel PvP

@app.on_callback_query(filters.regex("^cancel_pvp$")) async def cancel_pvp(client, callback_query: CallbackQuery): user_id = callback_query.from_user.id request = await db.pvp_requests.find_one({"_id": user_id}) if not request: return await callback_query.answer("❌ No fight request.", show_alert=True)

challenger = request["challenger_id"]
await db.pvp_requests.delete_one({"_id": user_id})

await client.send_message(
    chat_id=challenger,
    text=f"❌ <a href=\"tg://user?id={user_id}\">{callback_query.from_user.first_name}</a> declined your PvP challenge.",
    parse_mode="html"
)

await callback_query.message.edit("❌ You declined the PvP challenge.")

Attack logic

@app.on_callback_query(filters.regex(r"^attack_(\d+)(\d+)$")) async def pvp_attack(client, callback_query: CallbackQuery): attacker_id = callback_query.from_user.id uid1, uid2 = map(int, callback_query.data.split("")[1:]) fight_key = f"{uid1}_{uid2}" fight = await db.fights.find_one({"_id": fight_key})

if not fight:
    return await callback_query.answer("❌ Fight not found.", show_alert=True)

if fight["turn"] != attacker_id:
    return await callback_query.answer("❌ Not your turn!", show_alert=True)

opponent = uid2 if attacker_id == uid1 else uid1
damage = random.randint(5, 20)
if attacker_id == uid1:
    fight["hp2"] -= damage
else:
    fight["hp1"] -= damage

text = f"🥊 <a href=\"tg://user?id={attacker_id}\">Attacker</a> did <b>{damage}</b> damage!\n"
text += f"❤️ <a href=\"tg://user?id={uid1}\">P1</a>: {max(fight['hp1'], 0)} HP\n"
text += f"💔 <a href=\"tg://user?id={uid2}\">P2</a>: {max(fight['hp2'], 0)} HP"

winner, loser = None, None
if fight['hp1'] <= 0:
    winner, loser = uid2, uid1
elif fight['hp2'] <= 0:
    winner, loser = uid1, uid2

if winner:
    await db.users.update_one({"_id": winner}, {"$inc": {"coins": 100}}, upsert=True)
    await db.users.update_one({"_id": loser}, {"$inc": {"coins": -100}}, upsert=True)
    await db.fights.delete_one({"_id": fight_key})
    text += f"\n\n🏆 <a href=\"tg://user?id={winner}\">Winner</a> won +100 coins!"
    text += f"\n💸 <a href=\"tg://user?id={loser}\">Loser</a> lost 100 coins."
else:
    fight["turn"] = opponent
    await db.fights.replace_one({"_id": fight_key}, fight)

await callback_query.message.edit(
    text=text,
    parse_mode="html",
    reply_markup=None if winner else InlineKeyboardMarkup([
        [InlineKeyboardButton("Attack 👊", callback_data=f"attack_{uid1}_{uid2}")]
    ])
)



