import os
import re
import sys
import json
import time
import asyncio
import requests
import subprocess

import core as helper
from utils import progress_bar
from vars import API_ID, API_HASH, BOT_TOKEN
from aiohttp import ClientSession
from pyromod import listen
from subprocess import getstatusoutput

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from pyrogram.errors.exceptions.bad_request_400 import StickerEmojiInvalid
from pyrogram.types.messages_and_media import message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


bot = Client(
    "bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN)


@bot.on_message(filters.command(["start"]))
async def start(bot: Client, m: Message):
    await m.reply_text(f"<b>Hello {m.from_user.mention} 👋\n\n I Am A Bot For Download Links From Your **.TXT** File And Then Upload That File On Telegram So Basically If You Want To Use Me First Send Me /upload Command And Then Follow Few Steps..\n\nUse /stop to stop any ongoing task.</b>")


@bot.on_message(filters.command("stop"))
async def restart_handler(_, m):
    await m.reply_text("**Stopped**🚦", True)
    os.execl(sys.executable, sys.executable, *sys.argv)


@bot.on_message(filters.command(["upload"]))
async def upload(bot: Client, m: Message):
    editable = await m.reply_text('𝕤ᴇɴᴅ ᴛxᴛ ғɪʟᴇ ⚡️')
    input: Message = await bot.listen(editable.chat.id)
    x = await input.download()
    await input.delete(True)

    path = f"./downloads/{m.chat.id}"

    try:
       with open(x, "r") as f:
           content = f.read()
       content = content.split("\n")
       links = []
       for i in content:
           links.append(i.split("://", 1))
       os.remove(x)
    except:
       await m.reply_text("**Invalid file input.**")
       os.remove(x)
       return
    
    await editable.edit(f"**𝕋ᴏᴛᴀʟ ʟɪɴᴋ𝕤 ғᴏᴜɴᴅ ᴀʀᴇ🔗🔗** **{len(links)}**\n\n**𝕊ᴇɴᴅ 𝔽ʀᴏᴍ ᴡʜᴇʀᴇ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ ɪɴɪᴛɪᴀʟ ɪ𝕤** **1**")
    input0: Message = await bot.listen(editable.chat.id)
    raw_text = input0.text
    await input0.delete(True)

    await editable.edit("**Now Please Send Me Your Batch Name**")
    input1: Message = await bot.listen(editable.chat.id)
    raw_text0 = input1.text
    await input1.delete(True)
    
    await editable.edit("**𝔼ɴᴛᴇʀ ʀᴇ𝕤ᴏʟᴜᴛɪᴏɴ📸**\n144,240,360,480,720,1080 please choose quality")
    input2: Message = await bot.listen(editable.chat.id)
    raw_text2 = input2.text
    await input2.delete(True)

    try:
        if raw_text2 == "144":
            res = "256x144"
        elif raw_text2 == "240":
            res = "426x240"
        elif raw_text2 == "360":
            res = "640x360"
        elif raw_text2 == "480":
            res = "854x480"
        elif raw_text2 == "720":
            res = "1280x720"
        elif raw_text2 == "1080":
            res = "1920x1080" 
        else: 
            res = "UN"
    except Exception:
        res = "UN"
    
    await editable.edit("Now Enter A Caption to add caption on your uploaded file")
    input3: Message = await bot.listen(editable.chat.id)
    raw_text3 = input3.text
    await input3.delete(True)
    highlighter = f"️ ⁪⁬⁮⁮⁮"
    if raw_text3 == 'Robin':
        MR = highlighter 
    else:
        MR = raw_text3
   
    await editable.edit("Now send the Thumb url/nEg » https://graph.org/file/ce1723991756e48c35aa1.jpg \n Or if don't want thumbnail send = no")
    input6 = message = await bot.listen(editable.chat.id)
    raw_text6 = input6.text
    await input6.delete(True)
    await editable.delete()

    thumb = input6.text
    if thumb.startswith("http://") or thumb.startswith("https://"):
        getstatusoutput(f"wget '{thumb}' -O 'thumb.jpg'")
        thumb = "thumb.jpg"
    else:
        thumb == "no"

    if len(links) == 1:
        count = 1
    else:
        count = int(raw_text)

    try:
        # Update this part to handle 403 errors properly
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        cookies = "cookies.txt"  # Ensure this file is available in your project directory

        for i in range(count - 1, len(links)):
            V = links[i][1].replace("file/d/", "uc?export=download&id=").replace("www.youtube-nocookie.com/embed", "youtu.be").replace("?modestbranding=1", "").replace("/view?usp=sharing", "")
            url = "https://" + V

            if "visionias" in url:
                async with ClientSession() as session:
                    async with session.get(url, headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8', 'Accept-Language': 'en-US,en;q=0.9', 'Cache-Control': 'no-cache', 'Connection': 'keep-alive', 'Pragma': 'no-cache', 'Referer': 'http://www.visionias.in/', 'Sec-Fetch-Dest': 'iframe', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'cross-site', 'Upgrade-Insecure-Requests': '1', 'User-Agent': user_agent}) as resp:
                        text = await resp.text()
                        url = re.search(r"(https://.*?playlist.m3u8.*?)\"", text).group(1)

            elif 'videos.classplusapp' in url:
                url = requests.get(f'https://api.classplusapp.com/cams/uploader/video/jw-signed-url?url={url}', headers={'x-access-token': 'your_token'}).json()['url']

            elif '/master.mpd' in url:
                id =  url.split("/")[-2]
                url =  "https://d26g5bnklkwsh4.cloudfront.net/" + id + "/master.m3u8"

            name1 = links[i][0].replace("\t", "").replace(":", "").replace("/", "").replace("+", "").replace("#", "").replace("|", "").replace("@", "").replace("*", "").replace(".", "").replace("https", "").replace("http", "").strip()
            name = f'{str(count).zfill(3)}) {name1[:60]}'

            if "youtu" in url:
                ytf = f"b[height<={raw_text2}][ext=mp4]/bv[height<={raw_text2}][ext=mp4]+ba[ext=m4a]/b[ext=mp4]"
            else:
                ytf = f"b[height<={raw_text2}]/bv[height<={raw_text2}]+ba/b/bv+ba"

            # Command update
            if "jw-prod" in url:
                cmd = f'yt-dlp -o "{name}.mp4" "{url}" --user-agent "{user_agent}"'
            else:
                cmd = f'yt-dlp -f "{ytf}" "{url}" -o "{name}.mp4" --user-agent "{user_agent}" --cookies {cookies} -R 10 --fragment-retries 10'

            try:
                cc = f'**[📽️] Vid_ID:** {str(count).zfill(3)}.** {name1}{MR}.mkv\n**𝔹ᴀᴛᴄʜ** » **{raw_text0}**'
                cc1 = f'**[📁] Pdf_ID:** {str(count).zfill(3)}. {name1}{MR}.pdf \n**𝔹ᴀᴛᴄʜ** » **{raw_text0}**'
                
                # Download and send logic remains the same
                if "drive" in url:
                    try:
                        ka = await helper.download(url, name)
                        copy = await bot.send_document(chat_id=m.chat.id, document=ka, caption=cc1)
                        count += 1
                        os.remove(ka)
                        time.sleep(1)
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        continue

                # Further code for downloading and sending media remains unchanged...
                else:
                    Show = f"**⥥ 🄳🄾🅆🄽🄻🄾🄰🄳🄸🄽🄶⬇️⬇️... »**\n\n**📝Name »** `{name}\n❄Quality » {raw_text2}`\n\n**🔗URL »** `{url}`"
                    prog = await m.reply_text(Show)
                    res_file = await helper.download_video(url, cmd, name)
                    filename = res_file
                    await prog.delete(True)
                    await helper.send_vid(bot, m, cc, filename, thumb, name, prog)
                    count += 1
                    time.sleep(1)

            except Exception as e:
                await m.reply_text(f"**downloading Interupted **\n{str(e)}\n**Name** » {name}\n**Link** » `{url}`")
                continue

    except Exception as e:
        await m.reply_text(e)
    await m.reply_text("**𝔻ᴏɴᴇ 𝔹ᴏ𝕤𝕤😎**")

bot.run()
