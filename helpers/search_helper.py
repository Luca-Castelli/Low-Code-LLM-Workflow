import os

import requests
from dotenv import load_dotenv

from models.search_model import SearchItem, SearchResults

load_dotenv()


class GoogleCustomSearchClient:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        self.cx = os.getenv("CUSTOM_SEARCH_ENGINE_ID")

    def search(self, query: str) -> SearchResults:
        url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={self.api_key}&cx={self.cx}"
        response = requests.get(url)
        response.raise_for_status()
        json_data = response.json()
        return self.json_to_search_results(json_data, query)

    def json_to_search_results(self, json_data: dict, query: str) -> SearchResults:
        items = json_data.get("items", [])
        search_items = []
        for item in items:
            search_item = SearchItem(
                title=item.get("title", ""),
                link=item.get("link", ""),
                snippet=item.get("snippet", ""),
                source_metadata={
                    "API": f"Google Custom Search {self.cx}",
                    "query": query,
                },
            )
            search_items.append(search_item)
        return SearchResults(items=search_items)
