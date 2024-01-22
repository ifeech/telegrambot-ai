import requests

from .abstract_client import Client


class OllamaApiClient(Client):
    def _request(self, message: str):
        # Формирование JSON-данных для отправки на другой сервер
        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": message}],
            "stream": False,
        }

        return requests.post(f"{self.server}/chat", json=data).json()

    def _getMessage(self, response) -> str:
        return response["message"]["content"]
