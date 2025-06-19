from pyrogram import Client, filters 
from pyrogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton 
import random

@Client.on_message(filters.command("hunt")) async def hunt_handler(c, m: Message): user_id = m.from_user.id user = users_col.find_one({"user_id": user_id}) if not user: return await m.reply("⚠️ Pehle /start karke character le lo.")

characters = mongo.characters.find_one()
enemies = mongo.enemies.find_one()

if not characters or not enemies:
    return await m.reply("❌ Characters ya Enemies load nahi huye.")

keys = list(enemies.keys())
random_key = random.choice(keys)
enemy = enemies[random_key]

users_col.update_one({"user_id": user_id}, {"$set": {"current_enemy": random_key}})
character = characters[user['character_id']]

msg = f"🔍 <b>Enemy Found!</b>\n\n👤 You: {character['name']}\n👹 Enemy: {enemy['name']}\n❤️ HP: {enemy.get('hp', enemy.get('max_hp'))}\n\n<i>\"{enemy['quote']}\"</i>"

buttons = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("🔁 Next Enemy", callback_data="next_enemy"),
        InlineKeyboardButton("⚔️ Battle", callback_data="start_battle")
    ]
])
await c.send_photo(m.chat.id, enemy['image'], caption=msg, reply_markup=buttons, parse_mode="HTML")

@Client.on_callback_query(filters.regex("^next_enemy$")) async def next_enemy(c, q: CallbackQuery): user_id = q.from_user.id user = users_col.find_one({"user_id": user_id}) if not user: return await q.answer("⚠️ Pehle /start karke character le lo.", show_alert=True)

characters = mongo.characters.find_one()
enemies = mongo.enemies.find_one()
if not characters or not enemies:
    return await q.answer("❌ Characters ya Enemies load nahi huye.", show_alert=True)

current_key = user.get("current_enemy")
keys = list(enemies.keys())
available = [k for k in keys if k != current_key] or keys
new_key = random.choice(available)
enemy = enemies[new_key]

users_col.update_one({"user_id": user_id}, {"$set": {"current_enemy": new_key}})
character = characters[user['character_id']]

caption = f"🔍 <b>Enemy Found!</b>\n\n👤 You: {character['name']}\n👹 Enemy: {enemy['name']}\n❤️ HP: {enemy['hp']}\n\n<i>\"{enemy['quote']}\"</i>"
buttons = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("🔁 Next Enemy", callback_data="next_enemy"),
        InlineKeyboardButton("⚔️ Battle", callback_data="start_battle")
    ]
])
try:
    await q.edit_message_media(media=("photo", enemy['image']), reply_markup=buttons)
    await q.edit_message_caption(caption, reply_markup=buttons, parse_mode="HTML")
except Exception as e:
    await q.message.reply("❌ Error: " + str(e))

@Client.on_callback_query(filters.regex("^start_battle$")) async def start_battle(c, q: CallbackQuery): user_id = q.from_user.id user = users_col.find_one({"user_id": user_id}) characters = mongo.characters.find_one() enemies = mongo.enemies.find_one() if not user or not characters or not enemies: return await q.message.reply("⚠️ Required data missing. Pehle /start karo.")

char = characters[user['character_id']]
enemy_key = user.get("current_enemy")
enemy = enemies.get(enemy_key)
if not enemy:
    return await q.message.reply("❌ Enemy load nahi hua. Try /hunt again.")

player_attack = random.randint(char['damage'][0], char['damage'][1])
enemy_attack = random.randint(enemy['attack'][0], enemy['attack'][1])
player_hp = user.get("hp", char['hp']) - enemy_attack
enemy_hp = enemy['hp'] - player_attack

battle = {"player_hp": player_hp, "enemy_hp": enemy_hp, "enemy_key": enemy_key}
users_col.update_one({"user_id": user_id}, {"$set": {"battle": battle}})

msg = f"⚔️ <b>Battle Start!</b>\n\n👤 You attacked {enemy['name']} and dealt <b>{player_attack}</b> damage.\n👹 {enemy['name']} attacked back and dealt <b>{enemy_attack}</b> damage.\n\n❤️ Your HP: <b>{player_hp}</b>\n💀 Enemy HP: <b>{enemy_hp}</b>"

buttons = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("⚔️ Attack", callback_data="attack_battle"),
        InlineKeyboardButton("🏃 Retreat", callback_data="retreat_battle")
    ]
])
await q.edit_message_caption(msg, reply_markup=buttons, parse_mode="HTML")

@Client.on_callback_query(filters.regex("^attack_battle$")) async def attack_battle(c, q: CallbackQuery): user_id = q.from_user.id user = users_col.find_one({"user_id": user_id}) characters = mongo.characters.find_one() enemies = mongo.enemies.find_one() battle = user.get("battle")

if not user or not characters or not enemies or not battle:
    return await q.message.reply("⚠️ Battle data missing. Pehle /hunt aur battle start karo.")

char = characters[user['character_id']]
enemy = enemies[battle['enemy_key']]

if battle['player_hp'] <= 0:
    users_col.update_one({"user_id": user_id}, {"$unset": {"battle": ""}})
    return await q.edit_message_caption("💀 <b>You have already been defeated!</b>\nTry /hunt to find a new enemy.", parse_mode="HTML")

if battle['enemy_hp'] <= 0:
    users_col.update_one({"user_id": user_id}, {"$unset": {"battle": ""}})
    return await q.edit_message_caption(f"🎉 <b>You already defeated {enemy['name']}!</b>\nTry /hunt for next enemy.", parse_mode="HTML")

player_attack = random.randint(char['damage'][0], char['damage'][1])
enemy_attack = random.randint(enemy['attack'][0], enemy['attack'][1])
new_player_hp = battle['player_hp'] - enemy_attack
new_enemy_hp = battle['enemy_hp'] - player_attack

result = f"⚔️ <b>Battle Continues!</b>\n\n👤 You dealt <b>{player_attack}</b> to {enemy['name']}.\n👹 {enemy['name']} dealt <b>{enemy_attack}</b> to you.\n\n❤️ Your HP: <b>{max(new_player_hp, 0)}</b>\n💀 Enemy HP: <b>{max(new_enemy_hp, 0)}</b>"
buttons = []

if new_player_hp <= 0 and new_enemy_hp <= 0:
    result += "\n\n🤝 <b>It's a Draw!</b>"
    users_col.update_one({"user_id": user_id}, {"$unset": {"battle": ""}})

elif new_player_hp <= 0:
    result += f"\n\n💀 <b>You were defeated by {enemy['name']}!</b>"
    users_col.update_one({"user_id": user_id}, {"$unset": {"battle": ""}})

elif new_enemy_hp <= 0:
    result += f"\n\n🏆 <b>You defeated {enemy['name']}!</b>"
    xp_gain = random.randint(2, 5)
    new_xp = user.get("xp", 0) + xp_gain
    exp_max = user.get("exp_max", 100)
    level = user.get("level", 1)
    coins = user.get("coins", 0)

    if new_xp >= exp_max:
        level += 1
        new_xp -= exp_max
        exp_max = int(exp_max * 1.3)
        char['damage'][0] += 1
        char['damage'][1] += 1
        users_col.update_one({}, {"$set": {f"characters.{user['character_id']}": char}})
        coins += random.randint(10, 20)
        result += f"\n\n🆙 <b>Level Up!</b>\n⭐ New Level: <b>{level}</b>\n💰 Bonus Coins: <b>{coins}</b>\n💥 Damage Increased!"

    result += f"\n🎖️ <b>XP Gained:</b> {xp_gain}"

    users_col.update_one({"user_id": user_id}, {
        "$unset": {"battle": ""},
        "$set": {
            "xp": new_xp,
            "level": level,
            "exp_max": exp_max,
            "coins": coins
        }
    })

else:
    users_col.update_one({"user_id": user_id}, {
        "$set": {
            "battle": {
                "player_hp": new_player_hp,
                "enemy_hp": new_enemy_hp,
                "enemy_key": battle['enemy_key']
            }
        }
    })
    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("⚔️ Attack", callback_data="attack_battle"),
            InlineKeyboardButton("🏃 Retreat", callback_data="retreat_battle")
        ]
    ])

await q.edit_message_caption(result, reply_markup=buttons, parse_mode="HTML")

@Client.on_callback_query(filters.regex("^retreat_battle$")) async def retreat_battle(c, q: CallbackQuery): user_id = q.from_user.id user = users_col.find_one({"user_id": user_id}) if not user: return await q.message.reply("⚠️ User data missing!")

penalty = min(user.get("coins", 0), 10)
users_col.update_one({"user_id": user_id}, {
    "$set": {"coins": user.get("coins", 0) - penalty},
    "$unset": {"battle": ""}
})

retreat_text = f"🏃 <b>You retreated from battle!</b>\n💸 Lost <b>{penalty}</b> coins.\n\nTrain more and try again!"
await q.edit_message_caption(retreat_text, parse_mode="HTML")

