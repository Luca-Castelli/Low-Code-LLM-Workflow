# functions/search_functions.py
from helpers.search_helper import GoogleCustomSearchClient
from models.search_model import SearchResults


def perform_search(query: str) -> SearchResults:
    search_client = GoogleCustomSearchClient()
    return search_client.search(f'"{query}"')


def extract_titles(results: SearchResults) -> list:
    return [item.title for item in results.items]


def post_process_titles(titles: list) -> list:
    return [title.upper() for title in titles]
