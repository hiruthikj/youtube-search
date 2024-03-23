from logging import CRITICAL, DEBUG, ERROR, INFO, WARNING, Formatter, LogRecord

from ..config import settings

PROJECT_NAME = settings.PROJECT_NAME
ENABLE_COLOR_LOGS = settings.DEBUG
LOG_REQUEST_ID = settings.LOG_REQUEST_ID
LOG_CORRELATION_ID = settings.LOG_CORRELATION_ID


def get_colored_message(msg, levelno):
    GREY = "\x1b[38;20m"
    BLUE = "\033[94m"
    YELLOW = "\x1b[33;20m"
    RED = "\x1b[31;20m"
    BOLD_RED = "\x1b[31;1m"
    RESET = "\x1b[0m"

    color_log_level_mapping = {
        DEBUG: GREY,
        INFO: BLUE,
        WARNING: YELLOW,
        ERROR: RED,
        CRITICAL: BOLD_RED,
    }

    color_of_log = color_log_level_mapping[levelno]
    colored_message = color_of_log + msg + RESET
    return colored_message


class CustomFormatter(Formatter):
    def format(self, record: LogRecord):
        log_prefix = ""

        timestamp = self.formatTime(record, self.datefmt)

        log_prefix = log_prefix + f"[{PROJECT_NAME}]"
        log_prefix = log_prefix + " " + record.levelname
        log_prefix = log_prefix + " " + timestamp
        log_prefix = (
            log_prefix
            + " - "
            + f"{record.name}.{record.module}.{record.funcName}:{record.lineno}"
        )

        if LOG_REQUEST_ID and hasattr(record, "request_id") and record.request_id:
            log_prefix = log_prefix + " - " + f"[REQ-ID:{record.request_id}]"

        if (
            LOG_CORRELATION_ID
            and hasattr(record, "correlation_id")
            and record.correlation_id
        ):
            log_prefix = log_prefix + " - " + f"[CORR-ID:{record.correlation_id}]"

        record.msg = log_prefix + " " + str(record.msg)

        if ENABLE_COLOR_LOGS:
            record.msg = get_colored_message(record.msg, record.levelno)

        return super().format(record)
