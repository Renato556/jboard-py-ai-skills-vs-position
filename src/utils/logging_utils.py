import logging


class LoggingUtils:

    @staticmethod
    def setup_logging(log_level: str = 'INFO') -> None:
        logging.basicConfig(
            level=getattr(logging, log_level.upper()),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler('app.log')
            ]
        )
