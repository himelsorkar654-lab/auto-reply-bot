from telethon import TelegramClient, events
import os
import time

api_id = int(os.getenv("32641525"))
api_hash = os.getenv("dee5359a46e465e7a699161071bcff44")

client = TelegramClient("session", api_id, api_hash)

last_seen = time.time()

@client.on(events.NewMessage(outgoing=True))
async def active(event):
    global last_seen
    last_seen = time.time()

@client.on(events.NewMessage(incoming=True))
async def reply(event):
    global last_seen

    if time.time() - last_seen < 60:
        return

    await event.reply("👋 আমি এখন অফলাইনে আছি, পরে রিপ্লাই দিবো 😊")

client.start()
client.run_until_disconnected()
