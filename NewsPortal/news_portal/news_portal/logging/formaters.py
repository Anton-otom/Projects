import logging


class CustomConsoleFormatter(logging.Formatter):
    def format(self, record):
        message = super().format(record)
        if record.levelno >= logging.WARNING:
            message += f" | {record.pathname}"
        if record.levelno >= logging.ERROR and record.exc_info:
            message += f"\n{self.formatException(record.exc_info)}"
        return message
