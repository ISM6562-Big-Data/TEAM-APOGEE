### RDBMS Schema Analysis

#### Tables:
1. **Users Table:**
   - Contains information about users such as user ID, username, email, password hash, join date, and last login date.
   - Primary key: user_id.
   
2. **Videos Table:**
   - Stores data related to videos uploaded by users including video ID, user ID of the uploader, title, description, upload date, duration, views, and status.
   - Primary key: video_id.
   - Foreign key: user_id references the Users Table.
   
3. **Comments Table:**
   - Holds comments made by users on specific videos, including comment ID, user ID of the commenter, video ID of the commented video, comment text, and comment date.
   - Primary key: comment_id.
   - Foreign keys: user_id and video_id reference the Users and Videos Tables respectively.
   
4. **VideoLikes Table:**
   - Records likes given by users to videos, with like ID, user ID of the liker, and video ID of the liked video.
   - Primary key: like_id.
   - Foreign keys: user_id and video_id reference the Users and Videos Tables respectively.
   
5. **Subscriptions Table:**
   - Tracks user subscriptions to other users, with subscription ID, subscriber ID, subscribed-to ID, and subscription date.
   - Primary key: subscription_id.
   - Foreign keys: subscriber_id and subscribed_to_id reference the Users Table.
   
6. **Categories Table:**
   - Stores video categories with category ID and category name.
   - Primary key: category_id.
   - Unique constraint: category_name.
   
7. **VideoCategories Table:**
   - Represents a many-to-many relationship between videos and categories, linking video IDs with category IDs.
   - Composite primary key: (video_id, category_id).
   - Foreign keys: video_id references the Videos Table, category_id references the Categories Table.
   
8. **VideoViews Table:**
   - Records views on videos, with view ID, user ID of the viewer (nullable for non-logged-in users), and video ID of the viewed video.
   - Primary key: view_id.
   - Foreign keys: user_id and video_id reference the Users and Videos Tables respectively.

#### Relationships:
- Users can upload videos (one-to-many relationship between Users and Videos).
- Users can leave comments on videos (one-to-many relationship between Users and Comments, and Videos and Comments).
- Users can like videos (one-to-many relationship between Users and VideoLikes, and Videos and VideoLikes).
- Users can subscribe to other users (one-to-many relationship between Users and Subscriptions).
- Videos can belong to multiple categories, and categories can have multiple videos (many-to-many relationship between Videos and Categories via the VideoCategories Table).
- Users can view videos (one-to-many relationship between Users and VideoViews, and Videos and VideoViews).

#### Assumptions:
- The view_id in the VideoViews Table is assumed to be unique to track individual views.
- The user_id in the VideoViews Table can be NULL to accommodate views from non-logged-in users.
- The subscription_date in the Subscriptions Table represents the date when the subscription was made.
- The comment_date in the Comments Table represents the date and time when the comment was posted.
- The last_login in the Users Table represents the date and time of the user's last login activity.
- The upload_date in the Videos Table and the comment_date in the Comments Table are timestamps with time zone data types to accurately record the time of events regardless of the user's location.

