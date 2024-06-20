from helpers.llm_client import LLMClient
from helpers.scrape_helper import ArticleScraper
from models.article_model import Article, ArticleSummary
from models.search_model import SearchResults


def scrape_articles(search_results: SearchResults) -> list[Article]:
    scraper = ArticleScraper()
    articles = []
    for search_result in search_results.items:
        content = scraper.scrape_article(search_result.link)
        article = Article(
            title=search_result.title,
            link=search_result.link,
            content=content,
        )
        articles.append(article)
    return articles


def summarize_article(article: Article) -> ArticleSummary:
    prompt = f"Summarize the following article:\n\nTitle: {article.title}\n\nLink: {article.link}\n\nContent: {article.content}"
    llm_client = LLMClient(model_name="gpt-4o")
    return llm_client.call(prompt, ArticleSummary)


def summarize_articles(articles: list[Article]) -> list[ArticleSummary]:
    return [summarize_article(article) for article in articles]
