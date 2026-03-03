import os
import logging
from datetime import datetime
from dotenv import load_dotenv

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("Show Time", callback_data="time"),
            InlineKeyboardButton("Show Date", callback_data="date"),
        ],
        [
            InlineKeyboardButton("About", callback_data="about")
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Choose an option:",
        reply_markup=reply_markup
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    await query.answer()

    data = query.data

    if data == "time":
        text = f"Current Time: {datetime.now().strftime('%H:%M:%S')}"
    elif data == "date":
        text = f"Today's Date: {datetime.now().strftime('%Y-%m-%d')}"
    elif data == "about":
        text = "This is an interactive demo bot."
    else:
        text = "Unknown action."

    # Edit the same message instead of sending new one
    await query.edit_message_text(text=text)


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    app.run_polling()


if __name__ == "__main__":
    main()