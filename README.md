# 🍎 Bad Apple via Telegram Reactions

<p align="center">
  <a href="https://www.youtube.com/watch?v=dVx61BrTRj0">
    <img src="https://img.youtube.com/vi/dVx61BrTRj0/hqdefault.jpg" alt="Смотреть Bad Apple!!" width="600">
  </a>
</p>

Plays Bad Apple animation through custom emoji reactions on any Telegram message — powered by a userbot.

![Python](https://img.shields.io/badge/python-3.10+-blue)
![Telethon](https://img.shields.io/badge/telethon-latest-green)

## How it works

Each frame of the animation is encoded as a custom emoji. The userbot sequentially sets reactions on a chosen message — one reaction replaces another every 3 seconds, creating the illusion of playback.

## Installation

```bash
git clone https://github.com/IRRatium/badapple-on-custom-reaction
cd badapple-on-custom-reaction
pip install telethon python-dotenv
```

Create a `.env` file:

```env
API_ID=12345678
API_HASH=your_api_hash_here
```

Get `API_ID` and `API_HASH` at [my.telegram.org](https://my.telegram.org).

## Running

```bash
python player.py
```

On first launch Telethon will ask for your phone number, code, and 2FA (if set). The session is saved to `userbot.session` and won't ask again.

## Commands

Commands are sent **from your own account** in any chat (the userbot only listens to outgoing messages).

| Command | Action |
|---|---|
| `/launch` *(as a reply)* | Start animation on the replied-to message |
| `/stop` | Stop playback |
| `/start` | Show status |

Only one animation can play at a time. `/launch` is blocked while another session is active — use `/stop` first.

---

## 🎞 Cutter (cutter.py)

A Telegram bot that takes a video and automatically produces a ready-to-use `REACTION_EMOJIS` array for the player.

### How it works

1. Receives a video from the user
2. Splits it into 3-second chunks using `ffmpeg`
3. Converts each chunk to a square 100×100 WebM (custom emoji format)
4. Creates a private `custom_emoji` sticker pack and uploads all chunks
5. Returns an `emojis.txt` file with the array ready to paste into `player.py`

### Installation

```bash
pip install python-telegram-bot python-dotenv
```

`ffmpeg` and `ffprobe` are required:

```bash
# Debian/Ubuntu
sudo apt install ffmpeg

# Arch
sudo pacman -S ffmpeg

# macOS
brew install ffmpeg
```

Add to `.env`:

```env
CUTTER_TOKEN=your_cutter_bot_token
```

Create the bot via [@BotFather](https://t.me/BotFather). The user sending the video must be the owner of the sticker pack being created.

### Running

```bash
python cutter.py
```

Send any video to the bot — you'll get back an `emojis.txt` file with the ready array and a link to the created pack. Paste the contents into `player.py` as `REACTION_EMOJIS`.

---

## Project structure

```
.
├── player.py            # Userbot player
├── cutter.py            # Cutter bot
├── temp_reaction_tiles/ # Temporary frames during cutting (.gitignore)
├── .env                 # Secrets (.gitignore)
├── .env.example         # Config example
└── userbot.session      # Telethon session (.gitignore)
```

## Requirements

- Python 3.10+
- ffmpeg (for the cutter)
- Telegram account with **Telegram Premium** (required for custom emoji reactions)
