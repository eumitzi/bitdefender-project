from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
from datetime import datetime
import gridfs

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://localhost:27017")
#connect to the db
db = client.filesDB
#get the files collection 
files = db["fs.files"]

fs = gridfs.GridFS(db)

#logging function
def logToDB(scannedMd5, status):
    currentTime = datetime.now()
    db.log.insert_one({"timestamp": currentTime, "scanned": scannedMd5, "result": status})


#Upload the file
class Scan(Resource):
    def get(self):
       clientStatus = request.args["status"]
       clientMd5    = request.args["md5"]
       if clientStatus == "more_data": 
           fs.put(b"data2", md5=clientMd5, status=clientStatus)
           logToDB(clientMd5, clientStatus)       
       return "scanned"

#Download the file
class Download(Resource):
    def get(self):
        clientMd5 = request.args["md5"]
        for grid_data in fs.find({"md5": clientMd5}):
            data = grid_data.read()
      # print(data)
        return "downloaded"

api.add_resource(Scan, '/scan')
api.add_resource(Download, '/download')

if __name__=="__main__":
    app.run(host='127.0.0.0')

