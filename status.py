import asyncio
import os
from datetime import datetime
from dotenv import load_dotenv
from telethon import TelegramClient, events
from telethon.tl.functions.account import UpdateEmojiStatusRequest
from telethon.tl.types import EmojiStatus, EmojiStatusEmpty

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

# None — не играет, Task — активная анимация
active: asyncio.Task | None = None


def log(msg: str):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")


async def run_animation():
    global active
    log(f"▶ Старт  | кадров={len(REACTION_EMOJIS)}")

    try:
        for idx, emoji_id in enumerate(REACTION_EMOJIS):
            if active is None:
                log(f"■ Стоп   | кадр={idx}")
                break

            try:
                await client(UpdateEmojiStatusRequest(
                    emoji_status=EmojiStatus(document_id=int(emoji_id))
                ))
            except Exception as e:
                log(f"! Ошибка | кадр={idx}: {e}")

            await asyncio.sleep(3.0)

        # Снимаем статус по завершении
        try:
            await client(UpdateEmojiStatusRequest(emoji_status=EmojiStatusEmpty()))
        except Exception as e:
            log(f"! Снятие статуса: {e}")

        log("✓ Финиш")
    finally:
        active = None


@client.on(events.NewMessage(outgoing=True, pattern=r"^/start$"))
async def cmd_start(event):
    status = "▶️ Играет" if active is not None else "💤 Не активно"
    await event.reply(
        "👋 <b>Bad Apple Status Player</b>\n\n"
        f"📦 Кадров: <b>{len(REACTION_EMOJIS)}</b>\n"
        f"Статус: <b>{status}</b>\n\n"
        "/launch — запустить анимацию в статусе профиля\n"
        "/stop — остановить\n"
        "/start — показать статус",
        parse_mode="html"
    )


@client.on(events.NewMessage(outgoing=True, pattern=r"^/launch$"))
async def cmd_launch(event):
    global active

    if active is not None:
        await event.reply("⏳ Уже играет. Используй /stop сначала.")
        return

    await event.delete()
    active = asyncio.create_task(run_animation())


@client.on(events.NewMessage(outgoing=True, pattern=r"^/stop(all)?$"))
async def cmd_stop(event):
    global active

    if active is None:
        await event.reply("💤 Ничего не играет.")
        return

    active = None
    await event.reply("🛑 Остановлено.")
    log("■ Стоп (команда)")


async def main():
    await client.start()
    me = await client.get_me()
    log(f"✅ Юзербот запущен как @{me.username or me.first_name}")
    log("Отправь /launch чтобы запустить анимацию в статусе профиля.")
    await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
