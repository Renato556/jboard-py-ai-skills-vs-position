from urllib.parse import urlparse
from typing import Any, Dict


class ValidationUtils:

    @staticmethod
    def validate_url(url: str) -> bool:
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False

    @staticmethod
    def sanitize_input(data: Dict[str, Any]) -> Dict[str, Any]:
        if isinstance(data, dict):
            return {k: ValidationUtils.sanitize_input(v) if isinstance(v, (dict, list)) else str(v).strip()
                    for k, v in data.items()}
        elif isinstance(data, list):
            return [ValidationUtils.sanitize_input(item) for item in data]
        return data
