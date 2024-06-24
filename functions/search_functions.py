from typing import List

from helpers.search_helper import GoogleCustomSearchClient
from models.search_model import SearchResult


def perform_search(query: str) -> List[SearchResult]:
    search_client = GoogleCustomSearchClient()
    search_results = search_client.search(f'"{query}"')
    return search_results
