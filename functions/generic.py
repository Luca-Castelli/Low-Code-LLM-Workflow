from helpers.llm_client import LLMClient
from models.generic_model import Answer


def chat(query: str) -> Answer:
    llm_client = LLMClient(model_name="gpt-4o")
    return llm_client.call_with_data_model(query, Answer)
