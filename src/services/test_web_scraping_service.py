import unittest
from unittest.mock import Mock, patch
import requests
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.services import WebScrapingService


class TestWebScrapingService(unittest.TestCase):

    def setUp(self):
        self.service = WebScrapingService()
        self.service_with_custom_timeout = WebScrapingService(timeout=5)

    def test_init_default_timeout(self):
        service = WebScrapingService()
        self.assertEqual(service.timeout, 10)

    def test_init_custom_timeout(self):
        service = WebScrapingService(timeout=5)
        self.assertEqual(service.timeout, 5)

    @patch('services.web_scraping_service.requests.get')
    def test_fetch_page_content_success(self, mock_get):
        mock_response = Mock()
        mock_response.content = b"<html><body>Test content</body></html>"
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        url = "https://example.com"
        result = self.service.fetch_page_content(url)

        self.assertEqual(result, b"<html><body>Test content</body></html>")
        mock_get.assert_called_once_with(url, timeout=10)
        mock_response.raise_for_status.assert_called_once()

    @patch('services.web_scraping_service.requests.get')
    def test_fetch_page_content_with_custom_timeout(self, mock_get):
        mock_response = Mock()
        mock_response.content = b"content"
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        url = "https://example.com"
        result = self.service_with_custom_timeout.fetch_page_content(url)

        self.assertEqual(result, b"content")
        mock_get.assert_called_once_with(url, timeout=5)

    @patch('services.web_scraping_service.requests.get')
    @patch('builtins.print')
    def test_fetch_page_content_timeout_error(self, mock_print, mock_get):
        mock_get.side_effect = requests.exceptions.Timeout("Timeout occurred")

        with self.assertRaises(requests.exceptions.Timeout):
            self.service.fetch_page_content("https://example.com")

        mock_print.assert_called_with("[WEB_SCRAPING] ERRO: Timeout após 10s")

    @patch('services.web_scraping_service.requests.get')
    @patch('builtins.print')
    def test_fetch_page_content_http_error(self, mock_print, mock_get):
        http_error = requests.exceptions.HTTPError("404 Not Found")
        mock_get.side_effect = http_error

        with self.assertRaises(requests.exceptions.HTTPError):
            self.service.fetch_page_content("https://example.com")

        mock_print.assert_called_with(f"[WEB_SCRAPING] ERRO HTTP: {http_error}")

    @patch('services.web_scraping_service.requests.get')
    @patch('builtins.print')
    def test_fetch_page_content_request_exception(self, mock_print, mock_get):
        request_error = requests.exceptions.RequestException("Connection failed")
        mock_get.side_effect = request_error

        with self.assertRaises(requests.exceptions.RequestException):
            self.service.fetch_page_content("https://example.com")

        mock_print.assert_called_with(f"[WEB_SCRAPING] ERRO de requisição: {request_error}")

    def test_extract_meta_description_success(self):
        html_content = '''
        <html>
            <head>
                <meta name="description" content="Esta é uma descrição de teste">
            </head>
            <body>Content</body>
        </html>
        '''

        result = self.service.extract_meta_description(html_content)
        self.assertEqual(result, "Esta é uma descrição de teste")

    def test_extract_meta_description_no_meta_tag(self):
        html_content = '''
        <html>
            <head>
                <title>Test Page</title>
            </head>
            <body>Content</body>
        </html>
        '''

        result = self.service.extract_meta_description(html_content)
        self.assertIsNone(result)

    def test_extract_meta_description_empty_content(self):
        html_content = '''
        <html>
            <head>
                <meta name="description" content="">
            </head>
            <body>Content</body>
        </html>
        '''

        result = self.service.extract_meta_description(html_content)
        self.assertIsNone(result)

    def test_extract_meta_description_no_content_attribute(self):
        html_content = '''
        <html>
            <head>
                <meta name="description">
            </head>
            <body>Content</body>
        </html>
        '''

        result = self.service.extract_meta_description(html_content)
        self.assertIsNone(result)

    def test_extract_meta_description_multiple_meta_tags(self):
        html_content = '''
        <html>
            <head>
                <meta name="description" content="Primeira descrição">
                <meta name="description" content="Segunda descrição">
            </head>
            <body>Content</body>
        </html>
        '''

        result = self.service.extract_meta_description(html_content)
        self.assertEqual(result, "Primeira descrição")

    def test_extract_meta_description_case_insensitive(self):
        html_content = '''
        <html>
            <head>
                <meta name="DESCRIPTION" content="Descrição maiúscula">
            </head>
            <body>Content</body>
        </html>
        '''

        result = self.service.extract_meta_description(html_content)
        self.assertIsNone(result)

    @patch('builtins.print')
    def test_extract_meta_description_invalid_html(self, mock_print):
        html_content = None

        with self.assertRaises(Exception):
            self.service.extract_meta_description(html_content)

        self.assertTrue(mock_print.called)
        args = mock_print.call_args[0][0]
        self.assertTrue(args.startswith("[META_EXTRACTION] ERRO:"))

    def test_extract_meta_description_special_characters(self):
        html_content = '''
        <html>
            <head>
                <meta name="description" content="Descrição com ç, á, é, ã e outros acentos">
            </head>
            <body>Content</body>
        </html>
        '''

        result = self.service.extract_meta_description(html_content)
        self.assertEqual(result, "Descrição com ç, á, é, ã e outros acentos")

    def test_extract_meta_description_whitespace_content(self):
        html_content = '''
        <html>
            <head>
                <meta name="description" content="   ">
            </head>
            <body>Content</body>
        </html>
        '''

        result = self.service.extract_meta_description(html_content)
        self.assertEqual(result, "   ")


if __name__ == '__main__':
    unittest.main()
