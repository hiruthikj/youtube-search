"""Contains constants and enums"""
from enum import Enum


class RequestStatus(str, Enum):
    """API request status"""

    SUCCESS = "success"
    FAIL = "fail"


class ContextVariables(str, Enum):
    CORRELATION_ID_CTX_KEY = "correlation_id"
    REQUEST_ID_CTX_KEY = "request_id"
