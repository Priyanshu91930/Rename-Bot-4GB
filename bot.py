from pyrogram import Client, idle
from plugins.cb_data import app as Client2
from config import *
import pyromod
import pyrogram.utils
import os
import asyncio
from fastapi import FastAPI
import uvicorn

# Minimum chat/channel IDs
pyrogram.utils.MIN_CHAT_ID = -999999999999
pyrogram.utils.MIN_CHANNEL_ID = -100999999999999

# --- Read Render port ---
PORT = int(os.environ.get("PORT", 10000))  # Render provides $PORT automatically

# --- Create minimal FastAPI server for Render ---
app_fastapi = FastAPI()

@app_fastapi.get("/")
def root():
    return {"status": "Bot is running"}

# --- Initialize Pyrogram bot ---
bot = Client(
    "Renamer",
    bot_token=BOT_TOKEN,
    api_id=API_ID,
    api_hash=API_HASH,
    plugins=dict(root='plugins')
)

async def start_bots():
    """Start bots in background for STRING_SESSION or normal bot."""
    if STRING_SESSION:
        apps = [Client2, bot]
        for app in apps:
            await app.start()
        # Keep bots running
        await idle()
        for app in apps:
            await app.stop()
    else:
        await bot.start()
        await idle()
        await bot.stop()

# --- Run both FastAPI server and Pyrogram bot ---
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(start_bots())
    uvicorn.run(app_fastapi, host="0.0.0.0", port=PORT)
