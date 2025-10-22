from pyrogram import Client, idle
from plugins.cb_data import app as Client2
from config import *
import pyromod
import pyrogram.utils
import os
import asyncio
from fastapi import FastAPI
import uvicorn

pyrogram.utils.MIN_CHAT_ID = -999999999999
pyrogram.utils.MIN_CHANNEL_ID = -100999999999999

PORT = int(os.environ.get("PORT", 10000))  # Render port

# FastAPI server for Render
app_fastapi = FastAPI()

@app_fastapi.get("/")
def root():
    return {"status": "Bot is running"}

# Function to start your Pyrogram bots
async def start_bots():
    if STRING_SESSION:
        apps = [Client2, Client("Renamer", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH, plugins=dict(root='plugins'))]
        for app in apps:
            await app.start()
        await idle()  # Keep bots running
        for app in apps:
            await app.stop()
    else:
        bot = Client("Renamer", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH, plugins=dict(root='plugins'))
        await bot.start()
        await idle()
        await bot.stop()

# Run FastAPI + Pyrogram bot in same asyncio event loop
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(start_bots())
    uvicorn.run(app_fastapi, host="0.0.0.0", port=PORT)
