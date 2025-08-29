import os
from pyrogram import filters
from pyrogram.handlers import MessageHandler
from database.db import db

ADMIN_ID = int(os.environ.get("ADMIN_ID"))
DATABASE_CHANNEL_ID = int(os.environ.get("DATABASE_CHANNEL_ID"))

# Admin က file ပို့လိုက်ရင် ဒီ handler အလုပ်လုပ်ပါမယ်
async def add_file(client, message):
    # Admin ဖြစ်မှသာ အလုပ်လုပ်စေရန် စစ်ဆေးခြင်း
    if message.from_user.id != ADMIN_ID:
        return

    # message မှာ document ပါမပါ စစ်ဆေးခြင်း
    if message.document:
        file_name = message.document.file_name
        file_size = f"{message.document.file_size / (1024*1024):.2f} MB" if message.document.file_size else "N/A"
        
        # database channel ထဲကို file ကို copy လုပ်ခြင်း
        copied_message = await client.copy_message(
            chat_id=DATABASE_CHANNEL_ID,
            from_chat_id=message.chat.id,
            file_id=message.id
        )

        # database ထဲကို file information ထည့်ခြင်း
        await db.add_file(file_name, file_size, copied_message.id)
        
        await message.reply_text(
            f"**File added to database:**\n\n"
            f"**🎬 Movie:** {file_name}\n"
            f"**🗂️ Size:** {file_size}\n"
            f"**✅ Status:** Successfully Added!\n"
            #me update
            f"**Caption:** {caption}\n"
            f"**Fine** {files['file_name']}\n"
        )

add_file_handler = MessageHandler(add_file, filters.private & filters.user(ADMIN_ID) & filters.document)
