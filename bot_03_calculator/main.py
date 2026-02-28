from dotenv import load_dotenv
import os
from telegram import Update
from telegram.ext import (
    MessageHandler,
    CommandHandler,
    ApplicationBuilder,
    ContextTypes,
    filters
)
import re

load_dotenv()
token = os.getenv("BOT_TOKEN")

precedence = {
    '+': 1,
    '-': 1,
    '*': 2,
    '/': 2
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "HEY THERE!\n"
        "I AM A CALCULATOR."
    )

def is_tokens_valid(tokens) -> bool:
    if not tokens:
        return False

    prev = None
    balance = 0

    for token in tokens:
        if token.isdigit():
            if prev is not None and prev.isdigit():
                return False
            if prev == ")":
                return False

        elif token in ["+", "-", "*", "/"]:
            if prev in ["+", "-", "*", "/", "(" , None]:
                return False

        elif token == "(":
            balance += 1

        elif token == ")":
            balance -= 1
            if balance < 0:
                return False

        prev = token

    if prev in ["+", "-", "*", "/", "("]:
        return False

    return balance == 0

def calculate(tokens) -> int:
    tokens.insert(0, "(")
    tokens.append(")")
    Values = []
    Operators = []

    for token in tokens:
        if token.isdigit():
            Values.append(int(token))

        elif token in ["+", "-", "*", "/"]:
            while (
                len(Operators) > 0
                and Operators[-1] != "("
                and precedence[token] <= precedence[Operators[-1]]
            ):
                val2 = Values.pop()
                val1 = Values.pop()
                op = Operators.pop()

                result = None
                if op == "+":
                    result = val1 + val2
                elif op == "-":
                    result = val1 - val2
                elif op == "*":
                    result = val1 * val2
                elif op == "/":
                    result = val1 / val2

                Values.append(result)

            # IMPORTANT: push operator AFTER applying
            Operators.append(token)

        elif token == "(":
            Operators.append(token)

        elif token == ")":
            while len(Operators) and Operators[-1] != "(":
                val2 = Values.pop()
                val1 = Values.pop()
                op = Operators.pop()

                if op == "+":
                    result = val1 + val2
                elif op == "-":
                    result = val1 - val2
                elif op == "*":
                    result = val1 * val2
                elif op == "/":
                    result = val1 / val2

                Values.append(result)

            # Remove "("
            Operators.pop()

    while Operators:
        val2 = Values.pop()
        val1 = Values.pop()
        op = Operators.pop()

        if op == "+":
            result = val1 + val2
        elif op == "-":
            result = val1 - val2
        elif op == "*":
            result = val1 * val2
        elif op == "/":
            result = val1 / val2

        Values.append(result)

    return Values[-1]


async def calculator(update: Update, context: ContextTypes.DEFAULT_TYPE):
    expression = update.message.text

    if not re.fullmatch(r'[0-9+\-*/()\s]+', expression):
        await update.message.reply_text("Only integers and + - * / ( ) are allowed.")
        return

    tokens = re.findall(r'\d+|[+\-*/()]', expression)

    print(tokens)

    if not is_tokens_valid(tokens):
        await update.message.reply_text("The expression you entered is invalid.")
        return

    answer = calculate(tokens)
    await update.message.reply_text(f"{expression} = {str(answer)}")

app = ApplicationBuilder().token(token).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, calculator))

print("Bot is running...")
app.run_polling()