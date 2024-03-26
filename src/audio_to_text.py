import os
import whisper

from typing import Optional
from pathlib import Path
from pydub import AudioSegment


class AudioToText:
    __DIR_AUDIO = "./var/Audio/"

    def __init__(self, model: str):
        self.__whisperModel = whisper.load_model(model)

    def ogg2wav(self, path: Path) -> Optional[Path]:
        if path.suffix == ".oga":
            audio_path = str(path)

            audio = AudioSegment.from_file(audio_path)

            wav_name = path.name.replace(".oga", ".wav")
            wav_path = self.__DIR_AUDIO + wav_name
            audio.export(wav_path, format="wav")

            self.__remove_audio(audio_path)

            return Path(wav_path)

        return None

    def get_text_from_audio(self, path: Path) -> str:
        audio_path = str(path)

        result = self.__whisperModel.transcribe(audio_path)

        self.__remove_audio(audio_path)

        return result["text"]

    def __remove_audio(self, path: str) -> None:
        os.remove(path)
