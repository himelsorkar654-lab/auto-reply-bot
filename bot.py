from telethon import TelegramClient, events
import time
import os

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")

client = TelegramClient("session", api_id, api_hash)

auto_reply_on = True
last_active = time.time()
replied_users = {}

INACTIVE_TIME = 300
REPLY_COOLDOWN = 60

@client.on(events.NewMessage(outgoing=True))
async def update_active(event):
    global last_active, auto_reply_on
    last_active = time.time()

    if event.raw_text == ".off":
        auto_reply_on = False
        await event.edit("❌ Auto Reply OFF")

    elif event.raw_text == ".on":
        auto_reply_on = True
        await event.edit("✅ Auto Reply ON")

@client.on(events.NewMessage(incoming=True))
async def handler(event):
    global auto_reply_on

    if not auto_reply_on:
        return

    if time.time() - last_active < INACTIVE_TIME:
        return

    sender = await event.get_sender()

    if sender.bot:
        return

    user_id = sender.id

    if user_id in replied_users:
        if time.time() - replied_users[user_id] < REPLY_COOLDOWN:
            return

    replied_users[user_id] = time.time()

    await event.reply("👋 আমি এখন অফলাইনে আছি, পরে রিপ্লাই দিবো 😊")

client.start()
client.run_until_disconnected()
