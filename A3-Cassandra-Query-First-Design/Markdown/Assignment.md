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
The design decisions made in adapting the above schema for Cassandra from a traditional RDBMS context are deeply influenced by the need to achieve high performance and scalability, especially in distributed systems environments. Here's a justification of these design decisions, focusing on how they contribute to performance and scalability:

- **Denormalization and Redundancy**

    In traditional RDBMS systems, normalization is a core principle used to reduce redundancy and ensure data integrity. However, this often requires complex joins to reconstruct data for queries, which can become a performance bottleneck in distributed systems. Cassandra's emphasis on denormalization and redundancy is a strategic choice designed to minimize the need for joins, thereby significantly improving read performance. Storing data in the form it will be queried allows for fast, direct lookups without the overhead of assembling data from multiple tables.

- **Schema Design Based on Query Patterns**

    Cassandra requires a schema design that is closely aligned with query patterns. This design approach ensures that each query can be served efficiently by directly accessing a table optimized for that query, thus reducing the read and write latencies. By tailoring the data model to the application's access patterns, Cassandra can offer rapid responses to client requests, enhancing user experience and system throughput.

- **Primary Key and Data Distribution**

    The choice of partition key in Cassandra is critical as it determines how data is distributed across the cluster. A well-chosen partition key ensures uniform data distribution, avoiding hotspots and ensuring that no single node becomes a bottleneck. This uniform distribution is essential for scalability, as it ensures that the addition of nodes linearly increases the capacity of the system. Clustering columns, part of the primary key, allow for efficient sorting and retrieval within a partition, further optimizing access patterns.

- **Horizontal Scalability**

    Cassandra's data model and architecture are designed for horizontal scalability, meaning that it can handle increased load by adding more nodes to the cluster without significant reconfiguration. This scalability is achieved through data partitioning and replication, which allow the database to distribute loads evenly across the cluster and ensure data availability even in the face of node failures. This design is crucial for applications that require high availability and the ability to scale on demand.

- **Eventual Consistency Model**

    Cassandra adopts an eventual consistency model to maximize availability and partition tolerance, key components of the CAP theorem. This model allows Cassandra to continue operations even when some nodes are unreachable, ensuring that writes are not lost and can be replicated across the cluster once the affected nodes are back online. The ability to tune the consistency level for reads and writes allows developers to make trade-offs between consistency, availability, and latency based on the specific needs of their application.

- **Write and Read Throughput**

    Cassandra's write-optimized storage engine and the use of partition keys for data distribution lead to high write and read throughput. The architecture is designed to absorb high write loads by evenly distributing data across the cluster, thereby avoiding write bottlenecks. For reads, Cassandra's data model, which encourages storing data in the form it will be queried, enables efficient data retrieval without the need for resource-intensive operations like joins.

## Discussion
In this section, let's discuss on the challenges we faced during the translation process along with the considerations made and trade-offs in using Cansandra model.

### Challenges and Considerations - Akshay to add team's challenges in below points

- **Data Duplication:** Unlike RDBMS, where normalization is key to reducing data redundancy, Cassandra encourages denormalization for performance reasons. Managing data duplication across tables requires careful planning to ensure data consistency and integrity, which can be more complex to implement at the application level.
- **Query Flexibility:** RDBMS offers a high degree of query flexibility, including joins and sub-queries, allowing for complex queries against normalized data. Cassandra restricts query patterns to those explicitly modeled in the schema, requiring a thorough understanding of the application's query patterns upfront.
- **Transaction Support:** Cassandra provides limited support for ACID transactions, mainly through lightweight transactions that offer serial consistency but at a higher latency. Applications requiring complex transactions with strict ACID properties might find this limitation challenging.
- **Data Consistency:** The eventual consistency model of Cassandra, while beneficial for scalability and availability, requires applications to handle inconsistencies that might arise, unlike the strong consistency model typically provided by RDBMS.
- **Schema Evolution:** Modifying the schema in Cassandra, especially changing the primary key of existing tables, can be more cumbersome than in RDBMS. This requires planning ahead for future requirements to avoid complex migrations.

### Trade-offs - any more limitaion to add here ?

- **Scalability:** Cassandra shines in scenarios requiring horizontal scalability. It allows the YouTube application to handle massive volumes of data across many nodes efficiently, something that traditional RDBMS might struggle with at scale. This is a significant advantage for a global platform like YouTube, where data growth is continuous and exponential.
- **Availability:** Cassandra's distributed nature ensures high availability, with no single point of failure. This is crucial for a service like YouTube, where downtime directly impacts user experience and revenue.
- **Write Performance:** Cassandra offers excellent write performance across distributed architectures, making it suitable for write-heavy applications like YouTube, where new data (videos, comments, likes) are continuously being added.
- **Read Performance:** With a well-designed schema, Cassandra can also provide efficient read operations, particularly for use cases where data is read frequently but updated less often, such as video views or user profiles in YouTube.
- **Operational Complexity vs. Flexibility:** While Cassandra reduces some operational complexities related to scalability and availability, it introduces others, such as the need for careful data model planning and the management of data duplication. This trade-off requires a careful consideration of the application's specific needs and long-term maintenance capabilities.

## Conclusion

The project of translating a traditional RDBMS schema to a Cassandra schema for an application akin to YouTube offers profound insights into the intricacies of data modeling in NoSQL environments, specifically within the domain of high-scalability requirements. Here are the key learning outcomes and their potential real-world implications:

### Key Learning Outcomes

- **Data Modeling Around Queries:** One of the cardinal principles in using Cassandra effectively is the practice of modeling your data based on the queries you intend to run, rather than trying to fit your queries to a predetermined data model. This approach ensures that each query can be served with the utmost efficiency, directly impacting the application's responsiveness and user experience.
- **The Importance of Denormalization:** Embracing denormalization and understanding how to manage data duplication across tables are crucial. This strategy significantly differs from the normalization practices in RDBMS and is key to achieving high read and write performance in distributed systems like Cassandra.
- **Scalability and Performance:** The schema design decisions directly impact the application's ability to scale and perform under the pressures of big data. Cassandra's model facilitates linear scalability, allowing the YouTube application to grow seamlessly as demand increases.
- **Consistency vs. Availability:** The trade-offs between consistency and availability, as dictated by the CAP theorem, become starkly evident in this project. Cassandra's eventual consistency model, tuned for high availability and partition tolerance, requires a different approach to handling data integrity, especially in globally distributed applications.

### Real-world Implications

- **User Experience:** Fast read and write operations, facilitated by efficient schema design, ensure that users experience minimal latency when accessing videos, posting comments, or viewing recommendations. This responsiveness is crucial for user retention and engagement in competitive online spaces.
- **Operational Efficiency:** The ability to scale horizontally with ease means that the YouTube application can handle peak loads without significant rearchitecting or downtime for maintenance. This operational efficiency translates to cost savings and improved service reliability.
- **Data Integrity and Management:** While Cassandra's design optimizes for performance and scalability, it imposes an additional burden on application developers to manage data consistency across denormalized tables. This could require more sophisticated application logic or background processes to ensure data integrity, impacting development and operational overhead.
- **Global Reach:** The distributed nature of Cassandra's architecture makes it well-suited for applications requiring global reach. Data can be replicated across geographically dispersed data centers, reducing latency for users worldwide and enhancing the application's availability and disaster recovery capabilities.

### Influence on Performance and Scalability

- **Performance:** Direct access patterns designed into the schema mean that data can be retrieved with minimal overhead, supporting high-throughput and low-latency operations essential for a fluid user experience in a data-intensive application like YouTube.
- **Scalability:** The schema's design inherently supports distributed data storage, enabling the YouTube application to scale out across multiple servers and data centers. This capability is essential for accommodating the exponential growth in users and data volume, characteristic of successful online platforms.

