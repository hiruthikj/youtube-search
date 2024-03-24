CREATE TABLE
IF NOT EXISTS
youtube_videos (
    id SERIAL PRIMARY KEY,
    video_id VARCHAR(255) UNIQUE NOT NULL,
    title TEXT NOT NULL,
    description TEXT NULL,
    published_at TIMESTAMP NOT NULL,
    thumbnail_url VARCHAR(1023) NOT NULL,
    query_used TEXT NOT NULL
);


CREATE UNIQUE INDEX
IF NOT EXISTS
idx_youtube_videos_video_id
ON youtube_videos (video_id);

CREATE INDEX
IF NOT EXISTS
idx_youtube_videos_published_at
ON youtube_videos (published_at);

CREATE INDEX
IF NOT EXISTS
idx_youtube_videos_query_used
ON youtube_videos (query_used);
