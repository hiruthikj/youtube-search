CREATE TABLE youtube_videos (
    id SERIAL PRIMARY KEY,
    video_id VARCHAR(255) NOT NULL,
    title TEXT NOT NULL,
    description TEXT NULL,
    published_at DATETIME NOT NULL,
    thumbnail_url VARCHAR(1023) NOT NULL,
    query_used TEXT NOT NULL
);


CREATE INDEX
IF NOT EXISTS
idx_youtube_videos_published_at
ON youtube_videos (published_at);

CREATE INDEX
IF NOT EXISTS
idx_youtube_videos_query_used
ON youtube_videos (query_used);
