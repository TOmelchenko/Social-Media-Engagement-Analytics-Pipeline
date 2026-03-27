from pyspark.sql import SparkSession
import json
import psycopg2
import os

def get_spark(app_name="ETL"):
    return (
        SparkSession.builder
        .appName(app_name)
        .master("local[*]")
        .config("spark.driver.host","127.0.0.1")
        .config("spark.driver.bindAddress","127.0.0.1")
        .getOrCreate()
    )


with open("config/settings.json") as f:
    settings = json.load(f)

def get_connection():
    return psycopg2.connect(
        dbname=settings["db_name"],
        user=settings["db_user"],
        password=os.getenv("DB_PASSWORD"),
        host=settings["db_host"],
        port=settings["db_port"]
    )