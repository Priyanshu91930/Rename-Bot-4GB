import os
import asyncio
from pyrogram import Client, idle
from plugins.cb_data import app as Client2
from config import *
import pyromod
from fastapi import FastAPI
import uvicorn

PORT = int(os.environ.get("PORT", 10000))  # Render port

# FastAPI server for Render
app_fastapi = FastAPI()
@app_fastapi.get("/")
def root():
    return {"status": "Bot is running"}

# Initialize your bot(s)
bot = Client("Renamer", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH, plugins=dict(root='plugins'))

async def start_bots():
    """Start Pyrogram bots concurrently"""
    if STRING_SESSION:
        apps = [Client2, bot]
        for app in apps:
            await app.start()
        await idle()
        for app in apps:
            await app.stop()
    else:
        await bot.start()
        await idle()
        await bot.stop()

# Run FastAPI + Pyrogram together
async def main():
    # Run FastAPI server in background
    config = uvicorn.Config(app_fastapi, host="0.0.0.0", port=PORT, log_level="info")
    server = uvicorn.Server(config)
    api_task = asyncio.create_task(server.serve())
    
    # Run bot
    await start_bots()
    
    # Stop FastAPI when bot stops
    api_task.cancel()

if __name__ == "__main__":
    asyncio.run(main())
