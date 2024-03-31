-- Users Table
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    join_date TIMESTAMP WITH TIME ZONE NOT NULL,
    last_login TIMESTAMP WITH TIME ZONE
);

-- Videos Table
CREATE TABLE videos (
    video_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    upload_date TIMESTAMP WITH TIME ZONE NOT NULL,
    duration INT NOT NULL, -- assuming duration in seconds
    views INT DEFAULT 0,
    status VARCHAR(50),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Comments Table
CREATE TABLE comments (
    comment_id SERIAL PRIMARY KEY,
    video_id INT NOT NULL,
    user_id INT NOT NULL,
    comment_text TEXT NOT NULL,
    comment_date TIMESTAMP WITH TIME ZONE NOT NULL,
    FOREIGN KEY (video_id) REFERENCES videos(video_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- VideoLikes Table
CREATE TABLE videolikes (
    like_id SERIAL PRIMARY KEY,
    video_id INT NOT NULL,
    user_id INT NOT NULL,
    like_date TIMESTAMP WITH TIME ZONE NOT NULL,
    FOREIGN KEY (video_id) REFERENCES videos(video_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Subscriptions Table
CREATE TABLE subscriptions (
    subscription_id SERIAL PRIMARY KEY,
    subscriber_id INT NOT NULL,
    subscribed_to_id INT NOT NULL,
    subscription_date TIMESTAMP WITH TIME ZONE NOT NULL,
    FOREIGN KEY (subscriber_id) REFERENCES users(user_id),
    FOREIGN KEY (subscribed_to_id) REFERENCES users(user_id)
);

-- Categories Table
CREATE TABLE categories (
    category_id SERIAL PRIMARY KEY,
    category_name TEXT NOT NULL UNIQUE
);

-- VideoCategories Table (Many-to-Many relationship between Videos and Categories)
CREATE TABLE videocategories (
    video_id INT NOT NULL,
    category_id INT NOT NULL,
    PRIMARY KEY (video_id, category_id),
    FOREIGN KEY (video_id) REFERENCES videos(video_id),
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
);

-- VideoViews Table (For detailed analytics on views)
CREATE TABLE videoviews (
    view_id SERIAL PRIMARY KEY,
    video_id INT NOT NULL,
    user_id INT, -- This can be NULL to track views from non-logged in users
    view_date TIMESTAMP WITH TIME ZONE NOT NULL,
    FOREIGN KEY (video_id) REFERENCES videos(video_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
