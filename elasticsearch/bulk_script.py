#! /usr/bin/python
from elasticsearch import Elasticsearch, helpers
import csv


# connection to cluster
es = Elasticsearch(hosts = "http://localhost:9200", request_timeout = 120)

with open("EmployerReviews.csv", encoding = "utf-8") as f:
  reader = csv.DictReader(f)
  helpers.bulk(es, reader, index = "reviews", chunk_size = 5000, request_timeout = 120)
