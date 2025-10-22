from pyrogram import Client, filters
from pyrogram.enums import MessageMediaType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply

@Client.on_message(filters.private & filters.reply)
async def refunc(client, message):
    reply_message = message.reply_to_message
    if (reply_message.reply_markup) and isinstance(reply_message.reply_markup, ForceReply):
        new_name = message.text
        await message.delete()
        msg = await client.get_messages(message.chat.id, reply_message.id)
        file = msg.reply_to_message

        # --- Safe media access ---
        media = getattr(file, "media", None)
        if not media:
            await message.reply("❌ Could not detect media in the replied message.")
            return

        # Get file object safely
        file_obj = getattr(file, media.value, None)
        file_name = getattr(file_obj, "file_name", None)

        # Add extension if missing
        if not "." in new_name:
            if file_name and "." in file_name:
                extn = file_name.rsplit('.', 1)[-1]
            else:
                extn = "mkv"
            new_name = new_name + "." + extn

        await reply_message.delete()

        # --- Buttons ---
        button = [[InlineKeyboardButton("📁 Document", callback_data="upload_document")]]
        if media in [MessageMediaType.VIDEO, MessageMediaType.DOCUMENT]:
            button.append([InlineKeyboardButton("🎥 Video", callback_data="upload_video")])
        elif media == MessageMediaType.AUDIO:
            button.append([InlineKeyboardButton("🎵 Audio", callback_data="upload_audio")])

        await message.reply(
            text=f"**Select The Output File Type**\n\n**File Name :-** `{new_name}`",
            reply_to_message_id=file.id,
            reply_markup=InlineKeyboardMarkup(button)
        )
