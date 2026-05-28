# 🍎 Bad Apple via Telegram Reactions

Проигрывает анимацию Bad Apple через кастомные эмодзи-реакции на любое сообщение в Telegram — прямо из-под юзербота.

![Python](https://img.shields.io/badge/python-3.10+-blue)
![Telethon](https://img.shields.io/badge/telethon-latest-green)

## Как это работает

Каждый кадр анимации закодирован как кастомный эмодзи. Юзербот последовательно ставит реакции на выбранное сообщение — одна реакция в секунду заменяет другую, создавая иллюзию воспроизведения.

## Установка

```bash
git clone https://github.com/IRRatium/badapple-on-custom-reaction
cd badapple-on-custom-reaction
pip install telethon python-dotenv
```

Создай `.env`:

```env
API_ID=12345678
API_HASH=your_api_hash_here
```

`API_ID` и `API_HASH` берёшь на [my.telegram.org](https://my.telegram.org).

## Запуск

```bash
python player.py
```

При первом запуске Telethon попросит номер телефона, код и 2FA (если есть). Сессия сохранится в `userbot.session` и больше спрашивать не будет.

## Управление

Команды отправляются **от себя** в любом чате (юзербот слушает только исходящие сообщения).

| Команда | Действие |
|---|---|
| `/launch` | Запустить реакцию на само это сообщение |
| `/launch` *(ответом на сообщение)* | Запустить реакцию на то сообщение |
| `/stop` | Остановить все сессии в текущем чате |
| `/stopall` | Остановить все сессии во всех чатах |
| `/start` | Показать статус |

Можно запускать одновременно в нескольких чатах — сессии работают независимо.

## Структура проекта

```
.
├── player.py            # Основной скрипт
├── cutter/              # Инструмент для нарезки видео на кадры-эмодзи
├── temp_reaction_tiles/ # Временные кадры (в .gitignore)
├── .env                 # Токены (в .gitignore)
└── userbot.session      # Сессия Telethon (в .gitignore)
```

## Требования

- Python 3.10+
- Аккаунт Telegram с подпиской **Telegram Premium** (для кастомных реакций)
