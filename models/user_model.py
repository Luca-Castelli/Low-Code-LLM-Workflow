from pydantic import BaseModel, Field


class User(BaseModel):
    name: str = Field(..., description="name")
    age: int = Field(..., description="age")
    verified: bool = Field(default=False, description="dummy to test post-processing")
