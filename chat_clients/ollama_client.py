import httpx

from .abstract_client import Client


class OllamaApiClient(Client):
    def __init__(self, url: str, model: str):
        super().__init__(url, model)

        self.__client = httpx.AsyncClient(base_url=url, timeout=120)

    async def _request(self, messages: list):
        data = {
            "model": self._model,
            "messages": messages,
            "stream": False,
        }

        return await self.__client.post("/chat", json=data)

    def _getMessage(self, response) -> str:
        data = response.json()

        if "message" not in data or "content" not in data["message"]:
            raise ValueError("Response is not correct")

        return data["message"]["content"]
