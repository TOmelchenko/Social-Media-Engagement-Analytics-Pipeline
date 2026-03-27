CREATE DATABASE social_media;

CREATE TABLE IF NOT EXISTS final_report(
    creator_user_id TEXT,
    username TEXT,
    creator_total_engagement INTEGER
);

SELECT COUNT(1) FROM final_report;

SELECT * FROM final_report;