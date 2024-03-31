import os


from datetime import datetime
from TTS.api import TTS


class TextToAudio:
    __DIR_AUDIO = "./var/Audio/"

    def __init__(self, model: str):
        self.__tts = TTS(model).to(os.getenv("TTS_DEVICE"))

    def isActive() -> bool:
        return bool(os.getenv("TTS_SPEAKER"))

    def generate(self, answer: str, user: int) -> str:
        answer_wav = self.__generate_name(user)

        self.__tts.tts_to_file(
            text=answer,
            file_path=answer_wav,
            speaker=self.__get_speaker(),
            speaker_wav=self.__get_speaker_wav(),
            language=os.getenv("TTS_LANGUAGE"),
            split_sentences=True,
        )

        return answer_wav

    def remove(self, path: str):
        os.remove(path)

    def __generate_name(self, user: int) -> str:
        current_datetime = datetime.now()
        date_string = current_datetime.strftime("%Y%m%d_%H%M%S")

        return f"{self.__DIR_AUDIO}answer-{date_string}-{user}.wav"

    def __get_speaker(self) -> str | None:
        speaker = os.getenv("TTS_SPEAKER")

        return None if speaker.endswith(".wav") else speaker

    def __get_speaker_wav(self) -> str | None:
        speaker = os.getenv("TTS_SPEAKER")

        return speaker if speaker.endswith(".wav") else None
