
# Phase 1 Checkpoint Tasks

Complete the following tasks after running the script.

## Task 1

Run the script successfully and confirm that all three raw files are loaded into Spark.
Yes, all three raw files are loaded into Spark.

## Task 2

Record the row counts for:

* posts - 228 
* engagement - 440
* users - 233

## Task 3

Write down the schema observations:

* Which columns are strings?  For engagements, post (except content_length) and users all columns are string.
* Which columns are numeric? - Only content_length: integer (nullable = true)
* Are any columns inferred differently than you expected? The created_at, timestamp, join_date are supposed to be date or datetime format and engagement_value - numeric.

## Task 4

Write down at least three important business columns from each dataset.
Posts:
	•	category
	•	post_type
	•	region

Engagement:
	•	post_id
	•	engagement_type
	•	engagement_value
	•	timestamp

Users:
	•	user_id / creator_user_id
	•	username
	•	followers_count
	•	account_type
	•	country

## Task 5

Explain in your own words:

* what a Spark DataFrame is - A distributed table of data that Spark processes across multiple nodes.
* what a schema is - The structure of the DataFrame (column names + data types).
* what the difference is between a transformation and an action. - Transformation → lazy (select, filter, join), prepare execution plan. 	Action → triggers execution (count, show, collect, write)

---


# Phase 2 Checkpoint Tasks

Complete the following after running the script.

## Task 1

Explain why you selected only certain columns from each dataset.

We selected only important columns to:
- reduce memory usage
- improve performance
- keep only business-relevant data
- simplify joins

## Task 2

Identify at least three cleaning steps you applied and explain why each one matters.
1.	dropna() → removes incomplete records that break joins/metrics
2.	dropDuplicates() → prevents duplicate engagement inflation
3.	trim() + upper() → standardizes text for consistent grouping


## Task 3

Explain why duplicate engagement records can damage reporting accuracy.

Duplicate engagement records:
- inflate engagement_score
- distort ranking of creators
- lead to incorrect business decisions

## Task 4

Write down the business meaning of the `engagement_score` column.
A weighted value representing engagement strength:
- LIKE = 1
- COMMENT = 2
- SHARE = 3
higher value = stronger user interaction


## Task 5

List the three grouped summaries you created and explain what each one tells the business.

Category engagement: → total engagement per content category
Creator engagement: → total engagement per user (who creates content)
Region engagement: → engagement distribution across geographic regions


## Task 6

Explain the difference between using:

* DataFrame API
* Spark SQL

DataFrame API:
- Python-based
- type-safe operations
- easier for ETL pipelines

Spark SQL:
- SQL queries
- easier for analysts
- good for ad-hoc analysis

## Task 7

If you used the UDF step, explain why a UDF was useful in that example.

- UDF helps when logic cannot be expressed with built-in functions
- but it is slower because it runs row-by-row


---
# Phase 3 Checkpoint Tasks

Complete the following after running the script.

## Task 1

Explain why `filtered_social_media_df` was a good candidate for caching.
Because:
- reused in multiple aggregations
- avoids recomputation of joins + filters
- improves performance significantly

## Task 2

Explain in your own words what caching does in Spark.
Caching stores DataFrame in memory (or disk) after first computation so Spark does not recompute lineage again.

## Task 3

Check the number of partitions in at least two DataFrames and record your observations.

Filtered DataFrame partitions:  200
Category summary partitions: 1
Creator summary partitions: 1
Region summary partitions: 1

## Task 4

Explain the difference between:

* `repartition()`
* `coalesce()`

`repartition()`
- increases or changes partitions
- causes full shuffle

`coalesce()`
- reduces partitions
- avoids full shuffle (faster)

## Task 5

Explain why too many small output files can be a problem.
Because of:
- slow reads
- slow queries in downstream systems
- metadata overhead


## Task 6

Explain what Parquet is in simple words.
A columnar storage format optimized for analytics (compressed + fast reads).

## Task 7

Compare CSV and Parquet:

* Which one is easier for humans to inspect?
* Which one is generally better for analytics workloads?
* Why?

- Easier for humans: CSV
- Better for analytics: Parquet
- Why: Parquet is compressed, column-based, faster, and supports schema

## Task 8

Explain why PostgreSQL may still be useful even when Spark does the heavy processing.

Because:
- stores final curated results
- supports BI tools (Tableau, Power BI)
- fast querying for dashboards
- persistent structured storage outside Spark

---