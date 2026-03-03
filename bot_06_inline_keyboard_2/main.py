import os
from dotenv import load_dotenv

from telegram import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    Update
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler
)

def get_api() -> str:
    load_dotenv()
    return os.getenv("BOT_TOKEN")

RESPONSES = {
        "education": "DAVIET 2024-2028\n"
                     "B.Tech in CSE.",
        "languages": "1. Punjabi\n"
                     "2. English\n"
                     "3. Hindi\n"
                     "4. C\n"
                     "5. C++\n"
                     "6. Python",
        "myself": "SECOND YEAR ENGINEERING STUDENT",
        "projects": "1. EduGenie\n"
                    "2. PhoneBook\n"
                    "3. VaultX\n"
                    "5. CipherSafe\n"
                    "6. MicroBots"
    }

def main_menu_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("Myself", callback_data="myself"),
            InlineKeyboardButton("Education", callback_data="education"),
        ],
        [
            InlineKeyboardButton("Languages", callback_data="languages"),
            InlineKeyboardButton("Projects", callback_data="projects"),
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "WELCOME TO THIS BOT.",
        reply_markup=main_menu_keyboard()
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    await query.answer()
    data = query.data

    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Back", callback_data="back")
            ]
        ]
    )

    if data in RESPONSES:
        await query.edit_message_text(
            RESPONSES[data],
            reply_markup=reply_markup
        )
    elif data == "back":
        await query.edit_message_text(
            "HOME MENU",
            reply_markup=main_menu_keyboard()
        )
    else:
        await query.edit_message_text(
            "Unknown Action."
        )


def main():
    Token = get_api()
    app = ApplicationBuilder().token(Token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    app.run_polling()


if __name__ == '__main__':
    main()