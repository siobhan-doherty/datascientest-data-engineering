from pymongo import MongoClient
from pprint import pprint
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
    host="127.0.0.1",
    port = 27017,
    username = MONGO_USERNAME,
    password = MONGO_PASSWORD,
    authSource="admin"
)
sample = client["sample"]
books = sample["books"]

# list of available databases
pprint(client.list_database_names())

# list of collections available in this database
pprint(sample.list_collection_names())

# one of the documents in this collection
pprint(books.find_one())

# number of documents in this collection
pprint(books.count_documents({}))

# number of books with more than 400 pages
pprint(books.count_documents({"pageCount": {"$gt": 400}}))

# number of books with more than 400 pages AND are published.
pprint(books.count_documents({
    "pageCount": {"$gt": 400},
    "status": "PUBLISH"
}))

# number of books with keyword Android in description (short or long)
pprint(books.count_documents({
    "$or": [
        {"shortDescription": {"$regex": "Android", "$options": "i"}},
        {"longDescription": {"$regex": "Android", "$options": "i"}}
    ]
}))

# 2 distinct category lists (depending of the index 0 and 1)
category_pipeline = [
    {"$group": {
        "_id": None,
        "cat0": {"$addToSet": {"$arrayElemAt": ["$categories", 0]}},
        "cat1": {"$addToSet": {"$arrayElemAt": ["$categories", 1]}},
    }}
]
pprint(list(books.aggregate(category_pipeline)))

# number of books containing Python, Java, C++, Scala
regex = "|".join(["Python","Java","C\\+\\+","Scala"])
pprint(books.count_documents({
    "longDescription": {"$regex": regex, "$options": "i"}
}))

# statistical information about database
stats_pipeline = [
    {"$unwind": "$categories"},
    {"$group": {
        "_id": "$categories",
        "min": {"$min": "$pageCount"},
        "max": {"$max": "$pageCount"},
        "avg": {"$avg": "$pageCount"}
    }}
]
pprint(list(books.aggregate(stats_pipeline)))

# extract info from year, month, day for post-2009 & display first 20
date_pipeline = [
    {"$project": {
        "title": 1,
        "when": {"$toDate": {"$getField": {
            "field": "date",
            "input": "$publishedDate"
        }}},
        "year": {"$year": "$when"},
        "month": {"$month": "$when"},
        "day": {"$dayOfMonth": "$when"}
    }},
    {"$match": {"year": {"$gt": 2009}}},
    {"$limit": 20}
]
pprint(list(books.aggregate(date_pipeline)))

# display first 20 list of authors in chronological order
authors_pipeline = [
    {"$project": {
        **{ f"author_{i + 1}": {"$arrayElemAt": ["$authors", i]}
            for i in range(10) }
    }},
    {"$limit": 20}
]
pprint(list(books.aggregate(authors_pipeline)))

# top 10 most prolific authors by number of articles
top_authors_pipeline = [
    {"$project": {"firstAuthor": {"$arrayElemAt": ["$authors", 0]}}},
    {"$group": {"_id": "$firstAuthor", "count": {"$sum": 1}}},
    {"$sort": {"count": -1}},
    {"$limit": 10}
]
pprint(list(books.aggregate(top_authors_pipeline)))
