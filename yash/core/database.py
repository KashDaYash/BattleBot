from motor.motor_asyncio import AsyncIOMotorClient
import config 

client = AsyncIOMotorClient(config.MONGO_DB_URI)

db = client["yashigame"]
users_col = db["users"]
char_col = db["characters"]
fight_col = ["fight"]




