# Telegram Archive

Automatically fetches posts from multiple Telegram channels every hour and archives them as Markdown files in this repository.

## Structure

```
archive/
  channel_name/
    YYYYMMDD.md   ← all posts from that day, appended each hour
```

Each message is formatted as:

```
HH:MM:SS
message text
```

## How it works

A GitHub Actions workflow runs at 5 minutes past every hour, reads channel names from `channels.csv`, fetches the previous full hour of posts from each channel, and appends them to the corresponding archive file.

## Setup

1. Obtain Telegram API credentials at https://my.telegram.org
2. Generate a session string using `run_once_locally.py` (run locally, never commit)
3. Add the following secrets to **Settings > Secrets > Actions**:

| Secret | Description |
|---|---|
| `TELEGRAM_API_ID` | Integer API ID from my.telegram.org |
| `TELEGRAM_API_HASH` | API hash string from my.telegram.org |
| `TELEGRAM_SESSION` | Telethon StringSession output |

4. Create a `channels.csv` file in the repo root with one channel username or ID per row:

```
my_channel
another_channel
```

5. Trigger the workflow manually from the **Actions** tab to verify.
