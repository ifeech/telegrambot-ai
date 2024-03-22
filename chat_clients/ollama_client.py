import requests

from .abstract_client import Client


class OllamaApiClient(Client):
    def _request(self, messages: list):
        # Формирование JSON-данных для отправки на другой сервер
        data = {
            "model": self._model,
            "messages": messages,
            "stream": False,
        }

        return requests.post(f"{self._url}/chat", json=data).json()

    def _getMessage(self, response) -> str:
        return response["message"]["content"]
