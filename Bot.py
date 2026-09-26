import asyncio
import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# 1. SETUP LOGGING (Shows errors in your terminal)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# REPLACE THIS WITH YOUR ACTUAL BOT TOKEN FROM BOTFATHER
BOT_TOKEN = "8963839200:AAGsPNOZZyvq19bsL5gUvx541eJscl-0NH0"


# 2. START COMMAND (/start)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "🔍 *SHERLOCK DETECTIVE TERMINAL ONLINE*\n\n"
        "Welcome, Investigator. Clues requested here will disappear rapidly.\n\n"
        "Available commands:\n"
        "/clue1 - Retrieve classified scene note (Self-destructs in 15s)\n"
        "Or type the password solution directly into this chat."
    )
    await update.message.reply_text(welcome_text, parse_mode="Markdown")


# 3. TIMED CLUE HANDLER (Self-destructs after X seconds)
async def clue1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    # Send the clue message
    clue_msg = await context.bot.send_message(
        chat_id=chat_id,
        text="⚠️ *CLASSIFIED EVIDENCE #1*\n\n"
        "\"The clock stopped at 03:14 AM, but the victim's tea was still boiling hot.\"\n\n"
        "⏱️ *This message will self-destruct in 15 seconds!*",
        parse_mode="Markdown",
    )

    # Wait for 15 seconds
    await asyncio.sleep(15)

    # Delete the clue message automatically
    try:
        await context.bot.delete_message(
            chat_id=chat_id, message_id=clue_msg.message_id
        )
        # Optional notification that clue expired
        await context.bot.send_message(
            chat_id=chat_id,
            text="❌ *EVIDENCE DESTROYED.* You were too slow!",
            parse_mode="Markdown",
        )
    except Exception as e:
        print(f"Could not delete message: {e}")


# 4. PASSWORD & ANSWER CHECKER
async def check_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.strip().lower()

    # Define your correct puzzle answer here
    CORRECT_ANSWER = "boiler"

    if user_input == CORRECT_ANSWER:
        success_text = (
            "🔓 *ACCESS GRANTED*\n\n"
            "Correct answer! Return to the WhatsApp chat and tell everyone "
            "the passkey is: **RED HERRING**."
        )
        await update.message.reply_text(success_text, parse_mode="Markdown")
    else:
        await update.message.reply_text(
            "🚫 *ACCESS DENIED.* Incorrect password. Try again."
        )


# 5. MAIN BOT RUNNER
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Register handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("clue1", clue1))

    # Catch plain text messages to check as password attempts
    app.add_handler(
        MessageHandler(filters.TEXT & (~filters.COMMAND), check_answer)
    )

    print("🕵️‍♂️ Sherlock Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
