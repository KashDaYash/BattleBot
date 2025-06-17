


@Client.on_message(filters.command("shop"))
async def show_shop(client, message):
    items = await db.shop_items.find().to_list(None)
    if not items:
        return await message.reply("❌ Shop not configured. Use /addshop first.")

    keyboard = []
    row = []

    for i, item in enumerate(items, start=1):
        btn = InlineKeyboardButton(
            text=f"{item['emoji']} - 💰{item['price']} | ❤️ +{item['hp']}",
            callback_data=f"buy_{item['_id']}"
        )
        row.append(btn)
        if i % 2 == 0:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)

    await message.reply(
        "🛒 <b>Welcome to the Shop!</b>\nChoose an item to buy:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="html"
    )
    
    
@Client.on_callback_query(filters.regex("^buy_"))
async def handle_buy(client, callback_query):
    user_id = callback_query.from_user.id
    item_id = callback_query.data.split("_", 1)[1]

    user = await db.users.find_one({"_id": user_id})
    if not user:
        return await callback_query.answer("⚠️ First use /start to register!", show_alert=True)

    item = await db.shop_items.find_one({"_id": item_id})
    if not item:
        return await callback_query.answer("❌ Item not found!", show_alert=True)

    if user.get("hp", 100) == 100:
        return await callback_query.answer("❤️ Your HP is already full!", show_alert=True)

    if user.get("coins", 0) < item["price"]:
        return await callback_query.answer("💸 Not enough coins!", show_alert=True)

    # Update user data
    new_hp = min(user.get("hp", 100) + item["hp"], 100)
    new_coins = user["coins"] - item["price"]

    await db.users.update_one(
        {"_id": user_id},
        {"$set": {"hp": new_hp, "coins": new_coins}}
    )

    await callback_query.answer(f"✅ Bought {item['emoji']}! +{item['hp']} HP", show_alert=False)

    await callback_query.message.edit_text(
        f"✅ You bought {item['emoji']}!\n❤️ HP: <b>{new_hp}</b>\n💰 Coins left: <b>{new_coins}</b>",
        parse_mode="html"
    )    