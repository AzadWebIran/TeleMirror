import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession

api_id = int(input('API ID: '))
api_hash = input('API Hash: ')

async def main():
    async with TelegramClient(StringSession(), api_id, api_hash) as client:
        print('\nSESSION STRING (copy this to GitHub Secrets as TELEGRAM_SESSION):')
        print(client.session.save())

asyncio.run(main())
