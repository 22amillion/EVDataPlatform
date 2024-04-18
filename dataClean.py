from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.functions import regexp_extract

# Function to initialize Spark session
def initialize_spark_session():
    return SparkSession.builder.appName("DSCI551Project").getOrCreate()

# Function to perform data cleaning
def data_clean(spark):
    # Read CSV file
    df = spark.read.csv("Electric_Vehicle_Population_Data.csv", header=True)

    # Define common selections
    common_selection = ["VIN (1-10)", "County", "City", "State", "Postal Code",
                        F.col("Model Year").alias("Year"), "Make", "Model",
                        F.col("Electric Vehicle Type").alias("Type"),
                        F.col("Clean Alternative Fuel Vehicle (CAFV) Eligibility").alias("Eligibility"),
                        F.col("Electric Range").alias("Range"),
                        F.col("Base MSRP").alias("MSRP"),
                        "Vehicle Location"]

    # Apply common selections and filters
    df_cleaned = df.select(*common_selection)\
                   .filter((df['Make'] != 'NULL') & (df['County'].isNotNull()))

    # Pattern for extracting longitude and latitude
    pattern = r'POINT \((-?\d+\.\d+) (-?\d+\.\d+)\)'

    # Extract longitude and latitude
    df_cleaned = df_cleaned.withColumn("longitude", regexp_extract("Vehicle Location", pattern, 1))\
                           .withColumn("latitude", regexp_extract("Vehicle Location", pattern, 2))

    # Write cleaned data to a new CSV file
    df_cleaned.write.csv("Electric_Vehicle_Population_Data_Cleaned", header=True, mode="overwrite")

    return df_cleaned

if __name__ == '__main__':
    # Initialize Spark session
    spark = initialize_spark_session()

    # Perform data cleaning
    df_cleaned = data_clean(spark)

    # Stop Spark session
    spark.stop()