import os
from dotenv import load_dotenv
from pymongo import MongoClient
#from bson.objectid import ObjectId
import pprint
import pandas as pd

load_dotenv()

MONGODB_URI = os.environ["MONGODB_URI"]

client = MongoClient(MONGODB_URI)

db = client.LearnMongo

stock_data = db.Collec1

# TO DO - USE AGGREGATE FUNCTIONS AND BUILD COMPLEX QUERIES
## Getting top 3 scrips by sector which have:
#  PE ratio > 0 and < 1   ||   PB ratio > 0 and < 1   ||   Market cap > 0   ||   sorted by Open price

projection = {"$project":{"SECTOR":1,"_id":0}}
documents_to_find = {"$match":{"PE":{"$gt":0,"$lt":1},"PB":{"$gt":0,"$lt":1},"Mcap Full in Crores":{"$gt":0}}}
group_by = {"$group":{"_id":"$SECTOR","count":{"$sum":1}}}
cursor = stock_data.aggregate([documents_to_find, group_by])
#cursor = stock_data.aggregate([projection, group_by])

num_of_groups = 0
for group1 in cursor:
    print (group1)
    num_of_groups += 1

print ("total number of groups", num_of_groups)
#cursor = stock_data.aggregate({"$match":documents_to_find},
#                               documents_to_find,{"SCRIP NAME": 1, "_id": 0, "Mcap Full in Crores": 1, "Open": 1, "Turnover in Crores": 1}).sort("Open")
client.close()

exit()

## Getting scrips which have:
#  PE ratio > 0 and < 1   ||   PB ratio > 0 and < 1   ||   Market cap > 0   ||   sorted by Open price
documents_to_find = {"PE":{"$gt":0,"$lt":1},"PB":{"$gt":0,"$lt":1},"Mcap Full in Crores":{"$gt":0}}
cursor = stock_data.find(documents_to_find,{"SCRIP NAME": 1, "_id": 0, "Mcap Full in Crores": 1, "Open": 1, "Turnover in Crores": 1}).sort("Open")

list1 = []
for doc in cursor:
    list1.append(doc)

df = pd.DataFrame(list1)
print (df)

client.close()

exit()