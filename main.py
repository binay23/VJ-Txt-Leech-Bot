import os
import asyncio
import aiohttp
import aiofiles
import subprocess
from pyrogram import Client, filters
from pyrogram.types import Message
import requests
from bs4 import BeautifulSoup
from yt_dlp import YoutubeDL

bot = Client("my_bot", api_id=123456, api_hash="your_api_hash", bot_token="your_bot_token")

async def get_direct_link(url):
    try:
        ydl_opts = {
            "quiet": True,
            "skip_download": True,
            "forceurl": True,
            "no_warnings": True,
            "simulate": True,
            "format": "best",
        }
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return info["url"]
    except Exception as e:
        print(f"Error getting direct link: {e}")
        return None

async def download_file(url, filename):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    async with aiofiles.open(filename, mode="wb") as f:
                        await f.write(await resp.read())
                    return filename
    except Exception as e:
        print(f"Download failed: {e}")
    return None

@bot.on_message(filters.command("get") & filters.private)
async def get_media(client: Client, message: Message):
    try:
        text = message.text.split(" ", 1)[1]
        soup = BeautifulSoup(text, "html.parser")
        results = soup.find_all("b")

        for i in range(0, len(results), 2):
            name = results[i].text.strip()
            url = results[i + 1].text.strip()
            await message.reply(f"Uploading ... - {name}")

            # Fix: Handle PDFs and Google Drive
            if "drive" in url or url.endswith(".pdf"):
                file_path = await download_file(url, f"{name}.pdf")
                if file_path:
                    await message.reply_document(document=file_path, caption=name)
                    os.remove(file_path)
                else:
                    await message.reply(f"❌ Failed to download {name}")
                continue

            # For video/audio links
            direct_link = await get_direct_link(url)
            if direct_link:
                output_file = f"{name}.mp4"
                process = await asyncio.create_subprocess_exec(
                    "ffmpeg",
                    "-i", direct_link,
                    "-c", "copy",
                    output_file,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )
                _, stderr = await process.communicate()
                if process.returncode == 0:
                    await message.reply_video(video=output_file, caption=name)
                    os.remove(output_file)
                else:
                    await message.reply(f"⚠️ Downloading Interrupted\n`{stderr.decode().strip()}`\nName » {name}\nLink » {url}")
            else:
                await message.reply(f"❌ Could not extract direct link for {name}")
    except Exception as e:
        await message.reply(f"🚫 Error: {e}")

bot.run()
