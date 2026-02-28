from dotenv import load_dotenv
import os
from telegram import Update
from telegram.ext import (
    CommandHandler,
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    filters,
    PicklePersistence
)

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
if TOKEN is None:
    raise ValueError("BOT_TOKEN not found. Check your .env file.")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["active"] = True
    await update.message.reply_text(
        f"Hello {update.effective_user.first_name}! Echo is now active."
    )

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["active"] = False
    await update.message.reply_text(
        "Thank You for testing the echo bot! Visit again.\n"
        "/start to experience this bot for echoing!"
    )

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get("active", False):
        return

    await update.message.copy(chat_id=update.effective_chat.id)

persistence = PicklePersistence(filepath="bot_data.pkl")

app = ApplicationBuilder().token(TOKEN).persistence(persistence).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("stop", stop))
app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, echo))

print("Bot is running...")
app.run_polling()