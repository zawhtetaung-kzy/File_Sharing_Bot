import os
from motor.motor_asyncio import AsyncIOMotorClient

class Database:
    def __init__(self):
        self.client = AsyncIOMotorClient(os.environ.get("DATABASE_URL"))
        self.db = self.client["FileSharingBot"]
        self.files_col = self.db["files"]

    async def add_file(self, movie_name, file_size, message_id):
        await self.files_col.update_one(
            {"movie_name": movie_name},
            {"$set": {"file_size": file_size, "message_id": message_id}},
            upsert=True,
        )

    async def get_files(self, query):
        # find() ကနေ ရလာတဲ့ cursor object ကို list အနေနဲ့ ပြောင်းပေးခြင်း
        return await self.files_col.find({"movie_name": {"$regex": query, "$options": "i"}}).to_list(length=10)
    
    async def get_file_by_message_id(self, message_id):
        return await self.files_col.find_one({"message_id": message_id})

db = Database()
