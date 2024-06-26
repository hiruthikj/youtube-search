import logging
from ast import Dict
from datetime import datetime, timezone

import requests
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from ..config import settings
from ..db.database import SessionLocal
from ..db.models import YoutubeVideoModel
from ..db.schemas import YoutubeVideo


async def create_youtube_video_record(db: Session, youtube_video: YoutubeVideo):
    db_video_dict = {
        "video_id": youtube_video.video_id,
        "title": youtube_video.title,
        "description": youtube_video.description,
        "published_at": youtube_video.published_at,
        "thumbnail_url": youtube_video.thumbnail_url,
        "query_used": youtube_video.query_used,
    }

    stmt = (
        insert(YoutubeVideoModel)
        .values(db_video_dict)
        # Does nothing when we try to add already existing video
        .on_conflict_do_nothing(index_elements=[YoutubeVideoModel.video_id])
    )

    db.execute(stmt)
    db.commit()
    return db_video_dict


async def fetch_from_yt() -> Dict:
    search_query = "ipl"
    max_results = 10
    published_after = (
        datetime.now(tz=timezone.utc).replace(tzinfo=None).isoformat() + "Z"
    )

    query_params = {
        "part": "snippet",
        "maxResults": max_results,
        "order": "date",
        "publishedAfter": published_after,
        "q": search_query,
        "key": settings.GOOGLE_DEVELOPER_KEY,
    }

    try:
        # settings.DEBUG and logging.debug(
        # f"Youtube API input: url={settings.YOUTUBE_API_ENDPOINT},query={query_params}")
        response = requests.get(url=settings.YOUTUBE_API_ENDPOINT, params=query_params)

        logging.debug(
            f"Response from Youtube API: status={response.status_code}, json={response.json()}"
        )
        response.raise_for_status()

    except requests.exceptions.RequestException as err:
        print("Request Error:", err)
        raise err

    result = response.json()
    for item in result["items"]:
        youtube_video = YoutubeVideo(
            title=item["snippet"]["title"],
            description=item["snippet"]["description"],
            published_at=item["snippet"]["publishedAt"],
            thumbnail_url=item["snippet"]["thumbnails"]["default"]["url"],
            video_id=item["id"]["videoId"],
            query_used=search_query,
        )

        await create_youtube_video_record(
            db=SessionLocal(), youtube_video=youtube_video
        )
        logging.info(f"Added video_id={youtube_video.video_id} to DB")

    return result
