from utils import get_spark

#import os
#from dotenv import load_dotenv

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


# Sample data
print("Posts Data")
posts_df.show(5, truncate=False)

print("Engagement Data")
engagement_df.show(5, truncate=False)

print("Users Data")
users_df.show(5, truncate=False)

# Inspect schema
print("Posts Schema")
posts_df.printSchema()

print("Engagement Schema")
engagement_df.printSchema()

print("Users Schema")
users_df.printSchema()

# List of columns
print("Posts Columns:", posts_df.columns)
print("Engagement Columns:", engagement_df.columns)
print("Users Columns:", users_df.columns)

# Row counts
print("Posts Count:", posts_df.count())
print("Engagement Count:", engagement_df.count())
print("Users Count:", users_df.count())

# Transformations
posts_selected_df = posts_df.select(
    "post_id",
    "user_id",
    "category",
    "post_type",
    "created_at",
    "region"
)

posts_selected_df.show(5, truncate=False)

technology_posts_df = posts_df.filter(posts_df.category == "Technology")
technology_posts_df.show(5, truncate=False)

from pyspark.sql.functions import length

posts_with_title_length_df = posts_df.withColumn(
    "category_name_length",
    length(posts_df.category)
)

posts_with_title_length_df.show(5, truncate=False)

spark.stop()