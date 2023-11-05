import openai

from .abstract_client import Client


class OpenAiApiClient(Client):
    def __init__(self, server: str, model: str):
        super().__init__(server, model)

        self.openai = openai
        self.openai.base_url = server
        self.openai.api_key = ""

    def _request(self, message: str):
        return self.openai.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": message,
                }
            ],
        )

    def _getMessage(self, response) -> str:
        return response.choices[0].message.content
