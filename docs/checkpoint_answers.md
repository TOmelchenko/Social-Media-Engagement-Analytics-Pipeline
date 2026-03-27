
# Phase 1 Checkpoint Tasks

Complete the following tasks after running the script.

## Task 1

Run the script successfully and confirm that all three raw files are loaded into Spark.

## Task 2

Record the row counts for:

* posts
* engagement
* users

## Task 3

Write down the schema observations:

* Which columns are strings?
* Which columns are numeric?
* Are any columns inferred differently than you expected?

## Task 4

Write down at least three important business columns from each dataset.

## Task 5

Explain in your own words:

* what a Spark DataFrame is
* what a schema is
* what the difference is between a transformation and an action

---


# Phase 2 Checkpoint Tasks

Complete the following after running the script.

## Task 1

Explain why you selected only certain columns from each dataset.

## Task 2

Identify at least three cleaning steps you applied and explain why each one matters.

## Task 3

Explain why duplicate engagement records can damage reporting accuracy.

## Task 4

Write down the business meaning of the `engagement_score` column.

## Task 5

List the three grouped summaries you created and explain what each one tells the business.

## Task 6

Explain the difference between using:

* DataFrame API
* Spark SQL

## Task 7

If you used the UDF step, explain why a UDF was useful in that example.

---
# Phase 3 Checkpoint Tasks

Complete the following after running the script.

## Task 1

Explain why `filtered_social_media_df` was a good candidate for caching.

## Task 2

Explain in your own words what caching does in Spark.

## Task 3

Check the number of partitions in at least two DataFrames and record your observations.

## Task 4

Explain the difference between:

* `repartition()`
* `coalesce()`

## Task 5

Explain why too many small output files can be a problem.

## Task 6

Explain what Parquet is in simple words.

## Task 7

Compare CSV and Parquet:

* Which one is easier for humans to inspect?
* Which one is generally better for analytics workloads?
* Why?

## Task 8

Explain why PostgreSQL may still be useful even when Spark does the heavy processing.

---