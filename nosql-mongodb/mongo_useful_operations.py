from pymongo import MongoClient
from pprint import pprint
from dotenv import load_dotenv
import re
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

zips = client["sample"]["zips"]
for i in list(zips.find({},{"_id":0,"city":1})):
    print(i)

zips = client["sample"]["zips"]
for i in list(zips.find({},{"_id":0,"city":1}).limit(12)):
    print(i)

zips = client["sample"]["zips"]
print(zips.find().distinct("state"))

pprint(client["sample"]["cie"].find_one())

exp = re.compile("^[0-9]*$")
pprint(list(zips.find({"city": exp}, {"city": 1})))

pprint(
    list(
        client["sample"]["cie"].aggregate(
            [
                {"$match": {"acquistions.company.name": "Tumblr"}},
                {"$project": {"_id": 1, "society": "$name"}}
            ]
        )
    )
)
