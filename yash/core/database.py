import motor.motor_asyncio
import config 

client = motor.motor_asyncio.AsyncIOMotorClient(config.MONGO_DB_URI)
db = client["users"]

collection = db["usercol"]  # define globally

def init_db(collection_name):
    global collection
    collection = db[collection_name]

async def insert(data: dict):
    if collection is None:
        raise RuntimeError("Database not initialized. Call init_db() first.")
    result = await collection.insert_one(data)
    return result.inserted_id

async def update(filters: dict, updates: dict, upsert=False):
    if not collection:
        raise RuntimeError("Database not initialized. Call init_db() first.")
    result = await collection.update_many(filters, {"$set": updates}, upsert=upsert)
    return result.modified_count

async def delete(filters: dict):
    if not collection:
        raise RuntimeError("Database not initialized. Call init_db() first.")
    result = await collection.delete_many(filters)
    return result.deleted_count

async def exists(query: dict) -> bool:
    if collection is None:
        raise ValueError("Collection is not set.")
    result = await collection.find_one(query)
    return result is not None
