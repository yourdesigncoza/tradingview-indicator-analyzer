import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logging():
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            RotatingFileHandler(
                'logs/scraper.log',
                maxBytes=1024*1024,  # 1MB
                backupCount=5
            ),
            logging.StreamHandler()
        ]
    )

    # Add specific loggers
    scraper_logger = logging.getLogger('scraper')
    analyzer_logger = logging.getLogger('analyzer')
    
    return scraper_logger, analyzer_logger