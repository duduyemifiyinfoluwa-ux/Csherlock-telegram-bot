import asyncio
import logging
import os
from threading import Thread
from flask import Flask
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# --- 1. DUMMY WEB SERVER FOR RENDER ---
web_app = Flask(__name__)


@web_app.route("/")
def home():
    return "Sherlock Terminal is Online!"


def run_flask():
    # Render automatically assigns a PORT variable
    port = int(os.environ.get("PORT", 8080))
    web_app.run(host="0.0.0.0", port=port)


# --- 2. TELEGRAM BOT LOGIC ---
logging.basicConfig(level=logging.INFO)

# Fetch token from Render Environment Variables for security
BOT_TOKEN = os.environ.get("BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔍 *SHERLOCK DETECTIVE TERMINAL ONLINE*\n\n"
        "Welcome, Investigator. System hosted on Cloud 24/7.\n\n"
        "Type /clue1 to view current evidence.",
        parse_mode="Markdown",
    )


async def clue1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    clue_msg = await context.bot.send_message(
        chat_id=chat_id,
        text="⚠️ *CLASSIFIED EVIDENCE #1*\n\n"
        '"The clock stopped at 03:14 AM, but the victim\'s tea was still boiling hot."\n\n'
        "⏱️ *This message will self-destruct in 15 seconds!*",
        parse_mode="Markdown",
    )

    await asyncio.sleep(15)

    try:
        await context.bot.delete_message(
            chat_id=chat_id, message_id=clue_msg.message_id
        )
        await context.bot.send_message(
            chat_id=chat_id,
            text="❌ *EVIDENCE DESTROYED.* Time expired!",
            parse_mode="Markdown",
        )
    except Exception as e:
        print(f"Error deleting message: {e}")


def main():
    # Run Flask in the background so it doesn't block the Telegram bot
    Thread(target=run_flask, daemon=True).start()

    # Run Telegram Bot
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("clue1", clue1))

    print("🕵️‍♂️ Sherlock Bot is running live...")
    app.run_polling()


if __name__ == "__main__":
    main()
