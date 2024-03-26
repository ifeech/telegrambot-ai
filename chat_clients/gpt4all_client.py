from .openai_client import OpenAiApiClient


class Gpt4AllApiClient(OpenAiApiClient):
    async def _request(self, messages: list):
        return await self.openai.completions.create(
            model=self._model,
            prompt=messages[0],
            max_tokens=100,
            temperature=0.9,
            top_p=0.9,
            top_k=40,
            repeat_penalty=1.1,
            repeat_last_n=64,
            n=9,
            echo=True,
            stream=False,
        )

    def _getMessage(self, response) -> str:
        return response.choices[0].text
