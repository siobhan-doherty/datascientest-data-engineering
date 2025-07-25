#! /usr/bin/python
from elasticsearch import Elasticsearch, helpers
import csv


# connection to cluster
es = Elasticsearch(hosts = "http://localhost:9200")

with open("cars.csv", encoding = "utf-8") as f:
  reader = csv.DictReader(f)
  helpers.bulk(es, reader, index = "cars")
