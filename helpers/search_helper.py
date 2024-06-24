import os
from typing import List

from dotenv import load_dotenv
from googleapiclient.discovery import build

from models.search_model import SearchResult

load_dotenv()


class GoogleCustomSearchClient:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        self.cx = os.getenv("CUSTOM_SEARCH_ENGINE_ID")
        self.service = build("customsearch", "v1", developerKey=self.api_key)
        self.results_per_page = 10

    def search(self, query: str, num_results: int = 100) -> List[SearchResult]:
        results = []
        try:
            for i in range(0, num_results, self.results_per_page):
                start = i + 1  # start parameter is 1-based
                response = (
                    self.service.cse()
                    .list(
                        q=query,
                        cx=self.cx,
                        start=start,
                        num=self.results_per_page,
                    )
                    .execute()
                )
                items = response.get("items", [])
                for item in items:
                    item["source_metadata"] = {
                        "API": f"Google Custom Search ({self.cx})",
                        "query": query,
                    }
                results.extend(items)
                if len(items) < self.results_per_page:
                    break  # Exit if fewer than results_per_page results are returned (end of results)
        except Exception as e:
            print(f"Error during search: {e}")

        return self.json_to_search_results(results, query)

    def json_to_search_results(
        self, json_data: List[dict], query: str
    ) -> List[SearchResult]:
        search_results = []
        for item in json_data:
            search_result = SearchResult(
                title=item.get("title", ""),
                link=item.get("link", ""),
                snippet=item.get("snippet", ""),
                source_metadata=item.get("source_metadata", {}),
            )
            search_results.append(search_result)
        return search_results
