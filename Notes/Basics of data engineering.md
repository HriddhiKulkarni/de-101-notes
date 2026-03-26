What is Data Engineering? <br/>
The process of collecting, maintaining, and transforming raw data into a usable format for use by data scientists, data analysts, etc., This process also involves building pipelines and creating systems around it.

What is ETL?<br/>
ETL(Extract, Transform, and Load). Extract involves extracting/reading the data, then transforming/processing it into clean usable format and finally loading it for use by data scientists/analysts/business users etc., for analytics purposes.

What is ELT?<br/>
ELT (Extract, Load, and Transform). This is a modern approach to ETL, here the data is dumped or "loaded" then "transform" step happens at the very end. 

ETL vs. ELT. When to use what process? <!-- Credits from: https://www.google.com/, https://www.ascend.io/blog/etl-vs-elt#toc-what-s-the-difference-between-etl-elt- -->

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

Data ingestion patterns: <br/>
Batch, Streaming, Change Data patterns (CDC), and Hybrid <br/>

Batch ingestion: The process of capturing and loading high-volume data in collected groups at scheduled intervals. <br/>
Streaming ingestion: The process of capturing and loading data as events occur, i.e., continuously in near real time. <br/>
Change Data Capture (CDC): The process that identifies and tracks only the specific data that has changed—such as inserts, updates, or deletes—in a source database. It then automatically moves those "deltas" to a target system in near real-time, keeping everything in sync without needing to reload entire datasets.<br/>
Hybrid ingestion: This combines all three patterns:
Batch for cost effective, stable, predictable loads
Streaming for real time operational intelligence
CDC for incremental, low latency synchronisation

What does a data engineer actually do day to day?

<!-- Credits from: 
https://www.google.com/, https://www.ascend.io/blog/etl-vs-elt#toc-what-s-the-difference-between-etl-elt-, <br/>
https://www.linkedin.com/pulse/modern-data-ingestion-patterns-batch-streaming-change-ziasc 
-->
