from pydantic import BaseModel, Field


class Article(BaseModel):
    title: str = Field(..., description="Title of the article")
    link: str = Field(..., description="Link to the article")
    content: str = Field(..., description="Content of the article")
    summary: str = Field(default="", description="Summary of the article")


class ArticleSummary(BaseModel):
    summary: str = Field(..., description="Summary of the article")
