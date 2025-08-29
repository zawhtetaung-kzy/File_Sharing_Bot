import os
import asyncio
from pyrogram import filters
from pyrogram.handlers import MessageHandler
from database.db import db
from pyrogram.enums import MessageEntityType
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

async def start_command(client, message):
    # start parameter ပါလာရင် လုပ်ဆောင်မယ့်အပိုင်း
    if len(message.command) > 1:
        file_id = message.command[1]
        file_data = await db.get_file(file_id)

        if file_data:
            try:
                db_channel_id = int(os.environ.get("DATABASE_CHANNEL_ID"))
                copied_message = await client.copy_message(
                    chat_id=message.chat.id,
                    from_chat_id=db_channel_id,
                    message_id=file_data["message_id"]
                )
                
                await asyncio.sleep(300) # 5 မိနစ်
                
                await client.delete_messages(
                    chat_id=message.chat.id,
                    message_ids=copied_message.id
                )
                
                await message.reply_text("This file has expired and been deleted for security reasons.")
                
            except Exception as e:
                await message.reply_text("Sorry, this file is no longer available.")
                print(f"Error copying message: {e}")
        else:
            await message.reply_text("This file ID is not valid or has expired.")
    # start parameter မပါရင် ပုံမှန်စာပြန်မယ့်အပိုင်း
    else:
        await message.reply_text("Hello! I am a file sharing bot. Use the special link to get files.")

start_command_handler = MessageHandler(start_command, filters.command("start"))
