import logging
from logging.config import dictConfig

from .log_format import CustomFormatter
from .middleware import get_correlation_id, get_request_id


class RequestIdFilter(logging.Filter):
    def filter(self, record):
        record.request_id = get_request_id()
        return True


class CorrelationIdFilter(logging.Filter):
    def filter(self, record):
        record.correlation_id = get_correlation_id()
        return True


# TODO: Better logging, correlation id logging, structured logging
def setup_logging(debug: bool):
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "filters": {
            "request_id": {
                "()": RequestIdFilter,
            },
            "correlation_id": {
                "()": CorrelationIdFilter,
            },
        },
        "formatters": {
            # 'standard': {
            #     'format': '%(asctime)s REQ-ID:%(request_id)s %(levelname)s %(name)s %(message)s'
            # },
            "standard": {
                "()": CustomFormatter,
                "format": "%(message)s",
            },
        },
        "handlers": {
            "error_stream": {
                "level": "ERROR",
                "class": "logging.StreamHandler",
                "formatter": "standard",
                "stream": "ext://sys.stderr",
                "filters": ["request_id", "correlation_id"],
            },
            "info_stream": {
                "level": "DEBUG" if debug else "INFO",
                "class": "logging.StreamHandler",
                "formatter": "standard",
                "stream": "ext://sys.stdout",
                "filters": ["request_id", "correlation_id"],
            },
        },
        "root": {
            "level": "NOTSET",
            "handlers": ["error_stream", "info_stream"],
        },
    }

    dictConfig(logging_config)
