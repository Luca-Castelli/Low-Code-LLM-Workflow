from pydantic import BaseModel, Field


class Answer(BaseModel):
    answer: str = Field(..., description="answer to the question")
