import requests
from bs4 import BeautifulSoup
from typing import Optional


class WebScrapingService:

    def __init__(self, timeout: int = 10):
        self.timeout = timeout

    def fetch_page_content(self, url: str) -> str:
        try:
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response.content

        except requests.exceptions.Timeout:
            print(f"[WEB_SCRAPING] ERRO: Timeout após {self.timeout}s")
            raise
        except requests.exceptions.HTTPError as e:
            print(f"[WEB_SCRAPING] ERRO HTTP: {e}")
            raise
        except requests.exceptions.RequestException as e:
            print(f"[WEB_SCRAPING] ERRO de requisição: {e}")
            raise

    def extract_meta_description(self, html_content: str) -> Optional[str]:
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            meta_description = soup.find('meta', attrs={'name': 'description'})

            if meta_description:
                content = meta_description.get('content')
                if content:
                    return content

            return None

        except Exception as e:
            print(f"[META_EXTRACTION] ERRO: {e}")
            raise
