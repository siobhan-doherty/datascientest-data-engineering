from pymongo import MongoClient
from pprint import pprint
from dotenv import load_dotenv
import os
import json


# load secrets from .env file
load_dotenv()
MONGO_USERNAME = os.getenv("MONGO_USERNAME")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")

# validate
if not (MONGO_USERNAME and MONGO_PASSWORD):
    raise RuntimeError("Ensure MONGO_USERNAME and MONGO_PASSWORD are set in .env")

client = MongoClient(
    host="127.0.0.1",
    port = 27017,
    username = MONGO_USERNAME,
    password = MONGO_PASSWORD,
    authSource="admin"
)
books_column = client["sample"]["books"]
books_column.drop()

with open("imports/books.json", "r") as f:
    data = [json.loads(line) for line in f if line.strip()]

for d in data:
    d.pop("_id", None)

result = books_column.insert_many(data)
print(f"Imported {len(result.inserted_ids)} books.")
