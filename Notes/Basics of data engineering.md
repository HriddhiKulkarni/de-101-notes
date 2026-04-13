**What is Data Engineering?**<br/>
The process of collecting, maintaining, and transforming raw data into a usable format for use by data scientists, data analysts, etc., This process also involves building pipelines and creating systems around it.

**What is ETL?**<br/>
ETL(Extract, Transform, and Load). Extract involves extracting/reading the data, then transforming/processing it into clean usable format and finally loading it for use by data scientists/analysts/business users etc., for analytics purposes.

**What is ELT?**<br/>
ELT (Extract, Load, and Transform). This is a modern approach to ETL, here the data is dumped or "loaded" then "transform" step happens at the very end. 

**ETL vs. ELT. When to use what process?**

| Feature |	ETL (Extract, Transform, Load)|	ELT (Extract, Load, Transform) |
|:--:|:--:|:--:|
| Order |	Transform occurs before loading. | Transform occurs after loading. |
| Location | Separate staging/processing server. | Directly inside the target warehouse/lake. |
| Data Types | Primarily structured data.	| Structured, unstructured, and semi-structured. |
| Load Speed | Slower (bottlenecked by transformation).	| Faster (immediate raw data ingestion). |
| Flexibility	| Schema-on-write: Fixed and rigid.	| Schema-on-read: Flexible, "sandbox" style. |
| Security | PII can be masked before storage. | Raw data is stored; requires post-load governance. |
| Maintenance | High (separate servers and complex pipelines). | Lower (simpler stack, leverages cloud power). |
| Best For|	On-prem systems, small datasets, strict compliance.	| Big data, cloud-native stacks, AI/ML models. |
| Privacy | Pre-load transformation can eliminate PII (helps for HIPPA). | Direct loading of data requires more privacy safeguards. |
| Maintenance | Secondary processing server adds to the maintenance burden. | With fewer systems, the maintenance burden is reduced. |
| Costs | Separate servers can create cost issues. | Simplified data stack costs less. |
| Requeries | Data is transformed before entering destination system; therefore raw data cannot be requeried. | Raw data is loaded directly into destination system and can be requeried endlessly. |
| Data Lake Compatibility | No, ETL does not have data lake compatibility. | Yes, ELT does have data lake compatibility. |

**Data ingestion patterns:** <br/> 
Batch ingestion: <br/>
The process of capturing and loading high-volume data in collected groups at scheduled intervals. <br/>
 <br/>
 Streaming ingestion:  <br/>
The process of capturing and loading data as events occur, i.e., continuously in near real time. <br/>
 <br/>
Change Data Capture (CDC):  <br/>
The process that identifies and tracks only the specific data that has changed—such as inserts, updates, or deletes—in a source database. It then automatically moves those "deltas" to a target system in near real-time, keeping everything in sync without needing to reload entire datasets.<br/>
 <br/>
Hybrid ingestion:  <br/>
This process is a flexible architecture that combines Batch, Streaming, and CDC to handle different data speeds and volumes in one system. It is typically implemented using one of these two patterns:<br/>
Lambda Architecture: Runs two parallel tracks — a Batch Layer for processing massive historical data with 100% accuracy, and a Speed Layer (using Streaming or CDC) to provide immediate, real-time insights.  <br/>
Micro-batching: A middle-ground approach where streaming data is processed in tiny groups every few seconds (like in Apache Spark Streaming) to balance the simplicity of batch with the speed of streaming.

| Pattern | Definition | Timing | Best For | Real-World Example |
| :--- | :--- | :--- | :--- | :--- |
| **Batch** | Processing large groups of data collected over a period. | Scheduled (e.g., Every 24 hrs) | High-volume, non-urgent reporting. | **Payroll:** Calculating and sending employee direct deposits once a month. |
| **Streaming** | Processing individual data points immediately as they are created. | Continuous (Millisecond latency) | High-velocity, mission-critical alerts. | **Fraud Detection:** Blocking a credit card transaction the second it happens. |
| **CDC** | Capturing only the "deltas" (changes) from a source database. | Near Real-Time (Seconds) | Database syncing without heavy reloads. | **Inventory Sync:** Updating a website's "In Stock" count as soon as a sale is made. |
| **Lambda** | A hybrid architecture that processes data through two parallel paths: a fast "Speed Layer" and an accurate "Batch Layer." | Simultaneous (Real-time + Scheduled) | Balancing immediate insights with 100% data accuracy. | **Ride-Sharing:** Using a speed layer for live surge pricing while a batch layer calculates official driver payouts overnight. |
| **Micro-batching** | Processing small groups of data at very short intervals. | Frequent (e.g., Every 10–60 seconds) | Balancing batch simplicity with near-real-time speed. | **Log Analysis:** Monitoring website traffic spikes in 1-minute chunks. |

**Architectures:**

| Method | Definition | Timing | Best For | Real-World Example | Storage / Platform | Processing Engine | Ingestion / CDC Tool |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Batch-First** | Traditional ETL where data is collected and moved in bulk. | Scheduled (e.g., Nightly) | Simple, non-urgent reports and deep historical audits. | **Banking:** Calculating monthly interest for all savings accounts at the end of the month. | Snowflake, BigQuery, S3 | Apache Spark, AWS Glue | Fivetran, Airbyte, dbt |
| **Lambda (Hybrid)** | Maintains two parallel paths: a "Batch Layer" for accuracy and a "Speed Layer" for real-time views. | Real-time + Scheduled | When you need sub-second alerts but legally require 100% accurate daily audits. | **Retail:** Showing **live stock alerts** while running **nightly inventory reconciliation**. | Azure Data Lake, Hadoop | Spark Streaming, Apache Flink | Apache Kafka, Debezium |
| **Kappa (Stream-First)** | Replaces the batch layer entirely; uses a single stream engine for both live and historical data. | Continuous / Replay | Reducing code complexity and operational overhead. | **Streaming Services:** Replaying days of user "play" events to update recommendation models after a code change. | Confluent Cloud, Redpanda | Apache Flink, ksqlDB | Kafka Connect, Striim |
| **Delta** | A three-layered architecture that adds the ability to update and delete records in real-time. | Continuous | Advanced Lakehouse environments needing "ACID" transactions. | **E-commerce:** Instantly **deleting** a user's data across all systems for GDPR compliance. | Databricks (Delta Lake), Microsoft Fabric | Spark Structured Streaming | Databricks Autoloader, Estuary |

What does a data engineer actually do day to day?
1. Building and Fixing Pipelines
2. Monitoring and Reliability
3. Database & Infrastructure Management
4. Collaboration with Data Scientists/Software Engineers/Business Users/Data Analysts
5. Architectural Design

<!-- Credits from: 
https://www.google.com/, https://www.ascend.io/blog/etl-vs-elt#toc-what-s-the-difference-between-etl-elt-, <br/>
https://www.linkedin.com/pulse/modern-data-ingestion-patterns-batch-streaming-change-ziasc 
-->
