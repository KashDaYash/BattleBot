import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
db = client["users"]

collection = None  # define globally

def init_db(collection_name):
    global collection
    collection = db[collection_name]

async def insert(data: dict):
    if not collection:
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

async def exists(filters: dict):
    if not collection:
        raise RuntimeError("Database not initialized. Call init_db() first.")
    doc = await collection.find_one(filters)
    return doc is not None
