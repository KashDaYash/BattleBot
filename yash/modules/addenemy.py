from pyrogram import Client, filters
from yash import app, db
from config import OWNER_ID 

enemies_collection = db["enemies"]

# Define the enemies
enemies = {
    "Drakor": {
        "name": "Drakor",
        "hp": 45,
        "attack": [10, 13],
        "quote": "Flames dance at my command.",
        "image": "https://files.catbox.moe/yjqp8n.jpg"
    },
    "Glacier": {
        "name": "Glacier",
        "hp": 38,
        "attack": [9, 11],
        "quote": "I am the frozen wrath of the mountains.",
        "image": "https://envs.sh/HqE.jpg"
    },
    "Grudor": {
        "name": "Grudor",
        "hp": 50,
        "attack": [7, 10],
        "quote": "Stone and steel are my allies.",
        "image": "https://files.catbox.moe/5xprol.jpg"
    },
    "Zarnok": {
        "name": "Zarnok",
        "hp": 35,
        "attack": [11, 14],
        "quote": "Shadows bend to my will.",
        "image": "https://files.catbox.moe/avzr6a.jpg"
    },
    "Silicox": {
        "name": "Silicox",
        "hp": 42,
        "attack": [9, 12],
        "quote": "Electricity courses through me.",
        "image": "https://files.catbox.moe/rnad1x.jpg"
    },
    "Venmora": {
        "name": "Venmora",
        "hp": 36,
        "attack": [10, 13],
        "quote": "My venom is your demise.",
        "image": "https://files.catbox.moe/2gjal5.jpg"
    },
    "Abyzoth": {
        "name": "Abyzoth",
        "hp": 48,
        "attack": [12, 15],
        "quote": "I am the harbinger of souls.",
        "image": "https://files.catbox.moe/xdwbyu.jpg"
    },
    "Voltrix": {
        "name": "Voltrix",
        "hp": 37,
        "attack": [8, 11],
        "quote": "Crystals reveal your fate.",
        "image": "https://envs.sh/HC_.jpg"
    },
    "Floraxa": {
        "name": "Floraxa",
        "hp": 55,
        "attack": [13, 16],
        "quote": "Nature's fury is my strength.",
        "image": "https://files.catbox.moe/msdb4a.jpg"
    },
    "Nimbrax": {
        "name": "Nimbrax",
        "hp": 55,
        "attack": [13, 16],
        "quote": "Storms gather at my beckoning.",
        "image": "https://files.catbox.moe/pxe6dd.jpg"
    },
    "Zombino": {
        "name": "Zombino",
        "hp": 55,
        "attack": [13, 16],
        "quote": "The undead rise with me.",
        "image": "https://envs.sh/HC5.jpg"
    }
}



@app.on_message(filters.command("addenemies") & filters.user(OWNER_ID))
def add_enemies(client, message):
    # Insert enemies into the MongoDB collection
    enemies_collection.update_one(
        {"_id": "enemies"},
        {"$set": {"data": enemies}},
        upsert=True
    )
    message.reply("✅ 10 enemies have been successfully saved!")
