import re

import requests


class ScrapeClient:
    def scrape_article(self, link: str) -> str:
        headers = {"Accept": "application/json"}
        response = requests.get(f"https://r.jina.ai/{link}", headers=headers)
        response.raise_for_status()
        json_data = response.json()
        content = json_data["data"]["content"]
        cleaned_content = self._preprocess_content(content)
        return cleaned_content

    def _preprocess_content(self, content: str) -> str:
        # Remove special characters and extra spaces
        content = re.sub(r"[^a-zA-Z0-9\s]", "", content)
        content = re.sub(r"\s+", " ", content).strip()
        return content
