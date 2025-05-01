from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import requests
import pymongo

# load secrets from .env file
load_dotenv()
MONGO_USERNAME = os.getenv("MONGO_USERNAME")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
WEATHER_KEY  = os.getenv("WEATHER_KEY")

# validate
if not (MONGO_USERNAME and MONGO_PASSWORD and WEATHER_KEY):
    raise RuntimeError("Ensure MONGO_USERNAME, MONGO_PASSWORD, and WEATHER_KEY are set in .env")

# connect to MongoDB
client = MongoClient(
    host = "127.0.0.1",
    port = 27017,
    username = MONGO_USERNAME,
    password = MONGO_PASSWORD
)
db = client["sample"]

# get or create weather collection
try:
    weather_col = db.create_collection("weather")
except pymongo.errors.CollectionInvalid:
    weather_col = db["weather"]

# fetch weather
CITY = "COURBEVOIE"
url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={WEATHER_KEY}"

response = requests.get(url)
response.raise_for_status()
data = response.json()

# clean and prep data
clean_data = {i: data[i] for i in ["weather", "main"]}
clean_data["weather"] = clean_data["weather"][0]

# add city and time to clean_data
clean_data["time"] = datetime.now().strftime("%H:%M:%S")
clean_data["city"] = CITY

# insert into mongoDB
final_data = weather_col.insert_one(clean_data)
print("Inserted:", final_data.inserted_id)

# insert list of multiple cities
def fetch_and_clean(city: str) -> dict:
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_KEY}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    clean_data = {i: data[i] for i in ["weather", "main"]}
    clean_data["weather"] = clean_data["weather"][0]
    # add city and time to clean_data
    clean_data["time"] = datetime.now().strftime("%H:%M:%S")
    clean_data["city"] = city
    return clean_data


cities = ["courbevoie", "puteaux", "lourdes", "bourg-la-reine"]
for city in cities:
    data = fetch_and_clean(city)
    weather_col.insert_one(data)

print(f"Inserted extra {len(cities)} cities.")

# find all data where weather.main is set to Clear, show the city only
print("\nCities with Clear weather:")
col = client["sample"]["weather"]
for i in list(col.find({"weather.main": "Clear"}, {"_id": 0, "city": 1})):
    print(i)

# count data where 289 ≤ temp_min ≤ temp_max ≤ 291
col = client["sample"]["weather"]
count_via_list = len(
    list(
        col.find(
            {
                "$and": [
                    {"main.temp_min": {"$gte": 287}},
                    {"main.temp_max": {"$lte": 291}},
                ]
            }
        )
    )
)
print("Temperature range list:", count_via_list) 
    
count_via_cd = col.count_documents(
    {
        "$and": [
            {"main.temp_min": {"$gte": 287}},
            {"main.temp_max": {"$lte": 291}},
        ]
    }
)
print("We can use also the count_documents function : ", count_via_cd)

count_implicit = col.count_documents(
    {"main.temp_min": {"$gte": 287}, "main.temp_max": {"$lte": 291}},
)
print("With the implicit AND ", count_implicit)

# aggregation of data per weather.main
print("\nNumber of documents by weather.main:")
col = client["sample"]["weather"]
for i in list(col.aggregate([{"$group": {"_id": "$weather.main", "nb": {"$sum": 1}}}])):
    print(i)
