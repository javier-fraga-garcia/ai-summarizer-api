import re
from newspaper import Article

from logger import get_logger

logger = get_logger(__name__)


class Scraper:
    @staticmethod
    def scrape(self, url):
        logger.info(f"Scraping content from {url}")
        article = Article(url)
        article.download()
        article.parse()
        text = article.text
        if not text:
            raise Exception(f"Text content for ${url} not detected")
        cleaned_text = re.sub(r"\s+", " ", text).strip()
        return cleaned_text
