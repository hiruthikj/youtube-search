-- Insert used by code
INSERT INTO youtube_videos (video_id, title, description, published_at, thumbnail_url, query_used)
VALUES (%(video_id)s, %(title)s, %(description)s, %(published_at)s, %(thumbnail_url)s, %(query_used)s)
ON CONFLICT (video_id) DO NOTHING
RETURNING youtube_videos.id
