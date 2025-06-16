from motor.motor_asyncio import AsyncIOMotorClient
import config 

client = AsyncIOMotorClient(config.MONGO_DB_URI)

db = client["yashigame"]
users = db["users"]