# YouTube Database Queries

## 1. Retrieving user information:

### Fetch user profile by user_id:
```sql
SELECT * FROM users WHERE user_id = 'UC_YO8yjS9';
```
- This query retrieves the user profile by their unique user ID.

### Fetch user profile by username:
```sql
SELECT * FROM users WHERE username = 'austin38';
```
- This query retrieves the user profile by their username.

### Fetch user profile by email:
```sql
SELECT * FROM users WHERE email = 'emckenzie@example.org';
```
- This query retrieves the user profile by their email address.

### Logging in (lookup by username or email):
```sql
SELECT * FROM users WHERE username = 'austin38' AND password_hash = '77b43822c318be1c618c2c047e80731be5adc190b949f81026d821165da72504';
-- OR
SELECT * FROM users WHERE email = 'emckenzie@example.org' AND password_hash = '77b43822c318be1c618c2c047e80731be5adc190b949f81026d821165da72504';
```
- These queries are used for user login, verifying the username or email and password combination.

### Updating user details:
```sql
UPDATE users SET username = 'austin38', email = 'emckenzie@example.org' WHERE user_id = 'UC_YO8yjS9';
```
- This query updates the username and email of a specific user identified by their user_id.


## 2. Listing videos uploaded by a specific user:

```sql
SELECT * FROM videos WHERE user_id = 'UC_YO17yjS18';
```
- This query lists all the videos uploaded by a specific user identified by their user_id.

## 3. Incrementing video views:

```sql
UPDATE videos SET views = views + 1 WHERE video_id = 'VYOjWN14yjS1516214';
```
- This query increments the view count of a specific video identified by its video_id.

## 4. Fetching comments for a specific video:

```sql
SELECT * FROM comments WHERE video_id = 'VYOjWN15yjS1617215';
```
- This query retrieves all the comments made on a specific video identified by its video_id.

## 5. Retrieving comments made by a specific user:

```sql
SELECT * FROM comments WHERE user_id = 'UC_YO13yjS14';
```
- This query retrieves all the comments made by a specific user identified by their user_id.

## 6. Listing users who liked a specific video:

```sql
SELECT u.* 
FROM users u
JOIN videolikes vl ON u.user_id = vl.user_id
WHERE vl.video_id = 'VYOjWN12yjS1314212';
```
- This query lists all the users who liked a specific video identified by its video_id.

## 7. Tracking videos liked by a user:

```sql
SELECT v.* 
FROM videos v
JOIN videolikes vl ON v.video_id = vl.video_id
WHERE vl.user_id = 'UC_YO11yjS12';
```
- This query tracks all the videos liked by a specific user identified by their user_id.

## 8. Viewing channel subscriptions:

### For subscriptions made by a user:

```sql
SELECT s.*, u.username AS subscriber_username, u2.username AS subscribed_to_username
FROM subscriptions s
JOIN users u ON s.subscriber_id = u.user_id
JOIN users u2 ON s.subscribed_to_id = u2.user_id
WHERE s.subscriber_id = 'UC_YO1yjS2';
```
- This query retrieves all the subscriptions made by a specific user identified by their user_id.

### For subscriptions to a channel:

```sql
SELECT s.*, u.username AS subscriber_username, u2.username AS subscribed_to_username
FROM subscriptions s
JOIN users u ON s.subscriber_id = u.user_id
JOIN users u2 ON s.subscribed_to_id = u2.user_id
WHERE s.subscribed_to_id = 'UC_YO1yjS2';
```
- This query retrieves all the subscriptions to a specific channel identified by the channel's user_id.
