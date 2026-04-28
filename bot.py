from telethon import TelegramClient, events
import time
import os
import random

api_id = int(os.getenv("32641525"))
api_hash = os.getenv("dee5359a46e465e7a699161071bcff44")

client = TelegramClient("session", api_id, api_hash)

auto_reply_on = True
night_mode = False
last_active = time.time()
replied_users = {}

INACTIVE_TIME = 10
REPLY_COOLDOWN = 5

# 👑 VIP user (তুমি)
VIP_USERS = [7509752074]

# 💬 Multiple replies
REPLIES = [
    "👋 আমি এখন অফলাইনে আছি, পরে রিপ্লাই দিবো 😊",
    "⏳ একটু ব্যস্ত আছি, কিছুক্ষণ পরে রিপ্লাই দিবো 👍",
    "🙏 এখন available না, পরে কথা বলবো ইনশাআল্লাহ",
    "📩 আপনার মেসেজ পেয়েছি, একটু পরে reply দিবো 😊"
]

@client.on(events.NewMessage(outgoing=True))
async def update_active(event):
    global last_active, auto_reply_on, night_mode
    last_active = time.time()

    if event.raw_text == ".off":
        auto_reply_on = False
        await event.edit("❌ Auto Reply OFF")

    elif event.raw_text == ".on":
        auto_reply_on = True
        await event.edit("✅ Auto Reply ON")

    elif event.raw_text == ".night":
        night_mode = True
        await event.edit("🌙 Night Mode ON")

    elif event.raw_text == ".day":
        night_mode = False
        await event.edit("☀️ Night Mode OFF")

@client.on(events.NewMessage(incoming=True))
async def handler(event):
    global auto_reply_on

    if not auto_reply_on:
        return

    sender = await event.get_sender()

    if sender.bot:
        return

    user_id = sender.id

    # 👑 VIP skip (তোমাকে auto reply দিবে না)
    if user_id in VIP_USERS:
        return

    # 🌙 Night mode (always reply)
    if night_mode:
        reply_text = random.choice(REPLIES)
        await event.reply(reply_text)
        return

    # ⏳ Inactive check
    if time.time() - last_active < INACTIVE_TIME:
        return

    # 🔁 Cooldown
    if user_id in replied_users:
        if time.time() - replied_users[user_id] < REPLY_COOLDOWN:
            return

    replied_users[user_id] = time.time()

    reply_text = random.choice(REPLIES)
    await event.reply(reply_text)

client.start()
client.run_until_disconnected()
