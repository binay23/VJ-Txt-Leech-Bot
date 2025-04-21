# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

import os
import re
import sys
import time
import requests
import asyncio
import subprocess

from pyrogram import Client, filters
from pyrogram.types import Message
from aiohttp import ClientSession
from pyromod import listen
from subprocess import getstatusoutput

from vars import API_ID, API_HASH, BOT_TOKEN

bot = Client(
    "bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN)

@bot.on_message(filters.command(["start"]))
async def start(bot: Client, m: Message):
    await m.reply_text(f"<b>Hello {m.from_user.mention} 👋\n\n I Am A Bot For Download Links From Your **.TXT** File And Then Upload That File On Telegram.\n\nUse /upload to start. Use /stop to restart the bot.</b>")

@bot.on_message(filters.command("stop"))
async def restart_handler(_, m):
    await m.reply_text("**Stopped**🚦", True)
    os.execl(sys.executable, sys.executable, *sys.argv)

@bot.on_message(filters.command(["upload"]))
async def upload(bot: Client, m: Message):
    editable = await m.reply_text('Send .txt file')
    input: Message = await bot.listen(editable.chat.id)
    file = await input.download()
    await input.delete(True)

    try:
        with open(file, "r", encoding="utf-8") as f:
            content = f.read().strip().splitlines()
        links = []
        for line in content:
            if ":" in line:
                name, url = line.split(":", 1)
                links.append((name.strip(), url.strip()))
        os.remove(file)
    except Exception as e:
        await m.reply_text(f"Invalid file format.\nError: {e}")
        os.remove(file)
        return

    await editable.edit(f"Found **{len(links)}** links.\nSend the starting index (default is 1):")
    input0 = await bot.listen(editable.chat.id)
    start_index = int(input0.text.strip()) if input0.text.strip().isdigit() else 1
    await input0.delete()

    await editable.edit("Send Batch Name:")
    input1 = await bot.listen(editable.chat.id)
    batch = input1.text.strip()
    await input1.delete()

    await editable.edit("Enter resolution (144/240/360/480/720/1080):")
    input2 = await bot.listen(editable.chat.id)
    resolution = input2.text.strip()
    await input2.delete()

    height_map = {
        "144": "256x144",
        "240": "426x240",
        "360": "640x360",
        "480": "854x480",
        "720": "1280x720",
        "1080": "1920x1080"
    }
    res = height_map.get(resolution, "640x360")

    await editable.edit("Enter caption (or type 'Robin'):")
    input3 = await bot.listen(editable.chat.id)
    raw_caption = input3.text.strip()
    await input3.delete()
    MR = "️ ⁪⁬⁮⁮⁮" if raw_caption.lower() == "robin" else raw_caption

    await editable.edit("Send thumbnail URL (or type 'no'):")
    input4 = await bot.listen(editable.chat.id)
    thumb_url = input4.text.strip()
    await input4.delete()
    await editable.delete()

    thumb_path = "thumb.jpg"
    if thumb_url.startswith("http"):
        os.system(f"wget '{thumb_url}' -O '{thumb_path}'")
    else:
        thumb_path = None

    count = start_index
    for name, url in links[start_index - 1:]:
        safe_name = re.sub(r'[<>:"/\\|?*]', "", name)
        base_name = f"{str(count).zfill(3)}) {safe_name[:60]}"

        try:
            if url.endswith(".pdf"):
                file_path = f"{base_name}.pdf"
                r = requests.get(url, stream=True)
                with open(file_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
                await bot.send_document(m.chat.id, document=file_path, caption=f"{base_name}{MR}\nBatch: {batch}")
                os.remove(file_path)

            elif url.endswith(".m3u8"):
                file_path = f"{base_name}.mp4"
                ffmpeg_cmd = f'ffmpeg -y -i "{url}" -c copy -bsf:a aac_adtstoasc "{file_path}"'
                res = subprocess.run(ffmpeg_cmd, shell=True)
                if not os.path.exists(file_path):
                    raise Exception("Download failed")
                await bot.send_video(m.chat.id, video=file_path, caption=f"{base_name}{MR}\nBatch: {batch}", thumb=thumb_path if thumb_path else None)
                os.remove(file_path)

            else:
                yt_cmd = f'yt-dlp -f "b[height<={resolution}]" "{url}" -o "{base_name}.mp4"'
                subprocess.run(yt_cmd, shell=True)
                await bot.send_video(m.chat.id, video=f"{base_name}.mp4", caption=f"{base_name}{MR}\nBatch: {batch}", thumb=thumb_path if thumb_path else None)
                os.remove(f"{base_name}.mp4")

            count += 1
            time.sleep(1)

        except Exception as e:
            await m.reply_text(f"Download failed:\n{e}\nName: {base_name}\nURL: {url}")
            continue

    await m.reply("**All Done Boss!**")

bot.run()
