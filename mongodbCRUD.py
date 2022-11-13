import os
from dotenv import load_dotenv
from pymongo import MongoClient
from bson.objectid import ObjectId
import pprint

load_dotenv()

MONGODB_URI = os.environ["MONGODB_URI"]
# connection string has been moved.
#    "mongodb+srv://test1:test1pw@cluster1.xkdoh.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(MONGODB_URI)

for db in client.list_database_names():
    print (db)

db = client.LearnMongo

stock_data = db.Collec1

############################################################################################ 7 deleting multiple documents
documents_to_delete = {"SECTOR": "testing mongo"}
pprint.pprint(stock_data.find_one(documents_to_delete))               # pprint document before delete
result = stock_data.delete_many(documents_to_delete)
pprint.pprint(stock_data.find_one(documents_to_delete))               # pprint document after delete
print ("# of rows deleted: " + str(result.deleted_count))
client.close()
exit()

############################################################################################ 7 deleting single document
document_to_delete = {"_id": ObjectId('637031ceaac9455ff74cd88f')}
pprint.pprint(stock_data.find_one(document_to_delete))               # pprint document before delete
result = stock_data.delete_one(document_to_delete)
pprint.pprint(stock_data.find_one(document_to_delete))               # pprint document after delete
print ("# of rows deleted: " + str(result.deleted_count))
client.close()
exit()

############################################################################################ 6 updating multiple documents
documents_to_update = {"SECTOR": "testing mongo"}
set_PE_ratio = {"$set":{"PE":10}}
result = stock_data.update_many(documents_to_update,set_PE_ratio)
print ("# of rows matched: " + str(result.matched_count))
print ("# of rows updated: " + str(result.modified_count))
pprint.pprint(stock_data.find_one(documents_to_update))
client.close()
exit()

############################################################################################ 5 updating single document
document_to_update = {"_id": ObjectId('636f9a6ed97bfaeb019f6098')}
add_to_PB_ratio = {"$inc":{"PB":1}}
pprint.pprint(stock_data.find_one(document_to_update))               # pprint document before update
result = stock_data.update_one(document_to_update,add_to_PB_ratio)
pprint.pprint(stock_data.find_one(document_to_update))               # pprint document after update
print ("# of rows updated: " + str(result.modified_count))
client.close()
exit()

############################################################################################ 4 selecting multiple documents
documents_to_find = {"SECTOR":{"$eq":"testing mongo"}}
cursor = stock_data.find(documents_to_find)
num_of_docs = 0
for doc in cursor:
    num_of_docs += 1
    pprint.pprint(doc)
print ("# of rows retrieved: " + str(num_of_docs))
client.close()
exit()

############################################################################################ 3 selecting one document
document_to_find = {"_id": ObjectId("636f9a6ed97bfaeb019f6098")}
result = stock_data.find_one(document_to_find)
pprint.pprint(result)
client.close()
exit()

############################################################################################ 2 inserting many documents
new_documents = [{
    "SCRIP NAME": "test document 1",
    "SECTOR": "testing mongo",
    "PE": 0
},
{
    "SCRIP NAME": "test document 2",
    "SECTOR": "testing mongo",
    "PE": 0,
    "PB": 1
}]

result = stock_data.insert_many(new_documents)

document_ids = result.inserted_ids
print ("# of inserted documents: ", str(len(document_ids)))
print (f"inserted document id's: {document_ids}")

client.close()

exit()

############################################################################################ 1 inserting one document:
new_document = {
    "SCRIP NAME": "test document",
    "SECTOR": "testing mongo",
    "PE": 0
}

result = stock_data.insert_one(new_document)

document_id = result.inserted_id
print ("inserted document: ", document_id)

client.close()