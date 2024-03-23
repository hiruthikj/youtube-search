from datetime import datetime

from pydantic import BaseModel


class YoutubeVideo(BaseModel):
    video_id: str
    title: str
    description: str = None
    published_at: datetime
    thumbnail_url: str
    query_used: str

    class Config:
        from_attributes = True
