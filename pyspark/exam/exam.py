from urllib.request import urlretrieve
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import *
from pyspark.sql.types import *
import os
import builtins


# download files
BASE_URL = "https://assets-datascientest.s3.eu-west-1.amazonaws.com"
def download_file(fn: str):
    if not os.path.exists(fn):
        urlretrieve(f"{BASE_URL}/{fn}", fn)

for fn in ("gps_app.csv", "gps_user.csv"):
    download_file(fn)

# bootstrap Spark
spark = SparkSession.builder.appName("PySpark Exam").master("local[*]").getOrCreate()

# read and normalise column names
def normalise(df: DataFrame) -> DataFrame:
    names = [c.strip().lower().replace(" ", "_") for c in df.columns]
    return df.toDF(*names)

raw_app = spark.read.option("header", True).option("inferSchema", True).option("escape", "\"").csv("gps_app.csv")
raw_user = spark.read.option("header", True).option("inferSchema", True).option("escape", "\"").csv("gps_user.csv")

raw_app = normalise(raw_app)
raw_user = normalise(raw_user)

# 3 clean raw_app missing values
# 3.1 fill rating with median
median_rating = raw_app.approxQuantile("rating", [0.5], 0.0)[0]
df1 = raw_app.withColumn("rating", when(col("rating").isNull(), median_rating).otherwise(col("rating")))

# 3.2 fill type with mode
mode_type = df1.groupBy("type").count().orderBy(col("count").desc()).first()["type"]
df2 = df1.withColumn("type", when(col("type").isNull(), mode_type).otherwise(col("type")))

# 3.3 normalise type strings and fill content_rating. Spark can read literal nan or zero, so map back to mode
df3 = (df2
       .withColumn("type", lower(regexp_replace(col("type"), r"\s+", "")))
       .withColumn("type", when(col("type").isin("nan", "0"), mode_type).otherwise(col("type")))
       .withColumn("content_rating", when(col("content_rating").isNull(), lit("unrated")).otherwise(col("content_rating")))
)

# 3.4 fill current_ver and android_ver columns with their modes
apps_clean = df3
for c in ("current_ver", "android_ver"):
    m = apps_clean.groupBy(c).count().orderBy(col("count").desc()).first()[c]
    apps_clean = apps_clean.withColumn(c, when(col(c).isNull(), m).otherwise(col(c)))

# 3.5 verify no more missing values
null_map = apps_clean.select(
    *[(col(c).isNull().cast("int").alias(c)) for c in apps_clean.columns]
).groupBy().sum().first().asDict()
total_nulls = builtins.sum(null_map.values())
assert total_nulls == 0, f"raw_app still has {total_nulls} nulls"

# 4 clean raw_user missing data
# 4.1 examine and count missing values present in dataset
counts = {
    c: raw_user.filter(col(c).isNull() | col(c).eqNullSafe("nan")).count() 
    for c in raw_user.columns
}
print("4.1 missing before clean:", counts)

# 4.2 drop rows where translated_review is null or literal 'nan'
u_one = raw_user.filter(
    col("translated_review").isNotNull()
).filter(~col("translated_review").eqNullSafe("nan"))

# 4.3 assert no more nulls in key columns
for c in ("translated_review", "sentiment", "sentiment_polarity", "sentiment_subjectivity"):
    n = u_one.filter(col(c).isNull()).count()
    assert n==0, f"raw_user.{c} still has {n} nulls"

# 5 deep clean raw_user 
# 5.1 find non-numeric in polarity / subjectivity
u_two = (
    u_one
        .withColumn("_p", col("sentiment_polarity").cast("double"))
        .withColumn("_s", col("sentiment_subjectivity").cast("double"))
)
bad_p = u_two.filter(col("_p").isNull() & col("sentiment_polarity").isNotNull()).count()
bad_s = u_two.filter(col("_s").isNull() & col("sentiment_subjectivity").isNotNull()).count()
print("5.1 bad polarity / subjectivity rows:", bad_p, bad_s)

# 5.2 convert numeric columns to float format
u_three = (u_two.drop("_p","_s")
           # Remove non-numeric characters and corrupted values from sentiment columns
           .withColumn("sentiment_polarity_clean", 
                      regexp_replace(col("sentiment_polarity").cast("string"), r"[^\d\.\-]", ""))
           .withColumn("sentiment_subjectivity_clean", 
                      regexp_replace(col("sentiment_subjectivity").cast("string"), r"[^\d\.\-]", ""))
           # Handle empty strings after cleaning
           .withColumn("sentiment_polarity_clean", 
                      when(col("sentiment_polarity_clean") == "", "0").otherwise(col("sentiment_polarity_clean")))
           .withColumn("sentiment_subjectivity_clean", 
                      when(col("sentiment_subjectivity_clean") == "", "0").otherwise(col("sentiment_subjectivity_clean")))
           # Cast to float
           .withColumn("sentiment_polarity", col("sentiment_polarity_clean").cast(FloatType()))
           .withColumn("sentiment_subjectivity", col("sentiment_subjectivity_clean").cast(FloatType()))
           .drop("sentiment_polarity_clean", "sentiment_subjectivity_clean"))

# 5.3 remove special characters and collapse spaces
u_four = u_three.withColumn("translated_review",
                            regexp_replace(col("translated_review"), r"[^A-Za-z0-9 ]", " ")) \
                .withColumn("translated_review", 
                            regexp_replace(col("translated_review"), r"\s{2,}", " "))
     
# 5.4 convert all characters in translated_review column to lowercase
u_five = u_four.withColumn("translated_review", lower(col("translated_review")))

# 5.5 display number of comments for each group of sizes ranging from 1 - 10 characters
u_five.select(length("translated_review").alias("L")) \
        .groupBy("L").count() \
        .filter("L between 1 and 10") \
        .orderBy("L")\
        .show(10, False)

# 5.6 keep only rows where comment length is greater than or equal to 3
u_six = u_five.filter(length("translated_review") >= 3)

# 5.7 calculate 20 most frequent words in positive comments
top_twenty = (u_six.filter(col("sentiment")=="Positive")
              .rdd
              .flatMap(lambda r: r["translated_review"].split(" "))
              .map(lambda w: (w,1))
              .reduceByKey(lambda a,b: a+b)
              .takeOrdered(20, key=lambda x:-x[1]))
print("Top-20 positive words:", top_twenty)

users_clean = u_six

a = apps_clean.withColumn("last_updated", 
                          to_date(col("last_updated"), "MMMM d, yyyy"))

final_app = (
    a
    # clean reviews column, remove non-numeric characters
    .withColumn("reviews_clean", regexp_replace(col("reviews").cast("string"), r"[^\d]", ""))
    .withColumn("reviews_clean", when(col("reviews_clean") == "", "0").otherwise(col("reviews_clean")))
    .withColumn("reviews", col("reviews_clean").cast(IntegerType()))
    .drop("reviews_clean")
    # clean installs column
    .withColumn("installs",
        regexp_replace(col("installs"), "[^0-9]", "").cast(IntegerType())
    )
    # clean price column, handle corrupted characters
    .withColumn("price_tmp",
        regexp_replace(col("price").cast("string"), "[^0-9\\.]", "")
    )
    .withColumn("price_tmp", when(col("price_tmp") == "", "0").otherwise(col("price_tmp")))
    .withColumn("price", col("price_tmp").cast(DoubleType()))
    .na.fill({"price": 0.0})
    .drop("price_tmp")
    # clean rating column, make sure there are no corrupted values
    .withColumn("rating_clean", regexp_replace(col("rating").cast("string"), r"[^\d\.\-]", ""))
    .withColumn("rating_clean", when(col("rating_clean") == "", str(median_rating)).otherwise(col("rating_clean")))
    .withColumn("rating", col("rating_clean").cast(DoubleType()))
    .drop("rating_clean")
)

# clean users_clean numeric columns before saving
users_clean_final = (users_clean
    # ensure sentiment_polarity and sentiment_subjectivity are properly cleaned
    .withColumn("sentiment_polarity", 
               when(col("sentiment_polarity").isNull(), 0.0).otherwise(col("sentiment_polarity")))
    .withColumn("sentiment_subjectivity", 
               when(col("sentiment_subjectivity").isNull(), 0.0).otherwise(col("sentiment_subjectivity")))
)

# verify cleaning
print("Sample of final_app data:")
final_app.select("rating", "reviews", "price").show(5)
print("Sample of users_clean_final data:")
users_clean_final.select("sentiment_polarity", "sentiment_subjectivity").show(5)

# load into MySQL
try:
    final_app.write \
        .mode("overwrite") \
        .format("jdbc") \
        .option("url",      "jdbc:mysql://localhost:3306/database") \
        .option("dbtable",  "gps_app") \
        .option("user",     "user") \
        .option("password", "password") \
        .save()
    print("Successfully saved final_app to MySQL")
except Exception as e:
    print(f"Error saving final_app: {e}")

try:
    users_clean_final.write \
        .mode("overwrite") \
        .format("jdbc") \
        .option("url",      "jdbc:mysql://localhost:3306/database") \
        .option("dbtable",  "gps_user") \
        .option("user",     "user") \
        .option("password", "password") \
        .save()
    print("Successfully saved users_clean to MySQL")
except Exception as e:
    print(f"Error saving users_clean: {e}")
