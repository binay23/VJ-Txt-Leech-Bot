import os
import sys
import time
import asyncio
import re
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from aiohttp import ClientSession
from utils import helper, progress_bar
from vars import API_ID, API_HASH, BOT_TOKEN
from pyrogram.types.messages_and_media import message
from pyromod import listen

bot = Client(
    "bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

async def download_thumbnail(url: str):
    async with ClientSession() as session:
        async with session.get(url) as resp:
            with open("thumb.jpg", "wb") as f:
                f.write(await resp.read())
    return "thumb.jpg"

def safe_remove(file_path):
    try:
        os.remove(file_path)
    except OSError as e:
        print(f"Error removing file {file_path}: {e}")

@bot.on_message(filters.command(["start"]))
async def start(bot: Client, m: Message):
    await m.reply_text(f"<b>Hello {m.from_user.mention} 👋\n\nI Am A Bot For Download Links From Your **.TXT** File...")

@bot.on_message(filters.command("stop"))
async def stop_handler(_, m):
    await m.reply_text("**Stopped**🚦", True)
    os.execl(sys.executable, sys.executable, *sys.argv)

@bot.on_message(filters.command(["upload"]))
async def upload(bot: Client, m: Message):
    editable = await m.reply_text('𝕤ᴇɴᴅ ᴛxᴛ ғɪʟᴇ ⚡️')
    input: Message = await bot.listen(editable.chat.id)
    x = await input.download()
    await input.delete(True)

    try:
        links = await process_file_links(x, m)
        safe_remove(x)  # Remove the file after processing
    except Exception as e:
        await m.reply_text(f"Error processing the file: {str(e)}")
        return
    
    if len(links) == 0:
        await m.reply_text("No valid links found!")
        return

    # Continue processing links, prompts for quality, etc.
    await editable.edit(f"**𝕋ᴏᴛᴀʟ ʟɪɴᴋ𝕤: {len(links)}**")
    # Handle further inputs like batch name, quality, etc.

    await m.reply_text("Done! 😎")

bot.run()
