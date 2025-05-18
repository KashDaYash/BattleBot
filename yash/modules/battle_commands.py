from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from yash import app
from random import randint
from yash.data.characters import CHARACTERS, get_character
from yash.utils.tools import user_check


battles = {}

@app.on_message(filters.command("fight"))
@user_check()
async def start_fight(client, message):
    if message.reply_to_message:
        opponent = message.reply_to_message.from_user
    elif len(message.command) > 1:
        opponent = await client.get_users(message.command[1])
    else:
        await message.reply("⚠ Please reply to a user or mention a username to fight.")
        return

    if opponent.id == message.from_user.id:
        await message.reply("⚠ You cannot fight yourself!")
        return

    # Send challenge request
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Accept", callback_data=f"accept_{message.chat.id}_{message.from_user.id}")],
        [InlineKeyboardButton("❌ Reject", callback_data="reject_{message.chat.id}_{message.from_user.id}")]
    ])
    try:
        await client.send_message(
            opponent.id,
            f"⚔ **{message.from_user.first_name} has challenged you to a battle!**\n\nDo you accept?",
            reply_markup=keyboard
        )
        await message.reply("✅ Fight request sent!")
    except Exception as e:
        await message.reply(f"{opponent.first_name if opponent.first_name else opponent.last_name} ne bot private me start nahi kiya")

@app.on_callback_query(filters.regex("^accept_"))
async def accept_fight(client, callback_query):
    challenger_id = int(callback_query.data.split("_")[-1])
    chat_id = int(callback_query.data.split("_")[1])
    if callback_query.from_user.id == challenger_id:
        await callback_query.answer("You cannot accept your own challenge!", show_alert=True)
        return

    # Start the battle
    challenger = await client.get_users(challenger_id)
    opponent = callback_query.from_user
    c1 = get_character("RyuujinKai")  # Get character from database or default
    c2 = get_character("AkariYume")  # Same for opponent character

    result = simulate_fight(c1, c2, challenger, opponent)
    await callback_query.message.edit_text(result)
    await app.send_message(chat_id=chat_id, text=result)

@app.on_callback_query(filters.regex("^reject"))
async def reject_fight(client, callback_query):
    chat_id = int(callback_query.data.split("_")[1])
    await callback_query.answer("❌ Fight request rejected!", show_alert=True)
    await callback_query.message.delete()
    await app.send_message(chat_id=chat_id, text="❌ Fight Request Rejected!")

# Add the simulate_fight function
def simulate_fight(c1, c2, user1, user2):
    log = ""
    turn = 0
    c1_hp, c2_hp = c1.hp, c2.hp

    while c1_hp > 0 and c2_hp > 0:
        attacker = c1 if turn % 2 == 0 else c2
        defender = c2 if turn % 2 == 0 else c1
        dmg = randint(*attacker.damage)
        if randint(1, 100) <= 20:
            dmg *= 2
            log += f"{attacker.name} dealt critical damage!\n"
        if turn % 2 == 0:
            c2_hp -= dmg
        else:
            c1_hp -= dmg
        log += f"{attacker.name} attacks {defender.name} for {dmg} damage.\n"
        turn += 1

    if c1_hp > 0:
        winner_user = user1
        winner_char = c1
    else:
        winner_user = user2
        winner_char = c2

    log += f"\n\n🏆 Winner: {winner_user.first_name} ({winner_char.name})"
    return log