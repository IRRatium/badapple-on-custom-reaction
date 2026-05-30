import asyncio
import os
import random
from datetime import datetime
from dotenv import load_dotenv
from telethon import TelegramClient, events
from telethon.errors import FloodWaitError
from telethon.tl.functions.messages import SendReactionRequest
from telethon.tl.types import ReactionCustomEmoji

load_dotenv()

API_ID   = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

# === СЮДА ВСТАВЛЯЕШЬ МАССИВ ИЗ ТЕКСТОВОГО ФАЙЛА, КОТОРЫЙ ВЫДАСТ CUTTER ===
REACTION_EMOJIS = [
    "5242545520831927669",
    "5242572325722823011",
    "5242288363960048246",
    "5242225915135561370",
    "5242267108166900683",
    "5242608497937390244",
    "5242288681787626723",
    "5242601028989262469",
    "5242689539675301020",
    "5242616971907866264",
    "5242473481345471284",
    "5242275436108488330",
    "5242400282217847515",
    "5242653208546939074",
    "5242428457203307551",
    "5242639503306299701",
    "5242396330847933836",
    "5242588590763972015",
    "5242502498144525797",
    "5242486821513897677",
    "5242348218624283544",
    "5242239835124571944",
    "5242439173146715657",
    "5242690274114703760",
    "5242367524502280640",
    "5242421658270079711",
    "5242737102143134194",
    "5242639288557935930",
    "5242236004013742146",
    "5242349451279901026",
    "5242268512621207676",
    "5242397554913613158",
    "5242329144674523913",
    "5242622615494889936",
    "5242300943919261265",
    "5242533829930947916",
    "5242413240134178665",
    "5242486456441676148",
    "5242465492706305435",
    "5242399131166612543",
    "5242456237051778396",
    "5242468301614914144",
    "5242218192784365761",
    "5242575439574110946",
    "5242641938552758108",
    "5242747105121963623",
    "5242279151255196929",
    "5242327890544075423",
    "5242442377192316040",
    "5242301592459329067",
    "5242644292194834980",
    "5242529998820122183",
    "5242444374352110836",
    "5242701123202095812",
    "5242235256689433437",
    "5242345289456588681",
    "5242604190085191568",
    "5242207987942070672",
    "5242522577116634253",
    "5242275285784633801",
    "5242700255618701322",
    "5242646302239528543",
    "5242541646771426866",
    "5242217926496393799",
    "5242264243423713454",
    "5242385958501913101",
    "5242301991891280037",
    "5242613385610170624",
    "5242525398910145824",
    "5242410882197133643",
    "5242259076578056994",
    "5242511895532966851",
    "5242679532401500133",
    "5242592159881794220"
]

client = TelegramClient("userbot", API_ID, API_HASH)

# Только одна активная сессия в любой момент
active: dict[tuple, asyncio.Task] = {}
_lock = asyncio.Lock()


def log(msg: str):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")


async def run_animation(peer, peer_id: int, msg_id: int, chat_label: str):
    key = (peer_id, msg_id)
    log(f"▶ Старт  | чат={chat_label} msg_id={msg_id} | кадров={len(REACTION_EMOJIS)}")

    try:
        for idx, emoji_id in enumerate(REACTION_EMOJIS):
            if key not in active:
                log(f"■ Стоп   | чат={chat_label} msg_id={msg_id} | кадр={idx}")
                break

            try:
                await client(SendReactionRequest(
                    peer=peer,
                    msg_id=msg_id,
                    reaction=[ReactionCustomEmoji(document_id=int(emoji_id))],
                    big=True
                ))
            except Exception as e:
                log(f"! Ошибка | чат={chat_label} msg_id={msg_id} кадр={idx}: {e}")

            await asyncio.sleep(3.0)

        # Снимаем реакцию
        try:
            await client(SendReactionRequest(peer=peer, msg_id=msg_id, reaction=[]))
        except Exception as e:
            log(f"! Снятие реакции | чат={chat_label}: {e}")

        log(f"✓ Финиш  | чат={chat_label} msg_id={msg_id}")
    finally:
        active.pop(key, None)


@client.on(events.NewMessage(outgoing=True, pattern=r"^/start$"))
async def cmd_start(event):
    n = len(active)
    await event.reply(
        "👋 <b>Bad Apple Reaction Player</b>\n\n"
        f"📦 Кадров: <b>{len(REACTION_EMOJIS)}</b>\n"
        f"▶️ Активных сессий: <b>{n}</b>\n\n"
        "/launch (reply) — start animation on the replied-to message\n"
        "/stop — stop playback\n"
        "/start — show status",
        parse_mode="html"
    )


@client.on(events.NewMessage(outgoing=True, pattern=r"^/launch$"))
async def cmd_launch(event):
    if not event.reply_to_msg_id:
        await event.reply("↩️ Reply to a message to launch the animation on it.")
        return

    if active:
        await event.reply("⏳ Already playing. Use /stop first.")
        return

    target_msg_id = event.reply_to_msg_id
    peer      = await event.get_input_chat()
    chat_id   = event.chat_id
    key       = (chat_id, target_msg_id)

    # Получаем читаемое имя чата для логов
    try:
        chat = await event.get_chat()
        chat_label = getattr(chat, "title", None) or getattr(chat, "username", None) or str(chat_id)
    except Exception:
        chat_label = str(chat_id)

    await event.delete()

    task = asyncio.create_task(run_animation(peer, chat_id, target_msg_id, chat_label))
    active[key] = task


@client.on(events.NewMessage(outgoing=True, pattern=r"^/stop(all)?$"))
async def cmd_stop(event):
    if not active:
        await event.reply("💤 Nothing is playing.")
        return
    active.clear()
    await event.reply("🛑 Stopped.")
    log("■ Стоп (команда)")


async def main():
    await client.start()
    me = await client.get_me()
    log(f"✅ Юзербот запущен как @{me.username or me.first_name}")
    log("Отправь /launch в любом чате или ответом на сообщение.")
    await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
