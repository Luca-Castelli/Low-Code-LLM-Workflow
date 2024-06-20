from dotenv import load_dotenv
from instructor import from_openai
from openai import OpenAI
from pydantic import BaseModel

load_dotenv()


class LLMClient:

    def __init__(self, model_name: str):
        self.model_name = model_name
        self.client = self._initialize_client()

    def _initialize_client(self):
        return from_openai(OpenAI())

    def call(self, prompt: str, data_model: BaseModel) -> BaseModel:

        response = self.client.chat.completions.create(
            model=self.model_name,
            response_model=data_model,
            messages=[
                {"role": "system", "content": ""},
                {"role": "user", "content": prompt},
            ],
        )
        return response
