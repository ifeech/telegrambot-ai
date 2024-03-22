import os
from pathlib import Path
from telegram import Update
from telegram.ext import filters, ContextTypes, MessageHandler

from chat_clients.abstract_client import Client
from src.audio_to_text import AudioToText


class ChatAI:
    def __init__(self, chat_client: Client, audio_to_text: AudioToText):
        self.__chat_client = chat_client
        self.__audio_to_text = audio_to_text

    async def __text(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if context.user_data.get("waiting_for_message"):
            context.user_data["chat_session"].append(
                {"role": "system", "content": update.message.text}
            )
            context.user_data["waiting_for_message"] = False
        elif update.message.text:
            answer = self.__generate_answer(update.message.text, context.user_data)
            await update.message.reply_text(answer)

    async def __voice(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if update.message.voice:
            # get basic info about the voice note file and prepare it for downloading
            new_file = await context.bot.get_file(update.message.voice.file_id)
            # download the voice note as a file
            ogg_path = await new_file.download_to_drive(
                custom_path=os.getenv("TG_DIR_AUDIO") + Path(new_file.file_path).name
            )

            wav_path = self.__audio_to_text.ogg2wav(ogg_path)
            if wav_path:
                transcribed_voice = self.__audio_to_text.get_text_from_audio(wav_path)
                if transcribed_voice:
                    await update.message.reply_text("your voice: " + transcribed_voice)

                    answer = self.__generate_answer(
                        transcribed_voice, context.user_data
                    )
                    await update.message.reply_text(answer)
                else:
                    await update.message.reply_text("audio not recognized")
            else:
                await update.message.reply_text("audio not found")

    def __generate_answer(self, message: str, user_data: dict):
        if "chat_session" not in user_data:
            user_data["chat_session"] = []

        user_data["chat_session"].append({"role": "user", "content": message})

        answer = self.__chat_client.answer(user_data["chat_session"])
        user_data["chat_session"].append({"role": "assistant", "content": answer})

        return answer

    def handlers(self):
        return [
            MessageHandler(filters.TEXT, self.__text),
            MessageHandler(filters.VOICE, self.__voice),
        ]
