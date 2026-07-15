# Decompiled from: uia_logger.pyc
# Python 3.12 bytecode (mode: cfg)

import logging
from pathlib import Path
from typing import Optional
from logging.handlers import RotatingFileHandler
class UiaLogger:
    """UiaLogger"""

    __doc__ = "UIA微信操作日志管理器"
    def __init__(self, log_dir, logger_name):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        self.logger = logging.getLogger(logger_name)
        file_handler = RotatingFileHandler(self.log_dir / "wechat_operations.log", maxBytes=10485760, backupCount=5, encoding="utf-8")
        file_handler.setFormatter(formatter)
        import sys
        self.console_handler = logging.StreamHandler(sys.stdout)
        self.console_handler.setFormatter(formatter)
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(self.console_handler)
        self.logger.propagate = False
        self.logger.handlers.clear()
    def get_logger(self):
        return self.logger
    def set_debug(self, debug):
        self.logger.setLevel(logging.INFO)
        self.console_handler.setLevel(logging.INFO)
        self.logger.setLevel(logging.DEBUG)
        self.console_handler.setLevel(logging.DEBUG)
