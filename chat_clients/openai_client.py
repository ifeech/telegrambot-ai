import openai

from .abstract_client import Client


class OpenAiApiClient(Client):
    def __init__(self, url: str, model: str, api_key: str = ""):
        super().__init__(url, model)

        self.openai = openai
        self.openai.base_url = url
        self.openai.api_key = api_key

    def _request(self, messages: list):
        return self.openai.chat.completions.create(model=self._model, messages=messages)

    def _getMessage(self, response) -> str:
        return response.choices[0].message.content
