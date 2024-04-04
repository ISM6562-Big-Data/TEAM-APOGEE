Cassandra is designed for scalability and high availability without compromising performance. This means designing our schema based on the query patterns rather than structuring data into normalized tables. Here's we can model your PostgreSQL schema for Cassandra, focusing on the mentioned use cases (Queries) above.

### 1. Users Table

For user operations like fetching profiles, logging in, and updating details, we can keep a structure similar to the relational `users` table, but with Cassandra's data type adjustments.

```cql
CREATE TABLE users (
    user_id uuid PRIMARY KEY,
    username text,
    email text,
    password_hash text,
    join_date timestamp,
    last_login timestamp
);
```

### 2. Videos by User

To list videos uploaded by a user, creating a table that partitions videos by user_id. This table allows efficient retrieval of videos for a given user.

```cql
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
```

### 3. Comments for a Video

To fetch comments for a specific video, model comments around video_id.

```cql
CREATE TABLE comments_by_video (
    video_id uuid,
    comment_id uuid,
    user_id uuid,
    comment_text text,
    comment_date timestamp,
    PRIMARY KEY (video_id, comment_id)
) WITH CLUSTERING ORDER BY (comment_date DESC);
```

### 4. Comments by a User

Similarly, for retrieving comments made by a user:

```cql
CREATE TABLE comments_by_user (
    user_id uuid,
    comment_id uuid,
    video_id uuid,
    comment_text text,
    comment_date timestamp,
    PRIMARY KEY (user_id, comment_date)
) WITH CLUSTERING ORDER BY (comment_date DESC);
```

### 5. Users who Liked a Video

To list users who liked a video, you can create a table based on `video_id`.

```cql
CREATE TABLE likes_by_video (
    video_id uuid,
    user_id uuid,
    like_date timestamp,
    PRIMARY KEY (video_id, user_id)
);
```

### 6. Videos Liked by a User

Track which videos a user has liked:

```cql
CREATE TABLE likes_by_user (
    user_id uuid,
    video_id uuid,
    like_date timestamp,
    PRIMARY KEY (user_id, video_id)
);
```

### 7. Viewing Channel Subscriptions

Subscriptions can be modeled to easily retrieve who a user is subscribed to.

```cql
CREATE TABLE subscriptions_by_user (
    subscriber_id uuid,
    subscribed_to_id uuid,
    subscription_date timestamp,
    PRIMARY KEY (subscriber_id, subscribed_to_id)
);
```

### 8. Tracking Video Views by Video
Below design would typically focus on the video_id as the partition key to facilitate efficient retrieval of views per video. 

```cql
CREATE TABLE video_views_by_video (
    video_id uuid,
    view_id uuid,
    user_id uuid,
    view_date timestamp,
    PRIMARY KEY (video_id, view_date, user_id)
) WITH CLUSTERING ORDER BY (view_date DESC);
```

### Considerations

- Each use case is backed by a specific table designed to satisfy the query efficiently.
- Redundancy is expected and normal in NoSQL databases like Cassandra to facilitate fast reads.
