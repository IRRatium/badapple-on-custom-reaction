# 🍎 Bad Apple via Telegram

<table>
<tr>
<td><a href="https://www.youtube.com/watch?v=dVx61BrTRj0"><img src="https://img.youtube.com/vi/dVx61BrTRj0/hqdefault.jpg" alt="Bad Apple — Reactions"/></a></td>
<td><a href="https://www.youtube.com/watch?v=CHtNMiuicRQ"><img src="https://img.youtube.com/vi/CHtNMiuicRQ/hqdefault.jpg" alt="Bad Apple — Status"/></a></td>
</tr>
<tr>
<td align="center">Reactions (<code>reaction.py</code>)</td>
<td align="center">Status (<code>status.py</code>)</td>
</tr>
</table>

Plays the Bad Apple animation through Telegram — powered by a userbot.  
Two playback modes are available:

| Mode | File | Where it plays |
|------|------|----------------|
| **Reactions** | `reaction.py` | Custom emoji reactions on any message |
| **Status** | `status.py` | Custom emoji in your profile status |

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Telethon](https://img.shields.io/badge/telethon-latest-green)

---

## How it works

**reaction.py** — Each frame of the animation is a custom emoji. The userbot sequentially sets reactions on a chosen message, replacing one emoji with another every few seconds to create the illusion of playback.

**status.py** — Same idea, but the emoji is set as your Telegram profile status emoji, so the animation plays directly on your avatar.

---

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

---

## Running

### Reaction player

Plays the animation as reactions on a message.

```bash
python reaction.py
```

Commands are sent **from your own account** in any chat (the userbot only listens to outgoing messages).

| Command | Action |
|---------|--------|
| `/launch` *(as a reply)* | Start animation on the replied-to message |
| `/stop` | Stop playback |
| `/start` | Show status |

Only one animation can play at a time. `/launch` is blocked while another session is active — use `/stop` first.

---

### Status player

Plays the animation as your profile status emoji.

```bash
python status.py
```

---

## 🎞 Cutter (cutter.py)

A Telegram bot that takes a video and automatically produces a ready-to-use `REACTION_EMOJIS` array for the players.

### How it works

1. Receives a video from the user
2. Splits it into chunks using `ffmpeg`
3. Converts each chunk to a square 100×100 WebM (custom emoji format)
4. Creates a private `custom_emoji` sticker pack and uploads all chunks
5. Returns an `emojis.txt` file with the array ready to paste into the player

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

Send any video to the bot — you'll get back an `emojis.txt` file with the ready array and a link to the created pack. Paste the contents into the player as `REACTION_EMOJIS`.

---

## Project structure

```
.
├── reaction.py          # Userbot player — reactions on a message
├── status.py            # Userbot player — profile status emoji
├── cutter.py            # Cutter bot
├── temp_reaction_tiles/ # Temporary frames during cutting (.gitignore)
├── .env                 # Secrets (.gitignore)
├── .env.example         # Config example
└── userbot.session      # Telethon session (.gitignore)
```

---

## Requirements

- Python 3.10+
- ffmpeg (for the cutter)
- Telegram account with **Telegram Premium** (required for custom emoji reactions and status)
