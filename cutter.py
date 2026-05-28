import os
import asyncio
import shutil
import math
import subprocess
from uuid import uuid4
from dotenv import load_dotenv
from telegram import Update, InputSticker
from telegram.constants import ParseMode, StickerFormat
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

load_dotenv()

TOKEN = os.getenv("CUTTER_TOKEN")
TEMP_DIR = "temp_reaction_tiles"
os.makedirs(TEMP_DIR, exist_ok=True)

PART_DURATION = 3.0  # Каждая реакция длится 3 секунды

def ffprobe_duration(video_path):
    probe = subprocess.run(
        ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
         '-of', 'default=noprint_wrappers=1:nokey=1', video_path],
        capture_output=True, text=True
    )
    try:
        return float(probe.stdout.strip())
    except:
        return 0.0

def make_reaction_webm(video_path, out_webm, start_sec, duration):
    """Вырезает кусок видео, делает его квадратным 100x100 и жмет в WebM для Telegram"""
    subprocess.run([
        'ffmpeg', '-y', '-ss', str(start_sec), '-i', video_path,
        '-t', str(duration),
        # Делаем квадратным (crop) и сжимаем до 100x100, принудительно 60 fps (или 30)
        '-vf', 'crop=ih:ih,scale=100:100:flags=lanczos,fps=60',
        '-c:v', 'libvpx-vp9', '-b:v', '0', '-crf', '42',
        '-auto-alt-ref', '0', '-deadline', 'realtime', '-cpu-used', '8', '-an',
        out_webm
    ], capture_output=True)
    return os.path.exists(out_webm) and os.path.getsize(out_webm) > 0

async def receive_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    video = update.message.video or update.message.animation or update.message.document
    if not video:
        return

    user_id = update.effective_user.id
    bot = context.bot
    
    unique_id = uuid4().hex[:6]
    user_dir = os.path.join(TEMP_DIR, f"{user_id}_{unique_id}")
    os.makedirs(user_dir, exist_ok=True)
    
    video_path = os.path.join(user_dir, "input.mp4")
    status_msg = await update.message.reply_text("📥 <b>Скачиваю видео для реакций...</b>", parse_mode=ParseMode.HTML)

    file = await video.get_file()
    await file.download_to_drive(video_path)

    await status_msg.edit_text("🔍 <b>Анализирую тайминги...</b>", parse_mode=ParseMode.HTML)
    duration = ffprobe_duration(video_path)
    
    if duration <= 0:
        await status_msg.edit_text("❌ Ошибка анализа видео.")
        return

    num_parts = math.ceil(duration / PART_DURATION)
    bot_me = await bot.get_me()
    
    pack_name = f"ba_{unique_id}_by_{bot_me.username}"[:64].rstrip('_')
    pack_title = f"Bad Apple Reactions {unique_id}"

    await status_msg.edit_text(f"🎞 <b>Нарезаю {num_parts} фрагментов по 3с...</b>", parse_mode=ParseMode.HTML)

    sticker_objects = []
    
    for i in range(num_parts):
        start_sec = i * PART_DURATION
        dur = min(PART_DURATION, duration - start_sec)
        webm_path = os.path.join(user_dir, f"part_{i}.webm")
        
        # Рендерим кусок видео
        make_reaction_webm(video_path, webm_path, start_sec, dur)
        sticker_objects.append(webm_path)

    await status_msg.edit_text("🚀 <b>Создаю пак и загружаю все реакции...</b>\nЭто займет какое-то время из-за лимитов.", parse_mode=ParseMode.HTML)

    # Создаем пак с первым фрагментом
    first_file = open(sticker_objects[0], 'rb')
    await bot.create_new_sticker_set(
        user_id=user_id,
        name=pack_name,
        title=pack_title,
        stickers=[InputSticker(first_file, ["🔥"], format=StickerFormat.VIDEO)],
        sticker_type="custom_emoji"
    )
    first_file.close()

    # Добавляем все остальные фрагменты в этот же пак
    for idx, path in enumerate(sticker_objects[1:], start=1):
        await status_msg.edit_text(f"🚀 <b>Загрузка: {idx + 1}/{num_parts} фрагментов...</b>", parse_mode=ParseMode.HTML)
        with open(path, 'rb') as f:
            await bot.add_sticker_to_set(
                user_id=user_id,
                name=pack_name,
                sticker=InputSticker(f, ["🔥"], format=StickerFormat.VIDEO)
            )

    # Вытаскиваем ID созданных эмодзи, чтобы сформировать готовый массив для плеера
    sset = await bot.get_sticker_set(pack_name)
    emoji_ids = [s.custom_emoji_id for s in sset.stickers]

    # Генерируем кусок кода для вставки в бота-плеера
    formatted_ids = ",\n    ".join([f'"{eid}"' for eid in emoji_ids])
    code_output = f"REACTION_EMOJIS = [\n    {formatted_ids}\n]"
    
    # Сохраняем текстовый файл с готовым массивом
    txt_path = os.path.join(user_dir, "emojis.txt")
    with open(txt_path, "w") as f:
        f.write(code_output)

    await bot.send_document(
        chat_id=update.effective_chat.id,
        document=open(txt_path, 'rb'),
        caption=f"✅ <b>Готово!</b>\nПак: t.me/addemoji/{pack_name}\n\nВнутри файла готовый массив <code>REACTION_EMOJIS</code> для твоего плеера!"
    )
    
    shutil.rmtree(user_dir, ignore_errors=True)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.VIDEO | filters.Document.VIDEO, receive_video))
    print("Cutter для реакций запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
