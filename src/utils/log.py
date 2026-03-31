import logging

logger = None


class Logger:
    def __init__(self, log_file, severity_threshold):
        global logger

        self.log_file = log_file
        self.severity_threshold = severity_threshold

        self.logger = logging.getLogger(f"{__name__}.Logger")
        self.logger.setLevel(self.severity_threshold)

        handler = logging.FileHandler(self.log_file)
        formatter = logging.Formatter(
            '%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        )

        handler.setFormatter(formatter)

        self.logger.addHandler(handler)
        logger = self

    def send(self, message, severity=logging.INFO):
        self.logger.log(severity, message, stacklevel=2)
        if severity >= self.severity_threshold:
            print(f"{severity.real} - {message}")
