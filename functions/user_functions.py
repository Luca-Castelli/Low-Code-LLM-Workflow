from helpers.llm_client import LLMClient
from models.user_model import User


def pre_process_user(content: str) -> str:
    return content.upper()


def extract_user(content: str) -> User:
    llm_client = LLMClient(model_name="gpt-4o")
    return llm_client.call(content, User)


def post_process_user(user: User) -> User:
    user.verified = True
    return user
