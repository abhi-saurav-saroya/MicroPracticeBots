import os
from dotenv import load_dotenv

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)

# CONFIG
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# STATES
REGISTER_NAME, REGISTER_AGE, REGISTER_LOCATION, REGISTER_PASSWORD = range(4)
LOGIN_NAME, LOGIN_PASSWORD = range(2)

# DATABASE (In-Memory)
users = {}

# KEYBOARD
def main_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("Register", callback_data="register"),
            InlineKeyboardButton("Login", callback_data="login"),
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

# START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome.\nChoose an option:",
        reply_markup=main_keyboard()
    )

# REGISTER FLOW
async def start_register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    await query.message.reply_text("Enter a username (3–20 characters):")
    return REGISTER_NAME


async def register_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.message.text.strip()

    if not username.isalnum():
        await update.message.reply_text("Username must be alphanumeric only:")
        return REGISTER_NAME

    if not (3 <= len(username) <= 20):
        await update.message.reply_text("Username must be 3–20 characters:")
        return REGISTER_NAME

    if username in users:
        await update.message.reply_text("Username already exists. Try another:")
        return REGISTER_NAME

    context.user_data["reg_username"] = username
    await update.message.reply_text("Enter your age (10–100):")
    return REGISTER_AGE


async def register_age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    age_text = update.message.text.strip()

    if not age_text.isdigit():
        await update.message.reply_text("Age must be a number:")
        return REGISTER_AGE

    age = int(age_text)

    if not (10 <= age <= 100):
        await update.message.reply_text("Age must be between 10 and 100:")
        return REGISTER_AGE

    context.user_data["reg_age"] = age
    await update.message.reply_text("Enter your location:")
    return REGISTER_LOCATION


async def register_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    location = update.message.text.strip()

    if len(location) < 2:
        await update.message.reply_text("Location too short:")
        return REGISTER_LOCATION

    context.user_data["reg_location"] = location
    await update.message.reply_text("Create a password (min 6 characters):")
    return REGISTER_PASSWORD


async def register_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    password = update.message.text.strip()

    if len(password) < 6:
        await update.message.reply_text("Password too short. Minimum 6 characters:")
        return REGISTER_PASSWORD

    username = context.user_data["reg_username"]

    users[username] = {
        "age": context.user_data["reg_age"],
        "location": context.user_data["reg_location"],
        "password": password,
    }

    await update.message.reply_text("Registration successful!")

    context.user_data.clear()
    return ConversationHandler.END


# LOGIN FLOW
async def start_login(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    await query.message.reply_text("Enter your username:")
    return LOGIN_NAME


async def login_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.message.text.strip()

    if username not in users:
        await update.message.reply_text("User not found. Try again:")
        return LOGIN_NAME

    context.user_data["login_username"] = username
    await update.message.reply_text("Enter your password:")
    return LOGIN_PASSWORD


async def login_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    password = update.message.text.strip()
    username = context.user_data["login_username"]

    if users[username]["password"] == password:
        await update.message.reply_text("Login successful!")
    else:
        await update.message.reply_text("Incorrect password.")

    context.user_data.clear()
    return ConversationHandler.END


# CANCEL
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Operation cancelled.")
    context.user_data.clear()
    return ConversationHandler.END


# MAIN
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    register_conv = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(start_register, pattern="^register$")
        ],
        states={
            REGISTER_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, register_name)],
            REGISTER_AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, register_age)],
            REGISTER_LOCATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, register_location)],
            REGISTER_PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, register_password)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        allow_reentry=True,
    )

    login_conv = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(start_login, pattern="^login$")
        ],
        states={
            LOGIN_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, login_name)],
            LOGIN_PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, login_password)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        allow_reentry=True,
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(register_conv)
    app.add_handler(login_conv)

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()