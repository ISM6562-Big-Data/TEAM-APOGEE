# Translating RDBMS Schema to Cassandra for YouTube Application

## Introduction

This project focuses on the translation of Relational Database Management System (RDBMS) schemas into Apache Cassandra schemas, specifically tailored for big data applications using YouTube as a case study. The aim is to harness Cassandra's capabilities for fast reads and writes, as well as horizontal scalability, to address the demands of handling large volumes of data. This report outlines the project's scope, objectives, and the significance of this translation in the context of big data applications.

## Scope and Objectives
- Highlight the differences in schema design between Cassandra and traditional RDBMS, focusing on Cassandra's data model
- Demonstrate Cassandra's design principle of modeling your data based on how you will query it, rather than trying to minimize data duplication as you would in a traditional relational database. 
- Design tables to ensure efficient data retrieval that aligns with Cassandra’s strengths in handling large-scale, distributed data. - By duplicating data across tables where necessary, we prioritize query performance and scalability, key advantages of using Cassandra for applications with heavy read and write requirements.
- 

## Analyze the RDBMS Schema

### Overview

The RDBMS schema designed for the YouTube application is detailed below, highlighting its key components, relationships, and assumptions made about the data and its usage. The schema is normalized to ensure data integrity and reduce redundancy.

### Components and Relationships

- **Tables:** Describe each table included in the YouTube RDBMS schema, including columns, primary keys, and any foreign keys.
- **Relationships:** Discuss the relationships between tables, including one-to-many or many-to-many relationships.
- **Assumptions:** Note any assumptions about the data or its usage that influenced the schema design.

## Query Analysis

This section lists and analyzes the essential queries for the YouTube application's functionality. The analysis guides the translation of the RDBMS schema into a Cassandra schema, focusing on optimizing these queries.

### Essential Queries

- List the queries considered essential for the application. -  (We will get these queries from Saloni and put it here with some description.)
- Discuss how these queries influence the design of the Cassandra schema. - Check raw data folder

## Design Cassandra Schema

Adopting the "Query First" design philosophy, this section documents the process of translating the YouTube RDBMS schema into a Cassandra schema.

### Design Process

#### Query Optimization:
The Cassandra schema we've discussed is meticulously designed to align with the specific query requirements of our application. Let's dive into how each table in the Cassandra schema serves the essential queries identified earlier, reflecting the principle of designing around query patterns in Cassandra:

#### 1. Retrieving User Information

For operations like fetching user profiles and logging in (which may require looking up by username or email), we have proposed creating tables `users_by_username` and `users_by_email`. This design decision ensures direct and efficient access to user information using either a username or an email, which is crucial for login operations. This approach exemplifies Cassandra's design philosophy where data duplication across tables is acceptable to ensure query efficiency.

#### 2. Listing Videos Uploaded by a Specific User

The `videos_by_user` table is designed with `user_id` as the partition key and `video_id` as a clustering key. This arrangement enables the efficient retrieval of all videos uploaded by a specific user. The clustering order could further be defined to sort these videos by upload date or other relevant criteria, thus directly supporting the listing videos query.

#### 3. Incrementing Video Views

The video views are updated through the `videos_by_user` table, leveraging the video's `video_id`. By structuring the table to allow easy access via `user_id` and `video_id`, the schema supports efficient updates to the views count for any given video, reflecting the requirement for an efficient update operation for incrementing video views.

#### 4. Fetching Comments for a Specific Video

The `comments_by_video` table, with `video_id` as the partition key, is optimized for fetching all comments associated with a specific video. This design choice ensures that comments are easily and efficiently retrievable by video, supporting the query pattern for fetching video comments.

#### 5. Retrieving Comments Made by a Specific User

Similarly, the `comments_by_user` table uses `user_id` as the partition key, facilitating the efficient retrieval of all comments made by a specific user. This table structure is tailored to the query pattern for fetching a user's comments across videos.

#### 6. Listing Users Who Liked a Specific Video

The `likes_by_video` table is designed with `video_id` as the partition key. This table structure supports the direct and efficient retrieval of all users who have liked a particular video, directly catering to the query requirement for listing users who liked a video.

#### 7. Tracking Videos Liked by a User

For tracking which videos a user has liked, the `likes_by_user` table, with `user_id` as the partition key, enables the application to efficiently list all videos liked by a specific user. This design is an example of tailoring your data model to support specific read patterns, in this case, tracking likes by a user.

#### 8. Viewing Channel Subscriptions

The `subscriptions_by_user` table uses `subscriber_id` as the partition key, enabling efficient queries to view all channels a user is subscribed to. This table design is optimized for the subscription viewing pattern, ensuring that subscription information is easily accessible by subscriber ID.

#### Data Model Influences:Highlight the differences in schema design between Cassandra and traditional RDBMS, focusing on Cassandra's data model.  - Check raw data folder

### Final Cassandra Schema

- **Table Designs:** Present the final Cassandra table designs, including partition keys, clustering columns, and any secondary indexes.-  Akshay will add snapshots of Cassandra DB

#### Design Decisions:
The design decisions made in adapting a schema for Cassandra from a traditional RDBMS context are deeply influenced by the need to achieve high performance and scalability, especially in distributed systems environments. Here's a justification of these design decisions, focusing on how they contribute to performance and scalability:

- **Denormalization and Redundancy**

    In traditional RDBMS systems, normalization is a core principle used to reduce redundancy and ensure data integrity. However, this often requires complex joins to reconstruct data for queries, which can become a performance bottleneck in distributed systems. Cassandra's emphasis on denormalization and redundancy is a strategic choice designed to minimize the need for joins, thereby significantly improving read performance. Storing data in the form it will be queried allows for fast, direct lookups without the overhead of assembling data from multiple tables.

### Schema Design Based on Query Patterns

**Justification:** Cassandra requires a schema design that is closely aligned with query patterns. This design approach ensures that each query can be served efficiently by directly accessing a table optimized for that query, thus reducing the read and write latencies. By tailoring the data model to the application's access patterns, Cassandra can offer rapid responses to client requests, enhancing user experience and system throughput.

### Primary Key and Data Distribution

**Justification:** The choice of partition key in Cassandra is critical as it determines how data is distributed across the cluster. A well-chosen partition key ensures uniform data distribution, avoiding hotspots and ensuring that no single node becomes a bottleneck. This uniform distribution is essential for scalability, as it ensures that the addition of nodes linearly increases the capacity of the system. Clustering columns, part of the primary key, allow for efficient sorting and retrieval within a partition, further optimizing access patterns.

### Horizontal Scalability

**Justification:** Cassandra's data model and architecture are designed for horizontal scalability, meaning that it can handle increased load by adding more nodes to the cluster without significant reconfiguration. This scalability is achieved through data partitioning and replication, which allow the database to distribute loads evenly across the cluster and ensure data availability even in the face of node failures. This design is crucial for applications that require high availability and the ability to scale on demand.

### Eventual Consistency Model

**Justification:** Cassandra adopts an eventual consistency model to maximize availability and partition tolerance, key components of the CAP theorem. This model allows Cassandra to continue operations even when some nodes are unreachable, ensuring that writes are not lost and can be replicated across the cluster once the affected nodes are back online. The ability to tune the consistency level for reads and writes allows developers to make trade-offs between consistency, availability, and latency based on the specific needs of their application.

### Write and Read Throughput

**Justification:** Cassandra's write-optimized storage engine and the use of partition keys for data distribution lead to high write and read throughput. The architecture is designed to absorb high write loads by evenly distributing data across the cluster, thereby avoiding write bottlenecks. For reads, Cassandra's data model, which encourages storing data in the form it will be queried, enables efficient data retrieval without the need for resource-intensive operations like joins.

## Discussion

Reflect on the challenges and considerations encountered during the schema translation process. Discuss the trade-offs of using Cassandra over traditional RDBMS for the YouTube application.

### Challenges and Considerations - Check raw data folder for both below challengeConsideration.md 

- Describe the challenges faced during the translation process.
- Discuss any considerations that had to be made due to Cassandra's data model and architecture.

### Trade-offs -Check raw data folder challengeConsideration.md 

- Analyze the trade-offs of using Cassandra instead of a traditional RDBMS, considering the application's requirements.

## Conclusion - check raw data conclusion.md

Summarize the key learning outcomes from this project and discuss the potential real-world implications of the schema design decisions made for the YouTube application. Highlight how these decisions could influence the application's performance and scalability in a big data context.

