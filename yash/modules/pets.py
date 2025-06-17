from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery 

import random


PET_LIST = [ {"name": "lion", "hp": 120, "attack": 20}, {"name": "tiger", "hp": 110, "attack": 18}, {"name": "wolf", "hp": 100, "attack": 15}, {"name": "cat", "hp": 80, "attack": 8}, {"name": "rabbit", "hp": 60, "attack": 5}, {"name": "dog", "hp": 90, "attack": 10}, {"name": "eagle", "hp": 85, "attack": 12}, {"name": "dragon", "hp": 150, "attack": 25} ]

# /pets command

@app.on_message(filters.command("pets")) async def show_pets(client, message: Message): await send_pet_page(client, message.chat.id, 0)

async def send_pet_page(client, chat_id, page): per_page = 4 start = page * per_page end = start + per_page pets = PET_LIST[start:end]

buttons = [
    [InlineKeyboardButton(f"Buy {pet['name'].capitalize()}", callback_data=f"buy_pet_{pet['name']}")]
    for pet in pets
]

navigation = []
if page > 0:
    navigation.append(InlineKeyboardButton("⬅️ Prev", callback_data=f"pets_page_{page-1}"))
if end < len(PET_LIST):
    navigation.append(InlineKeyboardButton("➡️ Next", callback_data=f"pets_page_{page+1}"))
if navigation:
    buttons.append(navigation)

await client.send_message(
    chat_id,
    "🐾 Choose a pet to buy:",
    reply_markup=InlineKeyboardMarkup(buttons)
)



@app.on_callback_query(filters.regex(r"^pets_page_(\d+)$")) async def paginate_pets(client, callback_query: CallbackQuery): page = int(callback_query.data.split("_")[-1]) await callback_query.message.delete() await send_pet_page(client, callback_query.message.chat.id, page)

#Buy pet handler

@app.on_callback_query(filters.regex(r"^buy_pet_(\w+)$")) async def buy_pet(client, callback_query: CallbackQuery): pet_name = callback_query.data.split("_")[-1] pet_data = next((p for p in PET_LIST if p["name"] == pet_name), None) if not pet_data: return await callback_query.answer("❌ Invalid pet.", show_alert=True)

user_id = callback_query.from_user.id
pet_record = {
    "name": pet_name,
    "level": 1,
    "xp": 0,
    "hp": pet_data["hp"],
    "attack": pet_data["attack"]
}
await db.pets.update_one({"_id": user_id}, {"$push": {"pets": pet_record}}, upsert=True)
await callback_query.answer(f"✅ {pet_name.capitalize()} bought successfully!", show_alert=True)

# /mypets command

@app.on_message(filters.command("mypets")) async def my_pets(client, message: Message): user_id = message.from_user.id user_pets = await db.pets.find_one({"_id": user_id}) if not user_pets or not user_pets.get("pets"): return await message.reply("❌ You don't own any pets yet.")

text = "🐶 Your Pets:\n"
for pet in user_pets["pets"]:
    text += (f"• {pet['name'].capitalize()} - Level: {pet['level']} | XP: {pet['xp']} | HP: {pet['hp']} | ATK: {pet['attack']}\n")
await message.reply(text)

#Feed pet command to train (level up)

@app.on_message(filters.command("feedpet")) async def feed_pet(client, message: Message): user_id = message.from_user.id pet_data = await db.pets.find_one({"_id": user_id}) if not pet_data or not pet_data.get("pets"): return await message.reply("❌ You don't have any pets.")

pet = pet_data["pets"][0]  # First pet
pet["xp"] += 10
if pet["xp"] >= 100:
    pet["level"] += 1
    pet["xp"] = 0
    pet["hp"] += 10
    pet["attack"] += 2

await db.pets.update_one({"_id": user_id}, {"$set": {"pets": pet_data["pets"]}})
await message.reply(f"🍗 Fed {pet['name'].capitalize()}! Level: {pet['level']} | XP: {pet['xp']}")

Pet battle between user's pets (can be expanded to PvP later)

@app.on_message(filters.command("petbattle")) async def pet_battle(client, message: Message): user_id = message.from_user.id user = await db.pets.find_one({"_id": user_id}) if not user or not user.get("pets"): return await message.reply("❌ You don't have pets.")

pet = user["pets"][0]  # First pet
enemy_hp = 100
battle_log = "⚔️ Pet Battle Started!\n"
while enemy_hp > 0 and pet["hp"] > 0:
    dmg = random.randint(pet["attack"]//2, pet["attack"])
    enemy_dmg = random.randint(5, 15)
    enemy_hp -= dmg
    pet["hp"] -= enemy_dmg
    battle_log += f"{pet['name'].capitalize()} dealt {dmg}, received {enemy_dmg}\n"

if pet["hp"] <= 0:
    battle_log += "❌ Your pet fainted!"
else:
    battle_log += "🏆 Your pet won! +20 XP"
    pet["xp"] += 20
    if pet["xp"] >= 100:
        pet["level"] += 1
        pet["xp"] = 0
        pet["hp"] += 10
        pet["attack"] += 2

await db.pets.update_one({"_id": user_id}, {"$set": {"pets": user["pets"]}})
await message.reply(battle_log)

