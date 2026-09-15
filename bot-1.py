import logging
import os

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)
from openai import OpenAI

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Salom! Men AI botman, savolingizni yozing 🤖"
    )


async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    await update.message.chat.send_action(action="typing")

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Siz foydali va do'stona yordamchisiz. O'zbek tilida javob bering."
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ]
        )

        answer = response.choices[0].message.content

        await update.message.reply_text(answer)

    except Exception as e:
        logging.error(f"OpenAI xatosi: {e}")
        await update.message.reply_text(
            "Kechirasiz, xatolik yuz berdi. Keyinroq urinib ko'ring."
        )


def main():
    application = (
        ApplicationBuilder()
        .token(TELEGRAM_TOKEN)
        .connect_timeout(30)
        .read_timeout(30)
        .write_timeout(30)
        .get_updates_connect_timeout(30)
        .get_updates_read_timeout(30)
        .build()
    )

    application.add_handler(
        CommandHandler("start", start)
    )

    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, chat)
    )

    print("Bot ishga tushdi...")

    application.run_polling()


if __name__ == "__main__":
    main()
