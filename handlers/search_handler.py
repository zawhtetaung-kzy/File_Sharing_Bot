import os
from pyrogram import filters
from pyrogram.handlers import MessageHandler
from database.db import db
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

ADMIN_ID = int(os.environ.get("ADMIN_ID"))

async def search_message(client, message):
    if not message.text or message.entities:
        return

    query = message.text.lower().strip()
    
    # Database ထဲက အနီးစပ်ဆုံး Movie တွေကို ရှာဖွေခြင်း
    results = await db.get_files(query)
    
    if results:
        is_admin = message.from_user.id == ADMIN_ID
        response_text = ""
        buttons = []

        for result in results:
            file_name = result.get("file_name", "N/A")
            file_size = result.get("file_size", "N/A")
            file_id = result.get("file_id")
            
            # User အတွက် ပြသမယ့်စာသား
            response_text += f"**🎬 Movie:** {file_name}\n"
            response_text += f"**🗂️ Size:** {file_size}\n\n"

            # Admin အတွက် link button ကိုပါ ထည့်ပေးခြင်း
            if is_admin and file_id:
                link = f"https://t.me/c/{os.environ.get('DATABASE_CHANNEL_ID').replace('-100', '')}/{file_id}"
                buttons.append([InlineKeyboardButton(f"🔗 {file_name}", url=link)])

        if is_admin:
            await message.reply_text(
                "**Admin Search Result:**\n\n" + response_text,
                reply_markup=InlineKeyboardMarkup(buttons) if buttons else None,
                disable_web_page_preview=True
            )
        else:
            await message.reply_text("**Search Result:**\n\n" + response_text)

    else:
        await message.reply_text("Sorry, no movies were found with that name.")

search_message_handler = MessageHandler(search_message, filters.private & filters.text & ~filters.command(["start"]))
