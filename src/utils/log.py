import logging
import sys

from constant import LOG_COLORS, LOG_COLORS_RESET

logger = None


class ColoredFormatter(logging.Formatter):
    def format(self, record):
        color = LOG_COLORS.get(record.levelno, LOG_COLORS_RESET)
        record.levelname = f"{color}{record.levelname}{LOG_COLORS_RESET}"
        return super().format(record)


class Logger:
    def __init__(self, log_file, severity_threshold):
        global logger

        self.log_file = log_file
        self.severity_threshold = severity_threshold

        self.logger = logging.getLogger(f"{__name__}.Logger")
        self.logger.setLevel(self.severity_threshold)

        # File handler (no colors)
        file_handler = logging.FileHandler(self.log_file)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        ))

        # Console handler (with colors)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(ColoredFormatter(
            '%(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        ))

        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

        logger = self

    def send(self, message, severity=logging.INFO):
        self.logger.log(severity, message, stacklevel=2)
