from sqlalchemy import Column, DateTime, Index, Integer, String, Text

from .database import Base


class YoutubeVideoModel(Base):
    __tablename__ = "youtube_videos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    video_id = Column(String(255), nullable=False, unique=True)
    title = Column(Text, nullable=False)
    description = Column(Text)
    published_at = Column(DateTime, nullable=False)
    thumbnail_url = Column(String(1023), nullable=False)
    query_used = Column(Text, nullable=False)

    __table_args__ = (
        Index("idx_youtube_videos_video_id", video_id, unique=True),
        Index("idx_youtube_videos_published_at", published_at),
        Index("idx_youtube_videos_query_used", query_used),
    )
