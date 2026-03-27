from utils import get_spark
from pyspark.sql.functions import col, upper, trim, when, udf
from pyspark.sql.types import StringType

# Initialize Spark
spark = get_spark("SocialMediaPhase1RawDataInspection")

posts_path = "data/raw/posts.csv"
engagement_path = "data/raw/engagement.csv"
users_path = "data/raw/users.csv"

# Read DataFrames
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

# Transformations
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
    trim(col("engagement_value")).try_cast("int")
)

users_cast_df = users_renamed_df.withColumn(
    "followers_count",
    trim(col("followers_count")).try_cast("int")
)

posts_cast_df = posts_selected_df.withColumn(
    "content_length",
    trim(col("content_length")).try_cast("int")
)

# Drop N/A column
posts_clean_df = posts_cast_df.dropna(subset=["post_id", "user_id", "category"])
engagement_clean_df = engagement_cast_df.dropna(subset=["engagement_id", "post_id", "engagement_type"])
users_clean_df = users_cast_df.dropna(subset=["creator_user_id", "username"])

# Drop duplicates
posts_dedup_df = posts_clean_df.dropDuplicates(["post_id"])
engagement_dedup_df = engagement_clean_df.dropDuplicates(["engagement_id"])
users_dedup_df = users_clean_df.dropDuplicates(["creator_user_id"])


# Standardize text fields
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

# Create column
engagement_scored_df = engagement_standardized_df.withColumn(
    "engagement_score",
    when(col("engagement_type") == "LIKE", 1)
    .when(col("engagement_type") == "COMMENT", 2)
    .when(col("engagement_type") == "SHARE", 3)
    .otherwise(0)
)

# Join datasets
posts_engagement_df = posts_standardized_df.join(
    engagement_scored_df.drop("user_id"),
    on="post_id",
    how="inner"
)


full_social_media_df = posts_engagement_df.join(
    users_dedup_df,
    posts_engagement_df.user_id == users_dedup_df.creator_user_id,
    how="left"
)
# print("posts:", posts_standardized_df.count())
# print("engagement:", engagement_scored_df.count())
# print("joined:", posts_engagement_df.count())

# posts_standardized_df.printSchema()
# engagement_scored_df.printSchema()


# Transformations for business relevance
filtered_social_media_df = full_social_media_df.filter(
    (col("engagement_score") > 0) &
    (col("creator_user_id").isNotNull())
)

#filtered_social_media_df.show(truncate=False)
#print("filtered_social_media_df:", filtered_social_media_df.count())

category_engagement_df = filtered_social_media_df.groupBy("category").agg(
    {"engagement_score": "sum"}
).withColumnRenamed("sum(engagement_score)", "total_engagement_score")

category_engagement_df.show(truncate=False)

creator_engagement_df = filtered_social_media_df.groupBy(
    "creator_user_id",
    "username"
).agg(
    {"engagement_score": "sum"}
).withColumnRenamed("sum(engagement_score)", "creator_total_engagement")

creator_engagement_df.show(truncate=False)

region_engagement_df = filtered_social_media_df.groupBy("region").agg(
    {"engagement_score": "sum"}
).withColumnRenamed("sum(engagement_score)", "region_total_engagement")

region_engagement_df.show(truncate=False)


# Use Spark SQL for Reporting Queries
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

top_categories_sql_df.show(truncate=False)

# Use a Simple UDF
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

creator_classified_df.select(
    "creator_user_id",
    "username",
    "followers_count",
    "creator_size"
).show(10, truncate=False)

# Write Processed Outputs
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