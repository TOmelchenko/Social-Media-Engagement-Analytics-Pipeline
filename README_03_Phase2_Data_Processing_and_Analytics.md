# Phase 2 — Spark Data Processing and Engagement Analytics

Welcome to **Phase 2** of the Social Media Engagement Analytics Pipeline project.

In **Phase 1**, you worked like a data engineer receiving raw files for the first time. You started Spark, loaded the data, inspected rows, studied schema, and began understanding the structure of the social media platform data.

Now the work becomes more realistic.

In this phase, you will begin transforming raw data into **business-usable analytics outputs**. This is the core engineering phase of the project. You will clean the data, select important fields, standardize columns, filter records, build new derived columns, create grouped summaries, use Spark SQL, and prepare engagement-focused outputs that help the business understand platform activity.

This phase is based on the learning from:

* **Week 3 — Day 3: Spark DataFrames & SQL, Data Processing**
* Main focus:

  * schema awareness
  * transformations
  * filtering
  * grouping
  * aggregation
  * Spark SQL
  * simple UDF usage when needed

---

# Phase Objective

By the end of this phase, you should be able to:

* select only the columns that matter
* rename unclear columns for readability
* cast data types correctly
* clean invalid or incomplete records
* filter rows for business relevance
* create derived columns
* aggregate engagement data
* use Spark SQL for reporting-style queries
* understand when a UDF is useful
* produce structured analytics-ready outputs for the next phase

---

# Why This Phase Matters in Real Work

In real companies, raw event data is almost never ready for business reporting.

A product team, analytics team, or operations team does not want millions of raw interaction rows with inconsistent formats. They want clean outputs that answer business questions such as:

* Which categories perform best?
* Which creators generate the most engagement?
* Which post types get the strongest response?
* Which regions are most active?
* Which posts are underperforming?

To support those questions, data engineers must transform the raw data into forms that are:

* cleaner
* more standardized
* easier to query
* easier to trust
* more meaningful for business users

That is exactly what this phase simulates.

---

# Business Scenario for This Phase

The analytics team at the social media company has asked your data engineering team to prepare engagement-focused datasets that can be used in reporting.

They specifically want support for questions like:

* total likes, comments, and shares by category
* total engagement by creator
* average engagement by post type
* regional engagement activity
* high-performing and low-performing content

The raw data is not ready for this directly.
Your task is to process it in Spark and build clean, structured outputs.

---

# What You Will Build in This Phase

In this phase, you will:

1. load the raw data again in Spark
2. select the most useful columns
3. rename and cast columns
4. clean invalid or incomplete rows
5. standardize engagement values
6. create derived columns
7. join datasets where needed
8. group and aggregate the results
9. create Spark SQL views
10. run reporting-style SQL queries
11. optionally use one simple UDF
12. save processed and summarized outputs

This phase is guided.
Code is given step by step, and each step includes explanation of:

* the theory
* the business reason
* the technical implementation

---

# Files Used in This Phase

We continue using the same raw datasets from Phase 1:

* `posts.csv`
* `engagement.csv`
* `users.csv`

Example fields may include:

## posts

* `post_id`
* `user_id`
* `category`
* `post_type`
* `content_length`
* `created_at`
* `region`

## engagement

* `engagement_id`
* `post_id`
* `engagement_type`
* `engagement_value`
* `user_id`
* `timestamp`

## users

* `user_id`
* `username`
* `country`
* `account_type`
* `followers_count`
* `join_date`

---

# Step 1 — Create the Phase 2 Script

## Task

Create a new Python file:

```python
src/phase2_transformations_and_analytics.py
```

## Why this matters

In real engineering work, separating code by phase or responsibility helps with:

* readability
* troubleshooting
* team collaboration
* future improvements

This script will contain the main transformation logic for the project.

---

# Step 2 — Start a Spark Session and Load the Raw Files

## Theory

Every phase that works with Spark must begin with a Spark session.

We also need to read the datasets again because this script should be able to run independently.

That is a good professional habit.
A script should not depend on another script already being open in memory.

---

## Technical implementation

Add this code:

```python
from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("SocialMediaPhase2TransformationsAndAnalytics")
    .master("local[*]")
    .getOrCreate()
)

posts_path = "data/raw/posts.csv"
engagement_path = "data/raw/engagement.csv"
users_path = "data/raw/users.csv"

posts_df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(posts_path)
)

engagement_df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(engagement_path)
)

users_df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(users_path)
)
```

---

## Explanation

This repeats the same loading pattern from Phase 1, but now we are preparing to actually process the data.

Even though this feels repetitive, it reflects real project structure: each script should be able to start its own work clearly.

---

# Step 3 — Select Relevant Columns

## Theory

Real datasets often contain columns that are not immediately needed for a particular business question.

Selecting the most useful columns helps:

* reduce clutter
* improve readability
* make the logic easier to follow
* reduce unnecessary processing

This is one of the most common first transformation steps in a pipeline.

---

## Technical implementation

Add:

```python
posts_selected_df = posts_df.select(
    "post_id",
    "user_id",
    "category",
    "post_type",
    "content_length",
    "created_at",
    "region"
)

engagement_selected_df = engagement_df.select(
    "engagement_id",
    "post_id",
    "engagement_type",
    "engagement_value",
    "user_id",
    "timestamp"
)

users_selected_df = users_df.select(
    "user_id",
    "username",
    "country",
    "account_type",
    "followers_count",
    "join_date"
)
```

---

## Explanation

### `select(...)`

This is a Spark **transformation**.

It creates a new DataFrame that keeps only the specified columns.

### Business meaning

The business is interested in analytics-ready engagement reporting, so we focus on columns that support:

* identifying posts
* identifying users/creators
* measuring engagement
* grouping by category or region

---

# Step 4 — Rename Columns for Clarity

## Theory

Sometimes columns are technically correct but not ideal for readability.

Renaming columns helps make the transformation logic easier to understand, especially when joining multiple DataFrames.

Clear naming is important in team environments.

---

## Technical implementation

Add:

```python
users_renamed_df = users_selected_df.withColumnRenamed("user_id", "creator_user_id")
```

---

## Explanation

### Why rename here?

Both `posts` and `users` contain a user identifier.
When joining them, having the same column name in multiple places can be confusing.

By renaming the user ID in the users DataFrame, we make the join logic easier to understand later.

### Business meaning

A clean naming convention reduces mistakes when building production pipelines.

---

# Step 5 — Cast Data Types Where Needed

## Theory

Even when Spark infers schema automatically, you should still think carefully about data types.

In real projects, data types matter because they affect:

* filtering
* aggregation
* comparisons
* correctness

For example:

* engagement values must behave like numbers
* follower counts must behave like numbers
* timestamps may need conversion later

---

## Technical implementation

Add:

```python
from pyspark.sql.functions import col

engagement_cast_df = engagement_selected_df.withColumn(
    "engagement_value",
    col("engagement_value").cast("int")
)

users_cast_df = users_renamed_df.withColumn(
    "followers_count",
    col("followers_count").cast("int")
)

posts_cast_df = posts_selected_df.withColumn(
    "content_length",
    col("content_length").cast("int")
)
```

---

## Explanation

### `withColumn(... cast(...))`

This replaces the existing column with a new version of the same column using the specified data type.

### Why this matters

You cannot reliably sum, average, or compare a column if it is stored incorrectly as text.

### Business meaning

The analytics team needs trustworthy numbers.
Casting is part of making the dataset reliable.

---

# Step 6 — Remove Invalid or Incomplete Records

## Theory

Real data often contains missing or incomplete rows.

A post without a `post_id`, or an engagement record without a `post_id`, is difficult to use in downstream analytics.

You should clean obvious issues before aggregation.

---

## Technical implementation

Add:

```python
posts_clean_df = posts_cast_df.dropna(subset=["post_id", "user_id", "category"])
engagement_clean_df = engagement_cast_df.dropna(subset=["engagement_id", "post_id", "engagement_type"])
users_clean_df = users_cast_df.dropna(subset=["creator_user_id", "username"])
```

---

## Explanation

### `dropna(subset=[...])`

This removes rows where important columns are null.

### Why these columns?

These are key identifiers or business fields.
If they are missing, the row becomes much harder to trust or use.

### Business meaning

If engagement rows are missing essential identifiers, reports can become misleading or incomplete.

---

# Step 7 — Remove Duplicate Records

## Theory

Duplicate records are a common real-world problem.

If duplicates are not handled, engagement metrics may be inflated incorrectly.

---

## Technical implementation

Add:

```python
posts_dedup_df = posts_clean_df.dropDuplicates(["post_id"])
engagement_dedup_df = engagement_clean_df.dropDuplicates(["engagement_id"])
users_dedup_df = users_clean_df.dropDuplicates(["creator_user_id"])
```

---

## Explanation

### `dropDuplicates([...])`

This keeps only one row for each unique key.

### Business meaning

If the same engagement event appears twice, total engagement will be overstated.
This step protects reporting quality.

---

# Step 8 — Standardize Text Fields

## Theory

Text fields such as category names or post types can become inconsistent.

For example:

* `"technology"`
* `"Technology"`
* `"TECHNOLOGY"`

If these are not standardized, grouping results may split what should be one category into multiple separate groups.

---

## Technical implementation

Add:

```python
from pyspark.sql.functions import upper, trim

posts_standardized_df = (
    posts_dedup_df
    .withColumn("category", upper(trim(col("category"))))
    .withColumn("post_type", upper(trim(col("post_type"))))
    .withColumn("region", upper(trim(col("region"))))
)

engagement_standardized_df = engagement_dedup_df.withColumn(
    "engagement_type",
    upper(trim(col("engagement_type")))
)
```

---

## Explanation

### `trim(...)`

Removes extra spaces.

### `upper(...)`

Converts text to uppercase.

### Business meaning

Standardized text fields produce cleaner and more accurate reports.

For example:

* `"technology"` and `"Technology"` should not appear as separate categories in the final output.

---

# Step 9 — Create a Derived Engagement Score

## Theory

Raw engagement data may contain multiple interaction types such as:

* LIKE
* COMMENT
* SHARE

Sometimes a business wants a simple scoring model so that one metric can represent engagement more clearly.

For example:

* like = 1 point
* comment = 2 points
* share = 3 points

This is a simplified business rule, but it helps demonstrate how data engineers create derived columns for analytics.

---

## Technical implementation

Add:

```python
from pyspark.sql.functions import when

engagement_scored_df = engagement_standardized_df.withColumn(
    "engagement_score",
    when(col("engagement_type") == "LIKE", 1)
    .when(col("engagement_type") == "COMMENT", 2)
    .when(col("engagement_type") == "SHARE", 3)
    .otherwise(0)
)
```

---

## Explanation

### `when(...).when(...).otherwise(...)`

This is Spark’s way of expressing conditional logic for column creation.

### Business meaning

The company wants a simple metric that gives more weight to deeper engagement actions.

A share often means stronger engagement than a like, so it receives a higher score in this example.

---

# Step 10 — Join the Datasets

## Theory

Raw data is often split across multiple tables or files.

To answer business questions properly, data engineers frequently join datasets together.

In this project:

* `posts` contains content information
* `engagement` contains interaction events
* `users` contains creator information

We need to combine them.

---

## Technical implementation

Add:

```python
posts_engagement_df = posts_standardized_df.join(
    engagement_scored_df,
    on="post_id",
    how="inner"
)

full_social_media_df = posts_engagement_df.join(
    users_dedup_df,
    posts_engagement_df.user_id == users_dedup_df.creator_user_id,
    how="left"
)
```

---

## Explanation

### First join

This combines post information with engagement events using `post_id`.

### Second join

This combines post/engagement records with creator profile information.

### Why use `left` for the second join?

If a user profile is missing, we may still want to keep the engagement record rather than lose it completely.

### Business meaning

The business does not want isolated tables.
It wants joined information that connects content, interaction, and creator context.

---

# Step 11 — Filter Records for Business Relevance

## Theory

Not all records are equally useful for the business question you are solving.

Filtering allows you to:

* remove weak or irrelevant rows
* focus on key categories
* isolate valid engagement activity

---

## Technical implementation

Add:

```python
filtered_social_media_df = full_social_media_df.filter(
    col("engagement_score") > 0
)
```

---

## Explanation

This keeps only rows with meaningful engagement scores.

### Business meaning

If the scoring logic produced 0 for unknown or unsupported engagement types, those rows may not be helpful for our engagement reports.

---

# Step 12 — Group and Aggregate the Data

Now the project begins producing real analytics value.

This is one of the most important steps in the whole phase.

---

## Task 1 — Engagement by Category

### Theory

The business wants to know which content categories perform best.

### Technical implementation

Add:

```python
category_engagement_df = filtered_social_media_df.groupBy("category").agg(
    {"engagement_score": "sum"}
).withColumnRenamed("sum(engagement_score)", "total_engagement_score")
```

Then display it:

```python
category_engagement_df.show(truncate=False)
```

---

## Explanation

### `groupBy("category")`

This groups rows by category.

### `.agg({"engagement_score": "sum"})`

This sums the engagement score for each category.

### Business meaning

This produces one of the most useful high-level reports:
**Which categories generate the most total engagement?**

---

## Task 2 — Engagement by Creator

### Theory

The business also wants to know which creators are driving activity.

### Technical implementation

Add:

```python
creator_engagement_df = filtered_social_media_df.groupBy(
    "creator_user_id",
    "username"
).agg(
    {"engagement_score": "sum"}
).withColumnRenamed("sum(engagement_score)", "creator_total_engagement")
```

Display it:

```python
creator_engagement_df.show(truncate=False)
```

---

## Explanation

This groups by creator and sums total engagement score.

### Business meaning

This helps the business identify high-performing creators.

---

## Task 3 — Engagement by Region

### Technical implementation

Add:

```python
region_engagement_df = filtered_social_media_df.groupBy("region").agg(
    {"engagement_score": "sum"}
).withColumnRenamed("sum(engagement_score)", "region_total_engagement")
```

Display it:

```python
region_engagement_df.show(truncate=False)
```

---

## Business meaning

This supports questions such as:

* Which regions are most active?
* Where is user interaction strongest?

---

# Step 13 — Use Spark SQL for Reporting Queries

## Theory

Spark supports two main ways of working:

* DataFrame API
* Spark SQL

Some engineers prefer DataFrame code for pipelines.
Some analysts or SQL-heavy users prefer SQL for reporting logic.

You should be comfortable with both.

---

## Technical implementation

First create a temporary view:

```python
filtered_social_media_df.createOrReplaceTempView("social_media_activity")
```

Now run a SQL query:

```python
top_categories_sql_df = spark.sql("""
    SELECT
        category,
        SUM(engagement_score) AS total_engagement_score,
        COUNT(DISTINCT post_id) AS total_posts
    FROM social_media_activity
    GROUP BY category
    ORDER BY total_engagement_score DESC
""")
```

Display it:

```python
top_categories_sql_df.show(truncate=False)
```

---

## Explanation

### `createOrReplaceTempView(...)`

This makes the DataFrame available as a temporary table inside Spark SQL.

### `spark.sql(...)`

This allows you to query the data using SQL syntax.

### Business meaning

Many real reporting tasks are easier to explain and validate using SQL-style logic.

---

# Step 14 — Optional: Use a Simple UDF

## Theory

A **UDF** is a **User Defined Function**.

It allows you to apply custom logic when built-in Spark functions are not enough.

Important note:

* Use built-in Spark functions first whenever possible
* Use UDFs only when you really need custom logic

UDFs can be slower than Spark’s native functions, so they should be used carefully.

---

## Example use case

Suppose the business wants to classify creators into simple tiers based on follower count:

* Small Creator
* Medium Creator
* Large Creator

---

## Technical implementation

Add:

```python
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType

def classify_creator_size(followers_count):
    if followers_count is None:
        return "UNKNOWN"
    elif followers_count < 1000:
        return "SMALL"
    elif followers_count < 10000:
        return "MEDIUM"
    else:
        return "LARGE"

classify_creator_size_udf = udf(classify_creator_size, StringType())

creator_classified_df = filtered_social_media_df.withColumn(
    "creator_size",
    classify_creator_size_udf(col("followers_count"))
)
```

Display it:

```python
creator_classified_df.select(
    "creator_user_id",
    "username",
    "followers_count",
    "creator_size"
).show(10, truncate=False)
```

---

## Explanation

### Why use a UDF here?

We want custom business logic that maps follower counts into labeled categories.

### Business meaning

This makes it easier for business users to interpret creator scale without reading raw follower counts directly.

---

# Step 15 — Write Processed Outputs

## Theory

A data pipeline should usually produce outputs, not just printed results.

At this phase, we want to save the processed and aggregated datasets so they can be used later.

We will write outputs to files inside the project.

---

## Technical implementation

First create output folders if needed inside your project.

Then write the outputs:

```python
category_engagement_df.write.mode("overwrite").csv(
    "data/processed/category_engagement_summary",
    header=True
)

creator_engagement_df.write.mode("overwrite").csv(
    "data/processed/creator_engagement_summary",
    header=True
)

region_engagement_df.write.mode("overwrite").csv(
    "data/processed/region_engagement_summary",
    header=True
)
```

---

## Explanation

### `.write.mode("overwrite").csv(...)`

This writes the DataFrame to CSV files.

### Why use CSV here?

CSV is simple and easy to inspect manually.

Later, in Phase 3, we will discuss **Parquet** and why it is often better for analytics workloads.

For now, CSV is fine for visibility and learning.

---

# Important Beginner Note — What is Parquet?

You have not used Parquet yet in this phase, but you will likely see it in the next phase.

## What is Parquet?

**Parquet** is a file format designed for analytics and big data processing.

Unlike CSV, which stores data as plain text row by row, Parquet stores data in a **columnar format**.

That means:

* similar values in the same column are stored together
* it is often faster for analytics queries
* it is usually more storage-efficient
* it works very well with Spark

## Why not use it immediately here?

In this phase, the priority is:

* understanding transformations
* seeing outputs clearly
* keeping things beginner-friendly

So CSV is fine here.

In Phase 3, when we talk about better engineering choices and performance, Parquet will become more important and will be explained again.

---

# Step 16 — Stop the Spark Session

Add this at the end of the script:

```python
spark.stop()
```

---

# Full Example Script for Phase 2

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, upper, trim, when, udf
from pyspark.sql.types import StringType

spark = (
    SparkSession.builder
    .appName("SocialMediaPhase2TransformationsAndAnalytics")
    .master("local[*]")
    .getOrCreate()
)

posts_path = "data/raw/posts.csv"
engagement_path = "data/raw/engagement.csv"
users_path = "data/raw/users.csv"

posts_df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(posts_path)
)

engagement_df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(engagement_path)
)

users_df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(users_path)
)

posts_selected_df = posts_df.select(
    "post_id",
    "user_id",
    "category",
    "post_type",
    "content_length",
    "created_at",
    "region"
)

engagement_selected_df = engagement_df.select(
    "engagement_id",
    "post_id",
    "engagement_type",
    "engagement_value",
    "user_id",
    "timestamp"
)

users_selected_df = users_df.select(
    "user_id",
    "username",
    "country",
    "account_type",
    "followers_count",
    "join_date"
)

users_renamed_df = users_selected_df.withColumnRenamed("user_id", "creator_user_id")

engagement_cast_df = engagement_selected_df.withColumn(
    "engagement_value",
    col("engagement_value").cast("int")
)

users_cast_df = users_renamed_df.withColumn(
    "followers_count",
    col("followers_count").cast("int")
)

posts_cast_df = posts_selected_df.withColumn(
    "content_length",
    col("content_length").cast("int")
)

posts_clean_df = posts_cast_df.dropna(subset=["post_id", "user_id", "category"])
engagement_clean_df = engagement_cast_df.dropna(subset=["engagement_id", "post_id", "engagement_type"])
users_clean_df = users_cast_df.dropna(subset=["creator_user_id", "username"])

posts_dedup_df = posts_clean_df.dropDuplicates(["post_id"])
engagement_dedup_df = engagement_clean_df.dropDuplicates(["engagement_id"])
users_dedup_df = users_clean_df.dropDuplicates(["creator_user_id"])

posts_standardized_df = (
    posts_dedup_df
    .withColumn("category", upper(trim(col("category"))))
    .withColumn("post_type", upper(trim(col("post_type"))))
    .withColumn("region", upper(trim(col("region"))))
)

engagement_standardized_df = engagement_dedup_df.withColumn(
    "engagement_type",
    upper(trim(col("engagement_type")))
)

engagement_scored_df = engagement_standardized_df.withColumn(
    "engagement_score",
    when(col("engagement_type") == "LIKE", 1)
    .when(col("engagement_type") == "COMMENT", 2)
    .when(col("engagement_type") == "SHARE", 3)
    .otherwise(0)
)

posts_engagement_df = posts_standardized_df.join(
    engagement_scored_df,
    on="post_id",
    how="inner"
)

full_social_media_df = posts_engagement_df.join(
    users_dedup_df,
    posts_engagement_df.user_id == users_dedup_df.creator_user_id,
    how="left"
)

filtered_social_media_df = full_social_media_df.filter(
    col("engagement_score") > 0
)

category_engagement_df = filtered_social_media_df.groupBy("category").agg(
    {"engagement_score": "sum"}
).withColumnRenamed("sum(engagement_score)", "total_engagement_score")

creator_engagement_df = filtered_social_media_df.groupBy(
    "creator_user_id",
    "username"
).agg(
    {"engagement_score": "sum"}
).withColumnRenamed("sum(engagement_score)", "creator_total_engagement")

region_engagement_df = filtered_social_media_df.groupBy("region").agg(
    {"engagement_score": "sum"}
).withColumnRenamed("sum(engagement_score)", "region_total_engagement")

filtered_social_media_df.createOrReplaceTempView("social_media_activity")

top_categories_sql_df = spark.sql("""
    SELECT
        category,
        SUM(engagement_score) AS total_engagement_score,
        COUNT(DISTINCT post_id) AS total_posts
    FROM social_media_activity
    GROUP BY category
    ORDER BY total_engagement_score DESC
""")

def classify_creator_size(followers_count):
    if followers_count is None:
        return "UNKNOWN"
    elif followers_count < 1000:
        return "SMALL"
    elif followers_count < 10000:
        return "MEDIUM"
    else:
        return "LARGE"

classify_creator_size_udf = udf(classify_creator_size, StringType())

creator_classified_df = filtered_social_media_df.withColumn(
    "creator_size",
    classify_creator_size_udf(col("followers_count"))
)

category_engagement_df.write.mode("overwrite").csv(
    "data/processed/category_engagement_summary",
    header=True
)

creator_engagement_df.write.mode("overwrite").csv(
    "data/processed/creator_engagement_summary",
    header=True
)

region_engagement_df.write.mode("overwrite").csv(
    "data/processed/region_engagement_summary",
    header=True
)

spark.stop()
```

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

# What You Should Understand Before Moving to Phase 3

Before continuing, make sure you are comfortable with:

* selecting and renaming columns
* casting data types
* removing nulls and duplicates
* standardizing text fields
* creating derived columns
* joining multiple DataFrames
* filtering rows
* grouping and aggregating data
* creating temp views
* running Spark SQL queries
* understanding why processed outputs matter to the business

If these ideas still feel unclear, review this phase before moving on.

---

# End of Phase 2

At this point, you have completed the main transformation phase of the project.

You now understand how to:

* move from raw data to processed data
* turn messy records into cleaner outputs
* create engagement-based business summaries
* use both Spark DataFrame logic and Spark SQL
* prepare the data for more professional engineering decisions in the next phase

This is the core of real data engineering work.

---

# Next Step

Continue to:

**`README_04_Phase3_Performance_and_Output_Optimization.md`**

In the next phase, you will take your Spark pipeline one step further by applying performance-aware decisions such as caching, partitioning, and better output design.
