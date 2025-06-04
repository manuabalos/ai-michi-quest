from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.database import Database

MONGO_URI = "mongodb://localhost:27017"  # o URI remota si usas Atlas
DB_NAME = "ai_michi_quest"

client = AsyncIOMotorClient(MONGO_URI)
db: Database = client[DB_NAME]