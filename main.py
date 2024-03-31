import os
import logging
import argparse

from dotenv import load_dotenv

from chat_clients import *
from tg_bot import TGBot
from src.audio_to_text import AudioToText
from src.text_to_audio import TextToAudio


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
    parser.add_argument("-u", "--url")

    return parser


if __name__ == "__main__":
    parser = createArgParser()
    args = parser.parse_args()

    if args.client == "gpt4all":
        chat_client = Gpt4AllApiClient(args.url, args.model)
    elif args.client == "ollama":
        chat_client = OllamaApiClient(args.url, args.model)
    else:
        chat_client = OpenAiApiClient(args.url, args.model)

    audio_to_text = AudioToText(os.getenv("WHISPER_MODEL"))
    if TextToAudio.isActive():
        text_to_audio = TextToAudio("tts_models/multilingual/multi-dataset/xtts_v2")
    else:
        text_to_audio = None

    TG_Bot = TGBot(os.getenv("TG_TOKEN"), chat_client, audio_to_text, text_to_audio)

    TG_Bot.run()
