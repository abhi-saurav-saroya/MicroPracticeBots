from dotenv import load_dotenv
import os
from telegram import Update
from telegram.ext import(
    MessageHandler,
    CommandHandler,
    ApplicationBuilder,
    filters,
    ContextTypes
)

load_dotenv()
Token = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    state = context.user_data.get("state")
    if state is None:
        context.user_data["state"] = "waiting_for_name"
        await update.message.reply_text(
            "Hello, Welcome to Telegram Bot!\n"
            "What is your name?"
        )
    elif state == "blocked":
        await update.message.reply_text(
            "No way, you thought that restarting the bot will get you unblocked.\n"
            "COMPLETE YOUR HOMEWORK"
        )
    elif state == "registered":
        await update.message.reply_text(
            "WELCOME, YOU ARE OFFICIALLY REGISTERED.\n"
            f"Name: {context.user_data['name']}\n"
            f"Age: {context.user_data['age']}\n"
            f"Gender: {context.user_data['gender']}\n"
            f"Location: {context.user_data['location']}\n"
        )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    state = context.user_data.get("state")

    if state is None:
        await update.message.reply_text("Please type /start first.")
        return

    elif state == "waiting_for_name":
        await handle_name(update, context)

    elif state == "waiting_for_age":
        await handle_age(update, context)

    elif state == "waiting_for_gender":
        await handle_gender(update, context)

    elif state == "waiting_for_location":
        await handle_location(update, context)

    elif state == "blocked":
        await handle_block(update, context)


async def handle_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.message.text
    context.user_data["name"] = name
    context.user_data["state"] = "waiting_for_age"
    await update.message.reply_text(
        f"That's such a wonderful name, {(name.title())}\n"
        "How old are you?"
    )

async def handle_age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        age = int(update.message.text)
        context.user_data["age"] = age
        if 18 <= age <= 100:
            context.user_data["state"] = "waiting_for_gender"
            await update.message.reply_text(
                f"You are old enough. You have the access.\n"
                "What's your gender btw? M/F/O"
            )
        elif age > 100:
            context.user_data["state"] = "waiting_for_gender"
            await update.message.reply_text(
                f"{age}? Not dead already?\n"
                "Dont laugh, your teeth arent there\n"
                "What's your gender btw? M/F/O"
            )
        elif 0 <= age < 18:
            context.user_data["state"] = "blocked"
            await update.message.reply_text(
                f"{age}? Go to school, kiddo.\n"
                "!! BLOCKED !!"
            )
        else:
            await update.message.reply_text(
                "Nah, you gotta be kidding me, you aren't negative years old.\n"
                "Enter a valid age."
            )
    except ValueError:
        await update.message.reply_text(
            "Enter a valid age."
        )

async def handle_gender(update: Update, context: ContextTypes.DEFAULT_TYPE):
    gender = update.message.text.lower()
    if gender == "m" or gender == "male":
        context.user_data["gender"] = "M"
        context.user_data["state"] = "waiting_for_location"
        await update.message.reply_text(
            "I see, a handsome young dude, haha.\n"
            "What country are you from though?"
        )
    elif gender == "f" or gender == "female":
        context.user_data["gender"] = "F"
        context.user_data["state"] = "waiting_for_location"
        await update.message.reply_text(
            "I see, a gorgeous sweetie, huh?.\n"
            "What country are you from though?"
        )
    elif gender == "o" or gender == "other":
        context.user_data["gender"] = "O"
        context.user_data["state"] = "waiting_for_location"
        await update.message.reply_text(
            "I see, I see, welcome here.\n"
            "What country are you from though?"
        )
    else:
        await update.message.reply_text(
            "I have not heard of such gender before.\n"
            "Choose something that makes sense."
        )

async def handle_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    location = update.message.text.title()

    if location not in ["India", "Pakistan", "Nepal", "Sri Lanka", "Bhutan"]:
        context.user_data["state"] = "blocked"
        await update.message.reply_text(
            "We do not provide services there in your country.\n"
            "ACCESS DENIED."
        )

    else:
        context.user_data["location"] = location
        context.user_data["state"] = "registered"
        await start(update, context)



async def handle_block(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass



app = ApplicationBuilder().token(Token).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))


print("bot is running.....")
app.run_polling()