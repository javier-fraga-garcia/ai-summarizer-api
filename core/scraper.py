import re
from newspaper import Article

from logger import get_logger

logger = get_logger(__name__)


class Scraper:
    def __init__(self, url):
        self.url = url

    def scrape(self):
        logger.info(f"Scraping content from {self.url}")
        article = Article(self.url)
        article.download()
        article.parse()
        text = article.text
        if not text:
            raise Exception(f"Text content for ${self.url} not detected")
        cleaned_text = re.sub(r"\s+", " ", text).strip()
        return cleaned_text
