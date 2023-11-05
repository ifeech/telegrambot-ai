import os
import logging
import argparse

from dotenv import load_dotenv
from pathlib import Path
from telegram import Update, Voice
from telegram.ext import (
    filters,
    MessageHandler,
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

from chat_clients import *
from src.audio_to_text import AudioToText


load_dotenv()


logging.basicConfig(
    filename="./var/log/bot-ai.log",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=int(os.getenv("LOGGING_LEVEL")),
)


def createArgParser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--client")
    parser.add_argument("-m", "--model")
    parser.add_argument("-u", "--uri")

    return parser


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!"
    )


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    transcribed_voice = await send_transcribed_voice(update, context)

    message = transcribed_voice if transcribed_voice else update.message.text
    await send_answer(message, update, context)


async def send_transcribed_voice(update: Update, context) -> str:
    transcribed_voice = ""

    if update.message.voice:
        ogg_path = await download_voice(update.message.voice, context)

        wav_path = await audio_to_text.ogg2wav(ogg_path)
        if wav_path:
            transcribed_voice = await audio_to_text.get_text_from_audio(wav_path)

        message = (
            "your voice:" + transcribed_voice
            if "transcribed_voice" in locals()
            else "audio2text failed"
        )

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message,
        )

    return transcribed_voice


async def download_voice(voice: Voice, context) -> Path:
    # get basic info about the voice note file and prepare it for downloading
    new_file = await context.bot.get_file(voice.file_id)
    # download the voice note as a file
    return await new_file.download_to_drive(
        custom_path=os.getenv("TG_DIR_AUDIO") + Path(new_file.file_path).name
    )


async def send_answer(message: str, update: Update, context):
    answer = await chat_client.answer(message)

    await context.bot.send_message(chat_id=update.effective_chat.id, text=answer)


if __name__ == "__main__":
    parser = createArgParser()
    args = parser.parse_args()

    if args.client == "gpt4all":
        chat_client = Gpt4AllApiClient(args.uri, args.model)
    else:
        chat_client = OpenAiApiClient(args.uri, args.model)

    audio_to_text = AudioToText(os.getenv("WHISPER_MODEL"))
    application = ApplicationBuilder().token(os.getenv("TG_TOKEN")).build()

    start_handler = CommandHandler("start", start)
    application.add_handler(start_handler)

    echo_handler = MessageHandler(filters.CHAT | filters.AUDIO, echo)
    application.add_handler(echo_handler)

    application.run_polling()
