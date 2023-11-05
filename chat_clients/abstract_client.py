import logging

from abc import ABC, abstractmethod


class Client(ABC):
    def __init__(self, server: str, model: str):
        self.server = server
        self.model = model

    async def answer(self, message: str) -> str:
        try:
            response = self._request(message)
            answer = self._getMessage(response)
        except Exception as e:
            logging.critical("Server unavailable: %s", e)

            answer = "Server unavailable"

        return answer

    @abstractmethod
    def _request(self, message: str):
        pass

    @abstractmethod
    def _getMessage(self, response) -> str:
        pass
