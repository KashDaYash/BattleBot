from pyrogram import Client, filters
from yash import app, db
from config import OWNER_ID 

shop_collection = db["shop_items"]  # Shop items collection name

# Define the shop items
shop_items = {
    "apple": {"emoji": "🍎", "name": "Apple", "price": 5, "hp": 10},
    "banana": {"emoji": "🍌", "name": "Banana", "price": 7, "hp": 15},
    "kiwi": {"emoji": "🥝", "name": "Kiwi", "price": 8, "hp": 18},
    "burger": {"emoji": "🍔", "name": "Burger", "price": 15, "hp": 25},
    "cold_drink": {"emoji": "🥤", "name": "Cold Drink", "price": 20, "hp": 50},
    "grapes": {"emoji": "🍇", "name": "Grapes", "price": 6, "hp": 12},
    "watermelon": {"emoji": "🍉", "name": "Watermelon", "price": 10, "hp": 20},
    "fries": {"emoji": "🍟", "name": "Fries", "price": 12, "hp": 22},
    "pizza": {"emoji": "🍕", "name": "Pizza", "price": 18, "hp": 30},
    "chocolate": {"emoji": "🍫", "name": "Chocolate", "price": 9, "hp": 16},
}


@app.on_message(filters.command("addshopitems") & filters.user(OWNER_ID))
def add_shop_items(client, message):
    # Insert shop items into the MongoDB collection
    shop_collection.update_one(
        {"_id": "shop_items"},
        {"$set": {"data": shop_items}},
        upsert=True
    )
    message.reply("✅ Shop items have been successfully saved!")