CREATE TABLE users (
    user_id uuid PRIMARY KEY,
    username text,
    email text,
    password_hash text,
    join_date timestamp,
    last_login timestamp
);

CREATE TABLE videos_by_user (
    user_id uuid,
    video_id uuid,
    title text,
    description text,
    upload_date timestamp,
    duration int,
    views int,
    status text,
    PRIMARY KEY (user_id, video_id)
) WITH CLUSTERING ORDER BY (upload_date DESC);

CREATE TABLE comments_by_video (
    video_id uuid,
    comment_id uuid,
    user_id uuid,
    comment_text text,
    comment_date timestamp,
    PRIMARY KEY (video_id, comment_id)
) WITH CLUSTERING ORDER BY (comment_date DESC);

CREATE TABLE comments_by_user (
    user_id uuid,
    comment_id uuid,
    video_id uuid,
    comment_text text,
    comment_date timestamp,
    PRIMARY KEY (user_id, comment_date)
) WITH CLUSTERING ORDER BY (comment_date DESC);

CREATE TABLE likes_by_video (
    video_id uuid,
    user_id uuid,
    like_date timestamp,
    PRIMARY KEY (video_id, user_id)
);

CREATE TABLE likes_by_user (
    user_id uuid,
    video_id uuid,
    like_date timestamp,
    PRIMARY KEY (user_id, video_id)
);
CREATE TABLE subscriptions_by_user (
    subscriber_id uuid,
    subscribed_to_id uuid,
    subscription_date timestamp,
    PRIMARY KEY (subscriber_id, subscribed_to_id)
);

CREATE TABLE video_views_by_video (
    video_id uuid,
    view_id uuid,
    user_id uuid,
    view_date timestamp,
    PRIMARY KEY (video_id, view_date, user_id)
) WITH CLUSTERING ORDER BY (view_date DESC);