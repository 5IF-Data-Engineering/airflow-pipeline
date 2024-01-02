from pyspark.sql import SparkSession
import sys

# Arguments
name_dim = sys.argv[1]

# Spark Session
spark = SparkSession.builder.appName("SaveDimensionToSnowflake") \
    .config("spark.hadoop.fs.defaultFS", "hdfs://namenode:8020") \
    .config("spark.hadoop.dfs.replication", "1") \
    .getOrCreate()

# Spark Context
sc = spark.sparkContext
sc.setLogLevel("ERROR")

# Read data from Parquet file
dim_df = spark.read.parquet("hdfs://namenode:8020/output/{}.parquet".format(name_dim))

# Show dataframe
dim_df.show()

sfOptions = {
    "sfUrl": "https://vv06073.europe-west4.gcp.snowflakecomputing.com",
    "sfUser": "YOUR_SNOWFLAKE_USERNAME",
    "sfPassword": "YOUR_SNOWFLAKE_PASSWORD",
    "sfRole": "ACCOUNTADMIN",
    "sfDatabase": "DENG_PRODUCTION",
    "sfSchema": "DATA_PROD",
    "sfWarehouse": "COMPUTE_WH",
    "dbtable": "{}_DIM".format(name_dim.upper())
}

# Write data to Snowflake
dim_df.write \
    .format("net.snowflake.spark.snowflake") \
    .options(**sfOptions) \
    .mode("overwrite") \
    .save()

# Stop Spark Session
spark.stop()