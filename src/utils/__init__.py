from .logging_utils import LoggingUtils
from .validation_utils import ValidationUtils

def setup_logging(log_level: str = 'INFO') -> None:
    return LoggingUtils.setup_logging(log_level)

def validate_url(url: str) -> bool:
    return ValidationUtils.validate_url(url)

def sanitize_input(data):
    return ValidationUtils.sanitize_input(data)

__all__ = [
    'LoggingUtils',
    'ValidationUtils',
    'setup_logging',
    'validate_url',
    'sanitize_input'
]
