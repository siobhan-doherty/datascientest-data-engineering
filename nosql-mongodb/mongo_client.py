from pymongo import MongoClient
from dotenv import load_dotenv
import os


# load secrets from .env file
load_dotenv()
MONGO_USERNAME = os.getenv("MONGO_USERNAME")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")

# validate
if not (MONGO_USERNAME and MONGO_PASSWORD):
    raise RuntimeError("Ensure MONGO_USERNAME and MONGO_PASSWORD are set in .env")

client = MongoClient(
    host = "127.0.0.1",
    port = 27017,
    username = MONGO_USERNAME,
    password = MONGO_PASSWORD
)

print(client.list_database_names())

sample = client["sample"]
c_zips = sample["zips"]

print(c_zips.find_one())
