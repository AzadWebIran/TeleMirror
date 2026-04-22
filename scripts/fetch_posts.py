import asyncio
import csv
import os
import sys
from datetime import datetime, timedelta
from telethon import TelegramClient
from telethon.sessions import StringSession

required = {
    'TELEGRAM_API_ID': os.environ.get('TELEGRAM_API_ID'),
    'TELEGRAM_API_HASH': os.environ.get('TELEGRAM_API_HASH'),
    'TELEGRAM_SESSION': os.environ.get('TELEGRAM_SESSION'),
}

missing = [k for k, v in required.items() if not v]
if missing:
    print(f"Missing required env vars: {', '.join(missing)}")
    sys.exit(1)

API_ID = int(required['TELEGRAM_API_ID'])
API_HASH = required['TELEGRAM_API_HASH']
SESSION = required['TELEGRAM_SESSION']

CHANNELS_CSV = os.environ.get('CHANNELS_CSV', 'channels.csv')

now = datetime.utcnow()
end = now.replace(minute=0, second=0, microsecond=0)
start = end - timedelta(hours=1)


def read_channels(path):
    channels = []
    with open(path, newline='', encoding='utf-8') as f:
        for row in csv.reader(f):
            if row and row[0].strip():
                channels.append(row[0].strip())
    return channels


async def fetch_channel(client, channel):
    try:
        entity = await client.get_entity(channel)
    except Exception as e:
        print(f"Failed to resolve channel '{channel}': {e}")
        return

    messages = []
    async for m in client.iter_messages(entity, offset_date=end):
        msg_time = m.date.replace(tzinfo=None)
        if msg_time < start:
            break
        messages.append(m)
    messages.reverse()

    if not messages:
        print(f"No posts for '{channel}' in this window.")
        return

    channel_name = getattr(entity, 'username', None) or str(entity.id)

    by_date = {}
    for m in messages:
        date_key = m.date.strftime('%Y%m%d')
        by_date.setdefault(date_key, []).append(m)

    for date_key, msgs in by_date.items():
        path = f'archive/{channel_name}/{date_key}.md'
        os.makedirs(f'archive/{channel_name}', exist_ok=True)

        with open(path, 'a', encoding='utf-8') as f:
            for m in msgs:
                time_str = m.date.strftime('%H:%M:%S')
                text = (m.message or '').strip() or '[no text]'
                f.write(f'\n{time_str}\n{text}\n')

        print(f"Wrote {len(msgs)} posts to {path}")


async def main():
    if not os.path.exists(CHANNELS_CSV):
        print(f"Channels file not found: {CHANNELS_CSV}")
        sys.exit(1)

    channels = read_channels(CHANNELS_CSV)
    if not channels:
        print("No channels found in CSV.")
        sys.exit(0)

    async with TelegramClient(StringSession(SESSION), API_ID, API_HASH) as client:
        for channel in channels:
            await fetch_channel(client, channel)


asyncio.run(main())
