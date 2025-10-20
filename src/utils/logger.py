"""
Logging system cho ứng dụng
"""

import logging
import logging.handlers
from pathlib import Path
from typing import Optional

from ..config import LOG_LEVEL, LOG_FORMAT, LOG_FILE


def setup_logging(log_level: str = LOG_LEVEL, log_file: Optional[Path] = None) -> None:
    """Setup logging configuration"""
    if log_file is None:
        log_file = LOG_FILE
    
    # Tạo thư mục logs nếu chưa có
    log_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Cấu hình root logger
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format=LOG_FORMAT,
        handlers=[
            # Console handler
            logging.StreamHandler(),
            # File handler với rotation
            logging.handlers.RotatingFileHandler(
                log_file,
                maxBytes=10*1024*1024,  # 10MB
                backupCount=5,
                encoding='utf-8'
            )
        ]
    )


def get_logger(name: str) -> logging.Logger:
    """Lấy logger cho module"""
    return logging.getLogger(name)
