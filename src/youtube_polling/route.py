from fastapi import APIRouter

from .config import settings
from .extenstions.logging_router import LoggingRoute

search_router = APIRouter(prefix=settings.API_V1_STR, route_class=LoggingRoute)
