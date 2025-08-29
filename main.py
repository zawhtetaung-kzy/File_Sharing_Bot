import os
from dotenv import load_dotenv
from pyrogram import Client
from database.db import db
from handlers import start_handler, search_handler, admin_handlers

load_dotenv()

class FileSharingBot(Client):
    def __init__(self):
        super().__init__(
            name="FileSharingBot",
            api_id=int(os.environ.get("API_ID")),
            api_hash=os.environ.get("API_HASH"),
            bot_token=os.environ.get("BOT_TOKEN"),
        )
    
    async def start(self):
        await super().start()
        # Handlers တွေအားလုံးကို တစ်စုတစ်စည်းတည်း ထည့်သွင်းခြင်း
        self.add_handler(start_handler.start_command_handler)
        self.add_handler(search_handler.search_message_handler)
        self.add_handler(admin_handlers.add_file_handler)
        print("Bot is up and running!")

    async def stop(self, *args):
        await super().stop()
        print("Bot has been stopped.")

if __name__ == "__main__":
    bot = FileSharingBot()
    bot.run()
