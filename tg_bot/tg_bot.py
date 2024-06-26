from telegram.ext import ApplicationBuilder

from chat_clients.abstract_client import Client
from src.audio_to_text import AudioToText
from src.text_to_audio import TextToAudio

from .commands import Commands
from .chatAI import ChatAI


class TGBot:
    def __init__(
        self,
        token: str,
        chat_client: Client,
        audio_to_text: AudioToText,
        text_to_audio: TextToAudio | None,
    ):
        self.__application = ApplicationBuilder().token(token).build()

        # Command init
        commands = Commands()
        for handler in commands.handlers():
            self.__application.add_handler(handler)

        # Chat handler init
        chatAI = ChatAI(chat_client, audio_to_text, text_to_audio)
        for handler in chatAI.handlers():
            self.__application.add_handler(handler)

    def run(self) -> None:
        self.__application.run_polling()
