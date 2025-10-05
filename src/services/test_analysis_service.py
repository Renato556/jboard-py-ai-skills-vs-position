import unittest
from unittest.mock import Mock, patch
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.services import AnalysisService
from src.models import AnalysisRequest


class TestAnalysisService(unittest.TestCase):

    def setUp(self):
        self.service = AnalysisService()

        self.mock_web_scraper = Mock()
        self.mock_text_processor = Mock()
        self.mock_openai_service = Mock()

        self.service.web_scraper = self.mock_web_scraper
        self.service.text_processor = self.mock_text_processor
        self.service.openai_service = self.mock_openai_service

    def test_init_creates_services(self):
        service = AnalysisService()

        self.assertIsNotNone(service.web_scraper)
        self.assertIsNotNone(service.text_processor)
        self.assertIsNotNone(service.openai_service)

    def test_analyze_position_success_complete_flow(self):
        self.mock_web_scraper.fetch_page_content.return_value = "<html><meta name='description' content='Job description'/></html>"
        self.mock_web_scraper.extract_meta_description.return_value = "Desenvolvedor Python com experiência em Flask"
        self.mock_text_processor.format_description.return_value = "Desenvolvedor Python com experiência em Flask"
        self.mock_openai_service.analyze_match.return_value = "Match de 85% - Candidato tem boa compatibilidade"

        request = AnalysisRequest(
            position="https://example.com/job",
            skills=["Python", "Flask", "API"]
        )

        result = self.service.analyze_position(request, "test-api-key", "https://test-api.com")

        self.assertEqual(result, {"message": "Match de 85% - Candidato tem boa compatibilidade"})

        self.mock_web_scraper.fetch_page_content.assert_called_once_with("https://example.com/job")
        self.mock_web_scraper.extract_meta_description.assert_called_once_with("<html><meta name='description' content='Job description'/></html>")
        self.mock_text_processor.format_description.assert_called_once_with("Desenvolvedor Python com experiência em Flask")
        self.mock_openai_service.analyze_match.assert_called_once_with(
            ["Python", "Flask", "API"],
            "Desenvolvedor Python com experiência em Flask",
            "test-api-key",
            "https://test-api.com"
        )

    def test_analyze_position_with_default_api_url(self):
        self.mock_web_scraper.fetch_page_content.return_value = "<html>content</html>"
        self.mock_web_scraper.extract_meta_description.return_value = "Job description"
        self.mock_text_processor.format_description.return_value = "Job description"
        self.mock_openai_service.analyze_match.return_value = "Analysis result"

        request = AnalysisRequest(position="https://example.com/job", skills=["Python"])

        self.service.analyze_position(request, "test-api-key")

        self.mock_openai_service.analyze_match.assert_called_once_with(
            ["Python"],
            "Job description",
            "test-api-key",
            None
        )

    def test_analyze_position_no_meta_description_found(self):
        self.mock_web_scraper.fetch_page_content.return_value = "<html>content without meta</html>"
        self.mock_web_scraper.extract_meta_description.return_value = None

        request = AnalysisRequest(position="https://example.com/job", skills=["Python"])

        with self.assertRaises(ValueError) as context:
            self.service.analyze_position(request, "test-api-key")

        self.assertEqual(str(context.exception), "Meta description não encontrada")

        self.mock_text_processor.format_description.assert_not_called()
        self.mock_openai_service.analyze_match.assert_not_called()

    def test_analyze_position_empty_meta_description(self):
        self.mock_web_scraper.fetch_page_content.return_value = "<html>content</html>"
        self.mock_web_scraper.extract_meta_description.return_value = ""

        request = AnalysisRequest(position="https://example.com/job", skills=["Python"])

        with self.assertRaises(ValueError):
            self.service.analyze_position(request, "test-api-key")

    def test_analyze_position_web_scraper_exception(self):
        self.mock_web_scraper.fetch_page_content.side_effect = Exception("Network error")

        request = AnalysisRequest(position="https://invalid-url.com", skills=["Python"])

        with self.assertRaises(Exception):
            self.service.analyze_position(request, "test-api-key")

    def test_analyze_position_openai_service_exception(self):
        self.mock_web_scraper.fetch_page_content.return_value = "<html>content</html>"
        self.mock_web_scraper.extract_meta_description.return_value = "Job description"
        self.mock_text_processor.format_description.return_value = "Job description"
        self.mock_openai_service.analyze_match.side_effect = Exception("OpenAI API error")

        request = AnalysisRequest(position="https://example.com/job", skills=["Python"])

        with self.assertRaises(Exception):
            self.service.analyze_position(request, "test-api-key")

    @patch('builtins.print')
    def test_analyze_position_logs_error_and_reraises(self, mock_print):
        self.mock_web_scraper.fetch_page_content.side_effect = ValueError("Test error")

        request = AnalysisRequest(position="https://example.com/job", skills=["Python"])

        with self.assertRaises(ValueError):
            self.service.analyze_position(request, "test-api-key")

        mock_print.assert_called_with("[ANALYSIS] ERRO: Test error")

    def test_analyze_position_with_empty_skills_list(self):
        self.mock_web_scraper.fetch_page_content.return_value = "<html>content</html>"
        self.mock_web_scraper.extract_meta_description.return_value = "Job description"
        self.mock_text_processor.format_description.return_value = "Job description"
        self.mock_openai_service.analyze_match.return_value = "Candidato precisa desenvolver skills"

        request = AnalysisRequest(position="https://example.com/job", skills=[])

        self.service.analyze_position(request, "test-api-key")

        self.mock_openai_service.analyze_match.assert_called_once_with(
            [],
            "Job description",
            "test-api-key",
            None
        )

    def test_analyze_position_with_many_skills(self):
        self.mock_web_scraper.fetch_page_content.return_value = "<html>content</html>"
        self.mock_web_scraper.extract_meta_description.return_value = "Complex job description"
        self.mock_text_processor.format_description.return_value = "Complex job description"
        self.mock_openai_service.analyze_match.return_value = "Detailed analysis"

        many_skills = ["Python", "Flask", "Django", "FastAPI", "PostgreSQL", "Redis", "Docker", "Kubernetes", "AWS", "Git"]
        request = AnalysisRequest(position="https://example.com/job", skills=many_skills)

        self.service.analyze_position(request, "test-api-key")

        self.mock_openai_service.analyze_match.assert_called_once_with(
            many_skills,
            "Complex job description",
            "test-api-key",
            None
        )

    def test_analyze_position_with_special_characters_in_url(self):
        self.mock_web_scraper.fetch_page_content.return_value = "<html>content</html>"
        self.mock_web_scraper.extract_meta_description.return_value = "Job description"
        self.mock_text_processor.format_description.return_value = "Job description"
        self.mock_openai_service.analyze_match.return_value = "Analysis result"

        special_url = "https://example.com/job?id=123&category=dev&lang=pt-BR"
        request = AnalysisRequest(position=special_url, skills=["Python"])

        self.service.analyze_position(request, "test-api-key")

        self.mock_web_scraper.fetch_page_content.assert_called_once_with(special_url)

    def test_analyze_position_text_processor_formats_correctly(self):
        raw_description = "  Job   description\n\nwith   extra   spaces  "
        formatted_description = "Job description with extra spaces"

        self.mock_web_scraper.fetch_page_content.return_value = "<html>content</html>"
        self.mock_web_scraper.extract_meta_description.return_value = raw_description
        self.mock_text_processor.format_description.return_value = formatted_description
        self.mock_openai_service.analyze_match.return_value = "Analysis result"

        request = AnalysisRequest(position="https://example.com/job", skills=["Python"])

        self.service.analyze_position(request, "test-api-key")

        self.mock_text_processor.format_description.assert_called_once_with(raw_description)

        self.mock_openai_service.analyze_match.assert_called_once_with(
            ["Python"],
            formatted_description,
            "test-api-key",
            None
        )

    def test_analyze_position_preserves_api_key(self):
        self.mock_web_scraper.fetch_page_content.return_value = "<html>content</html>"
        self.mock_web_scraper.extract_meta_description.return_value = "Job description"
        self.mock_text_processor.format_description.return_value = "Job description"
        self.mock_openai_service.analyze_match.return_value = "Analysis result"

        api_key = "sk-proj-very-secret-api-key-12345"
        request = AnalysisRequest(position="https://example.com/job", skills=["Python"])

        self.service.analyze_position(request, api_key)

        self.mock_openai_service.analyze_match.assert_called_once_with(
            ["Python"],
            "Job description",
            api_key,
            None
        )

    def test_analyze_position_returns_correct_format(self):
        self.mock_web_scraper.fetch_page_content.return_value = "<html>content</html>"
        self.mock_web_scraper.extract_meta_description.return_value = "Job description"
        self.mock_text_processor.format_description.return_value = "Job description"
        ai_response = "Match de 90% - Excelente compatibilidade"
        self.mock_openai_service.analyze_match.return_value = ai_response

        request = AnalysisRequest(position="https://example.com/job", skills=["Python"])

        result = self.service.analyze_position(request, "test-api-key")

        self.assertIsInstance(result, dict)
        self.assertIn("message", result)
        self.assertEqual(result["message"], ai_response)


if __name__ == '__main__':
    unittest.main()
