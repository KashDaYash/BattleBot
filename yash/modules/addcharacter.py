from pyrogram import Client, filters
from yash import app, db
from config import OWNER_ID 
users_collection = db["users"]
# Define the characters
characters = {
    "RyuujinKai": {
        "name": "Ryuujin Kai",
        "stars": "✪✪✪✪",
        "hp": 30,
        "damage": [10, 12],
        "defense": 52,
        "quote": "The dragon’s roar shakes the heavens!",
        "ability": "• 20% chance to dodge.\n• 10% chance to deal double damage.",
        "image": "https://files.catbox.moe/atwh6c.jpg"
    },
    "AkariYume": {
        "name": "Akari Yume",
        "stars": "✪✪✪",
        "hp": 25,
        "damage": [8, 10],
        "defense": 60,
        "quote": "Dreams create reality!",
        "ability": "• 30% chance to dodge.\n• 5% chance to heal 5 HP per turn.",
        "image": "https://files.catbox.moe/qc7wvc.jpg"
    },
    "KuroganeRaiden": {
        "name": "Kurogane Raiden",
        "stars": "✪✪✪✪✪",
        "hp": 40,
        "damage": [12, 15],
        "defense": 45,
        "quote": "Thunder strikes with unyielding power!",
        "ability": "• 15% chance to stun enemy.\n• 20% chance to deal 150% damage.",
        "image": "https://envs.sh/Hqu.jpg"
    },
    "YashaNoctis": {
        "name": "Yasha Noctis",
        "stars": "✪✪✪✪",
        "hp": 28,
        "damage": [9, 11],
        "defense": 55,
        "quote": "Darkness is just another path to power.",
        "ability": "• 25% chance to dodge.\n• 10% chance to drain 5 HP from the enemy.",
        "image": "https://envs.sh/HqT.jpg"
    },
    "HarutoHikari": {
        "name": "Haruto Hikari",
        "stars": "✪✪",
        "hp": 20,
        "damage": [6, 8],
        "defense": 50,
        "quote": "Even the smallest light can shine in the darkest night!",
        "ability": "• 20% chance to dodge.\n• 5% chance to recover 3 HP after each attack.",
        "image": "https://envs.sh/Hqd.jpg"
    },
    "Lumina": {
        "name": "Lumina",
        "stars": "✪✪",
        "hp": 30,
        "damage": [14, 18],
        "defense": 60,
        "quote": "Rise through the shadows and blaze your own path!",
        "ability": "• 20% chance to dodge.\n• 5% chance to recover 3 HP after each attack.",
        "image": "https://envs.sh/HqQ.jpg"
    }
}


@app.on_message(filters.command("addcharacter") & filters.user(OWNER_ID))
def add_character(client, message):
    # Insert characters into the MongoDB collection
    users_collection.update_one(
        {"_id": "characters"},
        {"$set": {"data": characters}},
        upsert=True
    )
    message.reply("Characters successfully saved to the database.")
