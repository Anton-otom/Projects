import logging


class CustomConsoleFormatter(logging.Formatter):
    def format(self, record):
        base_format = f"{record.asctime} {record.levelname} {record.message}"
        if record.levelno >= logging.WARNING:
            base_format += f" | {record.pathname}"
        if record.levelno >= logging.ERROR and record.exc_info:
            base_format += f"\n{self.formatException(record.exc_info)}"
        return base_format
