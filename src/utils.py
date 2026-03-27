# spark_session.py
from pyspark.sql import SparkSession

def get_spark(app_name="ETL"):
    return (
        SparkSession.builder
        .appName(app_name)
        .master("local[*]")
        .config("spark.driver.host","127.0.0.1")
        .config("spark.driver.bindAddress","127.0.0.1")
        .getOrCreate()
    )