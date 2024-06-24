from typing import List

from helpers.llm_client import LLMClient
from helpers.scrape_helper import ScrapeClient
from models.article_model import Article, ArticleSummary
from models.search_model import SearchResult


def scrape_articles(search_results: List[SearchResult]) -> List[Article]:
    scraper = ScrapeClient()
    articles = []
    for search_result in search_results:
        content = scraper.scrape_article(search_result.link)
        article = Article(
            title=search_result.title,
            link=search_result.link,
            content=content,
        )
        articles.append(article)
    return articles


def summarize_article(article: Article, prompt: str) -> Article:
    formatted_prompt = prompt.format(
        title=article.title, link=article.link, content=article.content
    )
    llm_client = LLMClient(model_name="gpt-4o")
    article_summary = llm_client.call_with_data_model(formatted_prompt, ArticleSummary)
    article.summary = article_summary.summary
    return article


def summarize_articles(articles: List[Article], prompt: str) -> List[Article]:
    return [summarize_article(article, prompt) for article in articles]
