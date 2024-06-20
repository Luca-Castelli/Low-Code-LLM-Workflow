import requests


class ArticleScraper:
    def scrape_article(self, link: str) -> str:
        headers = {"Accept": "application/json"}
        response = requests.get(f"https://r.jina.ai/{link}", headers=headers)
        response.raise_for_status()
        json_data = response.json()
        return json_data["data"]["content"][:1000]
