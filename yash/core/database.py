from motor.motor_asyncio import AsyncIOMotorClient
import config 

mongo_url = "mongodb://localhost:27017"  # ya aapka Mongo Atlas URI
client = AsyncIOMotorClient(config.MONGO_DB_URI)

db = client["yashigame"]
users = db["users"]