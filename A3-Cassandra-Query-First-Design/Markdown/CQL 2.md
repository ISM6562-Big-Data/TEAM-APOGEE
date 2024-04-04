In Cassandra, the schema design is heavily influenced by the query patterns and access patterns of the application.
 The "Query First" design philosophy suggests designing the schema based on the queries that will be performed against the data.

Considering the RDBMS schema, we will translate it into a Cassandra schema. 
In Cassandra, denormalization is key as it doesn't support joins. We'll need to optimize for fast reads and distribute data evenly across the cluster.

### Defining Application Queries
-- Let’s begin with the query-first approach to start designing the data model for our Youtube application. 
--We've adapt the approach for designing the data model of a YouTube application using a query-first approach. After brainstroming it with the team , we have identified key queries related to the Youtube application:

Q1. Search for videos related to the username.<br>
Q2. View comments on a specific video.<br>
Q3. View likes on a specific video.<br>
Q4. View channel subscriptions.<br>
Q5 view videos by category name<br>
Q6. Retrieve views of a video.<br>


### Below are the CQL queries and corresponding create table statements for each query:


## Q1. Search for videos related to the username.
The table youtube.videos_by_user has user_id as the partition key and video_id as the clustering key. 
This allows efficient retrieval of videos uploaded by a specific user. The primary key seems appropriate for the given query.

CREATE KEYSPACE youtube
    WITH replication = {'class': 'SimpleStrategy', 'replication_factor' : 3};

CREATE TABLE youtube.videos_by_user (
    user_id text,
    video_id uuid,
    title text,
    description text,
    upload_date timestamp,
    duration int,
    status text,
    PRIMARY KEY (user_id, video_id)
)WITH comment = 'Q1. Search for videos related to the username';

## Q2. View comments on a specific video.
Comments can be stored with the video ID as the partition key.
The table youtube.comments_by_video has video_id as the partition key and comment_id as the clustering key.
 This allows efficient retrieval of comments for a specific video. The primary key seems appropriate for the given query.


CREATE TABLE youtube.comments_by_video (
    video_id uuid,
    comment_id uuid,
    user_id uuid,
    comment_text text,
    comment_date timestamp,
    PRIMARY KEY (video_id, comment_id)
)WITH comment = 'Q2. View comments on a specific video';

## Q3. View likes on a specific video.
Likes can also be stored with the video ID as the partition key.
The table youtube.likes_by_video has video_id as the partition key and like_id as the clustering key.
 This allows efficient retrieval of likes for a specific video. The primary key seems appropriate for the given query.

CREATE TABLE youtube.likes_by_video (
    video_id uuid,
    like_id uuid,
    user_id uuid,
    like_date timestamp,
    PRIMARY KEY (video_id, like_id)
)WITH comment = 'Q3. View likes on a specific video';


## Q4. View channel subscriptions.
Subscriptions can be stored with the subscribers user ID as the partition key.
The table youtube.subscriptions_by_user has subscriber_id as the partition key and subscription_id as the clustering key.
 This allows efficient retrieval of subscriptions for a specific user. The primary key seems appropriate for the given query.

CREATE TABLE youtube.subscriptions_by_user (
    subscriber_id uuid,
    subscription_id uuid,
    subscribed_to_id uuid,
    subscription_date timestamp,
    PRIMARY KEY (subscriber_id, subscription_id)
)WITH comment = 'Q4. View channel subscriptions';

In Cassandra, denormalization is common to optimize for query patterns. These tables are designed to support the given queries efficiently. However, keep in mind that the actual implementation may vary depending on specific requirements and access patterns.

## Q5 view videos by category name
The table youtube.videos_by_category has category_id as the partition key and video_id as the clustering key. 
This allows efficient retrieval of videos belonging to a specific category. The primary key seems appropriate for the given query.
-- Table creation for viewing videos by category
CREATE TABLE youtube.videos_by_category (
    category_id uuid,
    video_id uuid,
    title text,
    description text,
    upload_date timestamp,
    duration int,  
    status text,
    PRIMARY KEY (category_id, video_id)
)WITH comment = 'Q5. view videos by category name';



## Q6  Retrieve views of a video.
CREATE TABLE videoviews (
    video_id UUID,
    user_id UUID,
    view_date TIMESTAMP,
    PRIMARY KEY (video_id, view_date)
)WITH comment = 'Q6. Retrieve views of a video.';

Partition key: video_id
Clustering columns: view_date



### highlighting how Cassandra's data model influences your schema design compared to traditional RDBMS designs

1. Denormalization
In RDMS, we use normalization to reduce redundancy and ensure data integrity.But in Cassandra, denormalization is key in Cassandra. Data is stored in multiple tables to optimize for reads. We've denormalized data to reduce the need for joins, which are not present in Cassandra.
2. Query-Driven Schema Design
In RDBMS, Schema design is the structure of the data and relationships between entities.But in Cassandra, The schema or table is designed on the business queries. Each table serves a specific query or set of queries.
3. Partitioning and Distribution
In RDBMS, Data is typically stored on a single server, but the distribution is not a primary concern during schema design.
But in Cassandra, Data distribution is crucial. Partition keys are chosen carefully to evenly distribute data across the cluster. Partition keys decides which node in the cluster stores the data. We've used UUIDs as primary keys for even distribution across nodes.
4. Use of Composite Keys and Clustering Columns:
In RDBMS, Primary keys are often simple and single-column.But in Cassandra, Primary keys can be composite keys including both partition keys and clustering columns. 



# Cassandra Schema Query Descriptions

### 1. Retrieve all videos uploaded by a specific user:

SELECT * FROM videos_by_user WHERE user_id = <user_id>;

**Description:**
- **Advantage in Cassandra:** This query is useful because in Cassandra, denormalization is common, and queries are designed to be efficient for specific access patterns. Storing videos by user allows for fast retrieval of all videos uploaded by a particular user without the need for joins.
- **Difference from RDBMS:** In traditional RDBMS, you might have a normalized schema where videos are stored in a separate table and linked to users through foreign key relationships. Joins would be required to retrieve all videos uploaded by a specific user, potentially leading to performance issues at scale.

### 2. Retrieve all comments on a specific video, sorted by date:
SELECT * FROM comments_by_video WHERE video_id = <video_id>;

**Description:**
- **Advantage in Cassandra:** Storing comments by video allows for efficient retrieval of comments related to a particular video. Sorting by date enables retrieving comments in chronological order, which can be important for displaying comments in applications.
- **Difference from RDBMS:** In RDBMS, comments might be stored in a separate table linked to videos through foreign keys. Join operations would be needed to retrieve comments for a specific video and sorting might require additional processing.

### 3. Retrieve all comments made by a specific user, sorted by date:
SELECT * FROM comments_by_user WHERE user_id = <user_id>;

**Description:**
- **Advantage in Cassandra:** Storing comments by user allows for efficient retrieval of comments made by a particular user. Sorting by date enables retrieving comments in chronological order, which can be useful for displaying a user's comment history.
- **Difference from RDBMS:** In RDBMS, comments might be stored in a separate table linked to users through foreign keys. Join operations would be needed to retrieve comments made by a specific user and sorting might require additional processing.

### 4. Retrieve all likes received by a specific video:
SELECT * FROM likes_by_video WHERE video_id = <video_id>;

**Description:**
- **Advantage in Cassandra:** Storing likes by video allows for efficient retrieval of likes received by a particular video. This schema design optimizes for read operations when displaying the popularity of a video.
- **Difference from RDBMS:** In RDBMS, likes might be stored in a separate table linked to videos through foreign keys. Join operations would be needed to retrieve likes received by a specific video.

### 5. Retrieve all likes given by a specific user:
SELECT * FROM likes_by_user WHERE user_id = <user_id>;

**Description:**
- **Advantage in Cassandra:** Storing likes by user allows for efficient retrieval of likes given by a particular user. This schema design optimizes for read operations when displaying a user's liked content.
- **Difference from RDBMS:** In RDBMS, likes might be stored in a separate table linked to users through foreign keys. Join operations would be needed to retrieve likes given by a specific user.

### 6. Retrieve all subscriptions made by a specific user:
SELECT * FROM subscriptions_by_user WHERE subscriber_id = <subscriber_id>;

**Description:**
- **Advantage in Cassandra:** Storing subscriptions by user allows for efficient retrieval of subscriptions made by a particular user. This schema design optimizes for read operations when displaying a user's subscriptions.
- **Difference from RDBMS:** In RDBMS, subscriptions might be stored in a separate table linked to users through foreign keys. Join operations would be needed to retrieve subscriptions made by a specific user.



