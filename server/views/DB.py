from pymongo import MongoClient

def getBaseColl():
    mongoClient = MongoClient("mongodb://localhost:27017")
    db = mongoClient.bitDef
    base_Coll = db["files"]
    return base_Coll
