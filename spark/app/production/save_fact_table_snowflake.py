from pyspark.sql import SparkSession

# Spark Session
spark = SparkSession.builder.appName("SaveFactTableSnowflake") \
    .config("spark.hadoop.fs.defaultFS", "hdfs://namenode:8020") \
    .config("spark.hadoop.dfs.replication", "1") \
    .getOrCreate()

# Spark Context
sc = spark.sparkContext
sc.setLogLevel("ERROR")

# Read data from Parquet file
fact_table_df = spark.read.parquet("hdfs://namenode:8020/output/final_fact_table.parquet")

# Show dataframe
fact_table_df.show()

sfOptions = {
    "sfUrl": "https://vv06073.europe-west4.gcp.snowflakecomputing.com",
    "sfUser": "YOUR_SNOWFLAKE_USERNAME",
    "sfPassword": "YOUR_SNOWFLAKE_PASSWORD",
    "sfRole": "ACCOUNTADMIN",
    "sfDatabase": "DENG_PRODUCTION",
    "sfSchema": "DATA_PROD",
    "sfWarehouse": "COMPUTE_WH",
    "dbtable": "FACT_TABLE"
}

# Write data to Snowflake
fact_table_df.write \
    .format("net.snowflake.spark.snowflake") \
    .options(**sfOptions) \
    .mode("overwrite") \
    .save()

# Stop Spark Session
spark.stop()