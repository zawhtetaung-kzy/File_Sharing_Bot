import os
from motor.motor_asyncio import AsyncIOMotorClient

class Database:
    def __init__(self):
        self.client = AsyncIOMotorClient(os.environ.get("DATABASE_URL"))
        self.db = self.client["FileSharingBot"]
        self.files_col = self.db["files"]

    async def add_file(self, file_name, file_size, file_id):
        await self.files_col.update_one(
            {"file_name": file_name},
            {"$set": {"file_size": file_size, "file_id": file_id}},
            upsert=True,
        )

    async def get_files(self, query):
        return self.files_col.find({"file_name": {"$regex": query, "$options": "i"}}).to_list(length=10)

db = Database()
