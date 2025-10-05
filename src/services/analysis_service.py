from src.models import AnalysisRequest
from .web_scraping_service import WebScrapingService
from .text_processing_service import TextProcessingService
from .openai_service import OpenAIService


class AnalysisService:

    def __init__(self):
        self.web_scraper = WebScrapingService()
        self.text_processor = TextProcessingService()
        self.openai_service = OpenAIService()

    def analyze_position(self, request: AnalysisRequest, api_key: str, api_url: str = None) -> dict:
        try:
            html_content = self.web_scraper.fetch_page_content(request.position)
            raw_description = self.web_scraper.extract_meta_description(html_content)

            if not raw_description:
                raise ValueError("Meta description não encontrada")

            formatted_description = self.text_processor.format_description(raw_description)
            ai_analysis = self.openai_service.analyze_match(
                request.skills,
                formatted_description,
                api_key,
                api_url
            )

            return {"message": ai_analysis}

        except Exception as e:
            print(f"[ANALYSIS] ERRO: {str(e)}")
            raise
