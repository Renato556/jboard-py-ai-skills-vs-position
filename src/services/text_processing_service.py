import re


class TextProcessingService:

    @staticmethod
    def format_description(description: str) -> str:
        return re.sub(r'\s+', ' ', description).strip()
