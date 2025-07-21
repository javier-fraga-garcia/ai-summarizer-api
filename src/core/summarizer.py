from google import genai

from core.logger import get_logger
from core.config import settings

logger = get_logger(__name__)


class Summarizer:
    client = genai.Client(api_key=settings.GEMINI_API_KEY)

    prompt = """
    You are an assistant specialized in generating accurate and faithful summaries of articles. Your task is to clearly and concisely summarize the content of the article provided by the user.

    IMPORTANT:
    - Always preserve the **original language** of the article. If the article is in Spanish, the summary must be in Spanish. Do not translate under any circumstances.
    - The summary must not exceed 150 words.
    - Focus solely on the key points and essential information from the article.
    - Do not include introductions, conclusions, opinions, or generic phrases.
    - Do not add any extra commentary; return only the summary text.
    - Be completely accurate and do not fabricate or infer any information that is not explicitly stated in the article.

    Here is the article:
    {article}
    """

    @classmethod
    def summarize(cls, content: str) -> str:
        logger.info("Summarizing content")
        message = cls.prompt.format(article=content)
        response = cls.client.models.generate_content(
            model=settings.GEMINI_MODEL, contents=message
        )
        return response.text
