# models/search_model.py
from typing import Dict

from pydantic import BaseModel, Field


class SearchItem(BaseModel):
    title: str = Field(..., description="Title of the search result item")
    link: str = Field(..., description="Link to the search result item")
    snippet: str = Field(..., description="Snippet of the search result item")
    source_metadata: Dict[str, str] = Field(
        default_factory=dict,
        description="Metata for the search that produced the search result item.",
    )


class SearchResults(BaseModel):
    items: list[SearchItem] = Field(..., description="List of search result items")
