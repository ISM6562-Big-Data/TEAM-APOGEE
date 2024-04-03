# SQL Queries for YouTube Database

#### This document presents a set of SQL queries tailored for analyzing data within a YouTube platform's database. Each query targets specific aspects of the platform's data to provide valuable insights. Here are the queries along with their descriptions:

1. **Most Active User**:
   This query retrieves the top 10 users who have uploaded the highest number of videos. It helps identify the most active contributors on the platform.
   ```sql
   SELECT user_id, COUNT(*) AS total_videos_uploaded
   FROM videos
   GROUP BY user_id
   ORDER BY total_videos_uploaded DESC
   LIMIT 10;


2. **Most Subscriptions**:
   This query identifies the top 10 users who have the highest number of subscribers. It helps in understanding which users have the largest audience and influence.
   
   ```sql
   SELECT subscribed_to_id, COUNT(*) AS total_subscribers
   FROM subscriptions
   GROUP BY subscribed_to_id
   ORDER BY total_subscribers DESC
   LIMIT 10;


3. **Find Videos with Specific Category**:
   This query fetches the titles of videos that belong to a specific category, such as "Television". It allows users to discover content based on their interests.
   
    ```sql
    SELECT v.title, c.category_name
    FROM videocategories vcJOIN videos v 
    ON vc.video_id = v.video_idJOIN categories c 
    ON vc.category_id = c.category_id
    WHERE c.category_name = 'Television';

   
4. **Videos with Highest Engagement**:
   This query calculates the engagement score for videos by combining the number of likes and comments they have received. It helps in identifying the most engaging videos on the platform.
   
   ```sql
   SELECT v.title, (COALESCE(l.likes_count, 0) + COALESCE(c.comments_count, 0)) AS engagement
   FROM videos v
   LEFT JOIN (
       SELECT video_id, COUNT(*) AS likes_count
       FROM videolikes
       GROUP BY video_id
   ) l ON v.video_id = l.video_id
    LEFT JOIN (
       SELECT video_id, COUNT(*) AS comments_count
       FROM comments
       GROUP BY video_id) c ON v.video_id = c.video_id
    ORDER BY engagement DESC
    LIMIT 10;


5. **Most Popular Categories based on Total Views**:
   This query ranks categories based on the total number of views their videos have received. It provides insights into the most popular content genres among viewers.
   
   ```sql
   SELECT c.category_name, SUM(v.views) AS total_views
   FROM categories c
   JOIN videocategories vc ON c.category_id = vc.category_id
   JOIN videos v ON vc.video_id = v.video_id
   GROUP BY c.category_name
   ORDER BY total_views DESC;


6. **Incrementing Video Views**:
   This query updates the view count of a specific video by incrementing it by one. It tracks the number of times a video has been viewed.
   
   ```sql
   UPDATE videos
   SET views = views + 1
   WHERE video_id = 'VYOjWN6yjS78206';


7. **Viewing Channel Subscriptions**:
   This query retrieves the details of users who are subscribed to a specific channel, identified by its user ID.      It helps channel owners to view their subscriber list.
   
  ```sql
SELECT u.*
FROM subscriptions s
JOIN users u ON s.subscribed_to_id = u.user_id
WHERE s.subscriber_id = 'UC_YO1yjS2';


#### These queries enable thorough analysis of the YouTube platform's data, facilitating data-driven decisions, audience engagement strategies, and content management.
