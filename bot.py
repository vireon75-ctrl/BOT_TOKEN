from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardRemove,
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
import random
import os
import json
import logging

# =========================================================
# VIREON TELEGRAM BOT
# Requires python-telegram-bot v20+
# =========================================================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError(
        "BOT_TOKEN табылмады! Оны орта айнымалысы ретінде орнатыңыз."
    )

ADMIN_USERNAME = "Sabinanizhansykorem"
YOUTUBE_URL = "https://youtube.com/"
TIKTOK_URL = "https://tiktok.com/"
DATA_FILE = "users.json"

TEXTS = {
    "kk": {
        "welcome": "🤖 Vireon ботына қош келдің!\n\nҚажетті бөлімді таңда:",
        "profile_button": "👤 Сенің профилің",
        "games_button": "🎮 Ойындар",
        "language_button": "🌐 Тіл",
        "admin_button": "👑 Админ",
        "home": "🏠 БАСТЫ МӘЗІР\n\nҚажетті бөлімді таңда:",
        "profile": "👤 СЕНІҢ ПРОФИЛІҢ",
        "profile_name": "👤 Атың",
        "profile_name_none": "Қойылмаған",
        "profile_id": "🆔 ID",
        "points": "⭐ Ұпай",
        "coins": "🪙 Монета",
        "change_name": "✏️ Атымды өзгерту",
        "back": "🔙 Басты мәзір",
        "games": "🎮 ОЙЫНДАР МӘЗІРІ\n\nОйын таңда:",
        "coin": "🪙 Монета лақтыру",
        "dice": "🎲 Кубик",
        "math": "🧮 Математика",
        "guess": "🎯 Сан табу",
        "back_games": "🔙 Ойындарға қайту",
        "coin_result": "🪙 Монета лақтырылды!\n\n",
        "heads": "🟡 Аверс",
        "tails": "⚪ Реверс",
        "coin_count": "🪙 Монетаң",
        "again": "🔄 Қайта ойнау",
        "dice_result": "🎲 Кубик нәтижесі: ",
        "points_count": "⭐ Ұпайың",
        "math_instruction": "🧮 МАТЕМАТИКА\n\nЕсепті шығар:\n\n",
        "math_answer": "✍️ Жауабыңды санмен жаз.",
        "math_correct": "✅ Дұрыс!\n\n⭐ +1 ұпай",
        "math_wrong": "❌ Қате! Дұрыс жауап: ",
        "next_math": "🧮 Келесі есеп",
        "guess_instruction": "🎯 САН ТАБУ ОЙЫНЫ\n\nМен 1 мен 10 аралығында сан ойладым. Санды жаз:",
        "guess_higher": "⬆️ Үлкенірек сан таңда!",
        "guess_lower": "⬇️ Кішірек сан таңда!",
        "guess_correct": "🎉 Дұрыс таптың!\n\n⭐ +1 ұпай\n🪙 +2 монета",
        "language_title": "🌐 ТІЛ ТАҢДАУ\n\nҚай тілді таңдайсың?",
        "kk_selected": "🇰🇿 Қазақ тілі таңдалды!",
        "ru_selected": "🇷🇺 Русский язык выбран!",
        "en_selected": "🇬🇧 English selected!",
        "admin": "👑 АДМИН\n\n🤖 Vireon жобасының әкімшісі\n\nТөмендегі батырмалар арқылы байланыса аласың.",
        "write_admin": "📩 Админге жазу",
        "youtube": "▶️ YouTube",
        "tiktok": "🎵 TikTok",
        "enter_name": "✏️ Жаңа атыңды жаз:\n\nБұл Vireon ішіндегі профиліңнің аты болады.",
        "name_saved": "✅ Атың сәтті өзгертілді!",
        "invalid_number": "❌ Өтінемін, тек сан жаз.",
        "guess_wait": "🎯 Алдымен 1 мен 10 аралығындағы сан жаз.",
        "cancel": "Болдырмау",
    },
    "ru": {
        "welcome": "🤖 Добро пожаловать в Vireon!\n\nВыбери нужный раздел:",
        "profile_button": "👤 Твой профиль",
        "games_button": "🎮 Игры",
        "language_button": "🌐 Язык",
        "admin_button": "👑 Админ",
        "home": "🏠 ГЛАВНОЕ МЕНЮ\n\nВыбери нужный раздел:",
        "profile": "👤 ТВОЙ ПРОФИЛЬ",
        "profile_name": "👤 Имя",
        "profile_name_none": "Не установлено",
        "profile_id": "🆔 ID",
        "points": "⭐ Очки",
        "coins": "🪙 Монеты",
        "change_name": "✏️ Изменить имя",
        "back": "🔙 Главное меню",
        "games": "🎮 МЕНЮ ИГР\n\nВыбери игру:",
        "coin": "🪙 Подбросить монету",
        "dice": "🎲 Кубик",
        "math": "🧮 Математика",
        "guess": "🎯 Угадай число",
        "back_games": "🔙 Назад к играм",
        "coin_result": "🪙 Монета подброшена!\n\n",
        "heads": "🟡 Орёл",
        "tails": "⚪ Решка",
        "coin_count": "🪙 Твои монеты",
        "again": "🔄 Играть снова",
        "dice_result": "🎲 Результат кубика: ",
        "points_count": "⭐ Твои очки",
        "math_instruction": "🧮 МАТЕМАТИКА\n\nРеши пример:\n\n",
        "math_answer": "✍️ Напиши ответ числом.",
        "math_correct": "✅ Правильно!\n\n⭐ +1 очко",
        "math_wrong": "❌ Неправильно! Правильный ответ: ",
        "next_math": "🧮 Следующий пример",
        "guess_instruction": "🎯 УГАДАЙ ЧИСЛО\n\nЯ загадал число от 1 до 10. Напиши число:",
        "guess_higher": "⬆️ Выбери число побольше!",
        "guess_lower": "⬇️ Выбери число поменьше!",
        "guess_correct": "🎉 Правильно!\n\n⭐ +1 очко\n🪙 +2 монеты",
        "language_title": "🌐 ВЫБОР ЯЗЫКА\n\nКакой язык выбрать?",
        "kk_selected": "🇰🇿 Выбран казахский язык!",
        "ru_selected": "🇷🇺 Выбран русский язык!",
        "en_selected": "🇬🇧 Выбран английский язык!",
        "admin": "👑 АДМИН\n\n🤖 Администратор проекта Vireon\n\nТы можешь связаться с администратором:",
        "write_admin": "📩 Написать админу",
        "youtube": "▶️ YouTube",
        "tiktok": "🎵 TikTok",
        "enter_name": "✏️ Напиши новое имя:\n\nЭто будет имя твоего профиля внутри Vireon.",
        "name_saved": "✅ Имя успешно изменено!",
        "invalid_number": "❌ Пожалуйста, введи только число.",
        "guess_wait": "🎯 Сначала введи число от 1 до 10.",
        "cancel": "Отмена",
    },
    "en": {
        "welcome": "🤖 Welcome to Vireon!\n\nChoose a section:",
        "profile_button": "👤 Your Profile",
        "games_button": "🎮 Games",
        "language_button": "🌐 Language",
        "admin_button": "👑 Admin",
        "home": "🏠 MAIN MENU\n\nChoose a section:",
        "profile": "👤 YOUR PROFILE",
        "profile_name": "👤 Name",
        "profile_name_none": "Not set",
        "profile_id": "🆔 ID",
        "points": "⭐ Points",
        "coins": "🪙 Coins",
        "change_name": "✏️ Change Name",
        "back": "🔙 Main Menu",
        "games": "🎮 GAMES MENU\n\nChoose a game:",
        "coin": "🪙 Flip Coin",
        "dice": "🎲 Dice",
        "math": "🧮 Math",
        "guess": "🎯 Guess the Number",
        "back_games": "🔙 Back to Games",
        "coin_result": "🪙 Coin flipped!\n\n",
        "heads": "🟡 Heads",
        "tails": "⚪ Tails",
        "coin_count": "🪙 Your coins",
        "again": "🔄 Play Again",
        "dice_result": "🎲 Dice result: ",
        "points_count": "⭐ Your points",
        "math_instruction": "🧮 MATH\n\nSolve this problem:\n\n",
        "math_answer": "✍️ Type your answer as a number.",
        "math_correct": "✅ Correct!\n\n⭐ +1 point",
        "math_wrong": "❌ Wrong! Correct answer: ",
        "next_math": "🧮 Next Problem",
        "guess_instruction": "🎯 GUESS THE NUMBER\n\nI chose a number from 1 to 10. Type your guess:",
        "guess_higher": "⬆️ Choose a higher number!",
        "guess_lower": "⬇️ Choose a lower number!",
        "guess_correct": "🎉 Correct!\n\n⭐ +1 point\n🪙 +2 coins",
        "language_title": "🌐 LANGUAGE SELECTION\n\nWhich language do you choose?",
        "kk_selected": "🇰🇿 Kazakh selected!",
        "ru_selected": "🇷🇺 Russian selected!",
        "en_selected": "🇬🇧 English selected!",
        "admin": "👑 ADMIN\n\n🤖 Vireon project administrator\n\nUse the buttons below to visit the links or contact the admin.",
        "write_admin": "📩 Contact Admin",
        "youtube": "▶️ YouTube",
        "tiktok": "🎵 TikTok",
        "enter_name": "✏️ Enter your new name:\n\nThis will be your profile name inside Vireon.",
        "name_saved": "✅ Name successfully changed!",
        "invalid_number": "❌ Please enter a number only.",
        "guess_wait": "🎯 First, enter a number from 1 to 10.",
        "cancel": "Cancel",
    },
}


def load_users():
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data if isinstance(data, dict) else {}
    except (OSError, json.JSONDecodeError):
        logger.exception("Could not read users.json")
        return {}


users = load_users()


def save_users():
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(users, file, ensure_ascii=False, indent=2)
    except OSError:
        logger.exception("Could not save users.json")


def create_user(user_id):
    uid = str(user_id)
    if uid not in users:
        users[uid] = {
            "profile_name": "",
            "coins": 0,
            "points": 0,
            "language": "kk",
        }
        save_users()
    else:
        users[uid].setdefault("profile_name", "")
        users[uid].setdefault("coins", 0)
        users[uid].setdefault("points", 0)
        if users[uid].get("language") not in TEXTS:
            users[uid]["language"] = "kk"
    return users[uid]


def get_user(user_id):
    return create_user(user_id)


def update_user(user_id, field, value):
    allowed = {"profile_name", "coins", "points", "language"}
    if field not in allowed:
        return
    create_user(user_id)[field] = value
    save_users()


def add_coins(user_id, amount):
    user = create_user(user_id)
    user["coins"] = max(0, int(user.get("coins", 0)) + int(amount))
    save_users()


def add_points(user_id, amount):
    user = create_user(user_id)
    user["points"] = max(0, int(user.get("points", 0)) + int(amount))
    save_users()


def t(user_id, key):
    language = get_user(user_id).get("language", "kk")
    return TEXTS.get(language, TEXTS["kk"]).get(key, key)


def main_menu(user_id):
    keyboard = [
        [InlineKeyboardButton(t(user_id, "profile_button"), callback_data="profile")],
        [InlineKeyboardButton(t(user_id, "games_button"), callback_data="games")],
        [InlineKeyboardButton(t(user_id, "language_button"), callback_data="language")],
        [InlineKeyboardButton(t(user_id, "admin_button"), callback_data="admin")],
    ]
    return InlineKeyboardMarkup(keyboard)


def profile_menu(user_id):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(t(user_id, "change_name"), callback_data="change_name")],
        [InlineKeyboardButton(t(user_id, "back"), callback_data="home")],
    ])


def games_menu(user_id):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(t(user_id, "coin"), callback_data="coin")],
        [InlineKeyboardButton(t(user_id, "dice"), callback_data="dice")],
        [InlineKeyboardButton(t(user_id, "math"), callback_data="math")],
        [InlineKeyboardButton(t(user_id, "guess"), callback_data="guess")],
        [InlineKeyboardButton(t(user_id, "back"), callback_data="home")],
    ])


def language_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🇰🇿 Қазақша", callback_data="lang_kk")],
        [InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru")],
        [InlineKeyboardButton("🇬🇧 English", callback_data="lang_en")],
        [InlineKeyboardButton("🔙", callback_data="home")],
    ])


def back_to_games(user_id):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(t(user_id, "again"), callback_data="coin")],
        [InlineKeyboardButton(t(user_id, "back_games"), callback_data="games")],
    ])


def profile_text(user_id):
    user = get_user(user_id)
    name = user.get("profile_name") or t(user_id, "profile_name_none")
    return (
        f"{t(user_id, 'profile')}\n\n"
        f"{t(user_id, 'profile_name')}: {name}\n"
        f"{t(user_id, 'profile_id')}: {user_id}\n"
        f"{t(user_id, 'points')}: {user.get('points', 0)}\n"
        f"{t(user_id, 'coins')}: {user.get('coins', 0)}"
    )


def new_math_question(user_id):
    a = random.randint(1, 20)
    b = random.randint(1, 20)
    op = random.choice(["+", "-", "×"])
    if op == "+":
        answer = a + b
    elif op == "-":
        if b > a:
            a, b = b, a
        answer = a - b
    else:
        answer = a * b
    return f"{a} {op} {b} = ?", answer


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    create_user(user_id)
    context.user_data.pop("waiting_for_name", None)
    context.user_data.pop("math_answer", None)
    context.user_data.pop("guess_number", None)
    await update.effective_message.reply_text(
        t(user_id, "welcome"),
        reply_markup=main_menu(user_id),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    await update.effective_message.reply_text(
        "/start — " + t(user_id, "home") + "\n/help — help"
    )


async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    create_user(user_id)
    data = query.data

    if data == "home":
        context.user_data.pop("waiting_for_name", None)
        context.user_data.pop("math_answer", None)
        context.user_data.pop("guess_number", None)
        await query.edit_message_text(t(user_id, "home"), reply_markup=main_menu(user_id))

    elif data == "profile":
        await query.edit_message_text(profile_text(user_id), reply_markup=profile_menu(user_id))

    elif data == "games":
        await query.edit_message_text(t(user_id, "games"), reply_markup=games_menu(user_id))

    elif data == "change_name":
        context.user_data["waiting_for_name"] = True
        await query.edit_message_text(
            t(user_id, "enter_name"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(t(user_id, "back"), callback_data="profile")]
            ]),
        )

    elif data == "language":
        await query.edit_message_text(t(user_id, "language_title"), reply_markup=language_menu())

    elif data.startswith("lang_"):
        language = data.split("_", 1)[1]
        if language in TEXTS:
            update_user(user_id, "language", language)
        selected_key = {
            "kk": "kk_selected",
            "ru": "ru_selected",
            "en": "en_selected",
        }[language]
        await query.edit_message_text(
            t(user_id, selected_key),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(t(user_id, "back"), callback_data="home")]
            ]),
        )

    elif data == "admin":
        keyboard = [
            [InlineKeyboardButton(t(user_id, "write_admin"), url=f"https://t.me/{ADMIN_USERNAME}")],
            [InlineKeyboardButton(t(user_id, "youtube"), url=YOUTUBE_URL)],
            [InlineKeyboardButton(t(user_id, "tiktok"), url=TIKTOK_URL)],
            [InlineKeyboardButton(t(user_id, "back"), callback_data="home")],
        ]
        await query.edit_message_text(
            t(user_id, "admin"),
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    elif data == "coin":
        result_key = random.choice(["heads", "tails"])
        add_coins(user_id, 1)
        text = (
            t(user_id, "coin_result")
            + t(user_id, result_key)
            + "\n\n"
            + t(user_id, "coin_count")
            + f": {get_user(user_id)['coins']}"
        )
        await query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(t(user_id, "again"), callback_data="coin")],
                [InlineKeyboardButton(t(user_id, "back_games"), callback_data="games")],
            ]),
        )

    elif data == "dice":
        result = random.randint(1, 6)
        add_points(user_id, 1)
        await query.edit_message_text(
            f"{t(user_id, 'dice_result')}{result}\n\n"
            f"{t(user_id, 'points_count')}: {get_user(user_id)['points']}",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(t(user_id, "again"), callback_data="dice")],
                [InlineKeyboardButton(t(user_id, "back_games"), callback_data="games")],
            ]),
        )

    elif data == "math":
        question, answer = new_math_question(user_id)
        context.user_data["math_answer"] = answer
        await query.edit_message_text(
            t(user_id, "math_instruction") + question + "\n" + t(user_id, "math_answer"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(t(user_id, "back_games"), callback_data="games")]
            ]),
        )

    elif data == "guess":
        context.user_data["guess_number"] = random.randint(1, 10)
        await query.edit_message_text(
            t(user_id, "guess_instruction"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(t(user_id, "back_games"), callback_data="games")]
            ]),
        )


async def text_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_user or not update.effective_message:
        return

    user_id = update.effective_user.id
    message = update.effective_message
    text = (message.text or "").strip()
    create_user(user_id)

    if context.user_data.get("waiting_for_name"):
        if not text:
            await message.reply_text(t(user_id, "enter_name"))
            return
        if len(text) > 40:
            await message.reply_text("Атың 40 таңбадан аспасын. Қайта жаз.")
            return
        update_user(user_id, "profile_name", text)
        context.user_data.pop("waiting_for_name", None)
        await message.reply_text(
            t(user_id, "name_saved"),
            reply_markup=main_menu(user_id),
        )
        return

    if "math_answer" in context.user_data:
        try:
            answer = int(text)
        except ValueError:
            await message.reply_text(t(user_id, "invalid_number"))
            return

        correct_answer = context.user_data.pop("math_answer")
        if answer == correct_answer:
            add_points(user_id, 1)
            result_text = t(user_id, "math_correct")
        else:
            result_text = t(user_id, "math_wrong") + str(correct_answer)

        await message.reply_text(
            result_text,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(t(user_id, "next_math"), callback_data="math")],
                [InlineKeyboardButton(t(user_id, "back_games"), callback_data="games")],
            ]),
        )
        return

    if "guess_number" in context.user_data:
        try:
            guess = int(text)
        except ValueError:
            await message.reply_text(t(user_id, "invalid_number"))
            return

        if not 1 <= guess <= 10:
            await message.reply_text(t(user_id, "guess_wait"))
            return

        target = context.user_data["guess_number"]
        if guess < target:
            await message.reply_text(t(user_id, "guess_higher"))
        elif guess > target:
            await message.reply_text(t(user_id, "guess_lower"))
        else:
            context.user_data.pop("guess_number", None)
            add_points(user_id, 1)
            add_coins(user_id, 2)
            await message.reply_text(
                t(user_id, "guess_correct"),
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(t(user_id, "again"), callback_data="guess")],
                    [InlineKeyboardButton(t(user_id, "back_games"), callback_data="games")],
                ]),
            )
        return

    await message.reply_text(
        t(user_id, "home"),
        reply_markup=main_menu(user_id),
    )


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error(
        "Unhandled exception while processing update",
        exc_info=context.error,
    )


def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CallbackQueryHandler(buttons))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, text_messages)
    )
    application.add_error_handler(error_handler)

    logger.info("Vireon bot is starting...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
