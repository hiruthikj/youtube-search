import logging

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import PositiveInt
from sqlalchemy.orm import Session

from ..common.constants import RequestStatus
from ..config import settings
from ..db import models
from ..db.database import get_db
from ..extenstions.logging_router import LoggingRoute

search_router = APIRouter(prefix=settings.API_V1_STR, route_class=LoggingRoute)


@search_router.get("/search")
async def search_video(
    q: str, page: PositiveInt, size: PositiveInt = 10, db: Session = Depends(get_db)
):
    try:
        offset = (page - 1) * size
        limit = size
        results = (
            db.query(models.YoutubeVideoModel)
            .filter(
                models.YoutubeVideoModel.title.icontains(q),
                models.YoutubeVideoModel.description.icontains(q),
            )
            .order_by(models.YoutubeVideoModel.published_at.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )

        response = {
            "status": RequestStatus.SUCCESS,
            "data": {
                "videos": results,
                "current_page": page,
                "page_size": size,
                # "total_count": ""
            },
        }
        return JSONResponse(
            content=jsonable_encoder(response),
            status_code=status.HTTP_201_CREATED,
        )

    except Exception:
        logging.exception(
            "search_video Failed",
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )
