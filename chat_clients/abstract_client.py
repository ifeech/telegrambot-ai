import logging

from abc import ABC, abstractmethod


class Client(ABC):
    def __init__(self, url: str, model: str):
        self._url = url
        self._model = model

    async def answer(self, messages: list) -> str:
        try:
            response = await self._request(messages)
            answer = self._getMessage(response)
        except Exception as e:
            logging.critical("Server unavailable: %s", e)

            answer = "Server unavailable"

        return answer

    @abstractmethod
    async def _request(self, messages: list):
        pass

    @abstractmethod
    def _getMessage(self, response) -> str:
        pass
