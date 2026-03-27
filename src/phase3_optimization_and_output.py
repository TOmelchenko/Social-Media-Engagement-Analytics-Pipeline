from utils import get_spark, get_connection
from pyspark.sql.functions import col, upper, trim, when, udf
from pyspark.sql.types import StringType
import json
from dotenv import load_dotenv

load_dotenv()

# Load settings for db connection
with open("config/settings.json") as f:
    settings = json.load(f)

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

# Transformations for business relevance
filtered_social_media_df = full_social_media_df.filter(
    (col("engagement_score") > 0) &
    (col("creator_user_id").isNotNull())
)

filtered_social_media_df = filtered_social_media_df.cache()
filtered_social_media_df.count()

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


print("Filtered DataFrame partitions:", filtered_social_media_df.rdd.getNumPartitions())
print("Category summary partitions:", category_engagement_df.rdd.getNumPartitions())
print("Creator summary partitions:", creator_engagement_df.rdd.getNumPartitions())
print("Region summary partitions:", region_engagement_df.rdd.getNumPartitions())


category_engagement_repartitioned_df = category_engagement_df.repartition(2)
creator_engagement_repartitioned_df = creator_engagement_df.repartition(2)
region_engagement_repartitioned_df = region_engagement_df.repartition(2)

category_engagement_single_file_df = category_engagement_df.coalesce(1)
region_engagement_single_file_df = region_engagement_df.coalesce(1)


# Write Processed Outputs

category_engagement_single_file_df.write.mode("overwrite").csv(
    "data/output/csv/category_engagement_summary",
    header=True
)

creator_engagement_repartitioned_df.write.mode("overwrite").csv(
    "data/output/csv/creator_engagement_summary",
    header=True
)

region_engagement_single_file_df.write.mode("overwrite").csv(
    "data/output/csv/region_engagement_summary",
    header=True
)

category_engagement_repartitioned_df.write.mode("overwrite").parquet(
    "data/output/parquet/category_engagement_summary"
)

creator_engagement_repartitioned_df.write.mode("overwrite").parquet(
    "data/output/parquet/creator_engagement_summary"
)

region_engagement_repartitioned_df.write.mode("overwrite").parquet(
    "data/output/parquet/region_engagement_summary"
)

# Read Back a Parquet File to Verify It
parquet_check_df = spark.read.parquet("data/output/parquet/category_engagement_summary")
parquet_check_df.show(truncate=False)
parquet_check_df.printSchema()


# Save data in PostgreSQL
final_reporting_df = creator_engagement_df.select(
    "creator_user_id",
    "username",
    "creator_total_engagement"
)
final_reporting_df.show(truncate=False)

def load_final_report(records):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM final_report;")

    insert_query = """
        INSERT INTO final_report (
            creator_user_id,
            username,
            creator_total_engagement
        )
        VALUES (%s, %s, %s);
    """

    for record in records:
        cursor.execute(
            insert_query,
            (
                record["creator_user_id"],
                record["username"],
                record["creator_total_engagement"]
            )
        )

    connection.commit()
    cursor.close()
    connection.close()

load_final_report(final_reporting_df.collect())

spark.stop()