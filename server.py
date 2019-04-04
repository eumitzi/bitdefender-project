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
files = db["files"]

fs = gridfs.GridFS(db)

#Logging function
def logToDB(scannedMd5, status):
    currentTime = datetime.now()
    db.log.insert_one({"timestamp": currentTime, "scanned": scannedMd5, "result": status})

#Upload the file
class Scan(Resource):
    def post(self):

        #Get posted data
        postedData = request.get_json()
        clientMd5 = postedData['md5']
        clientStatus = postedData['status']

        if clientStatus == "more_data": 
            retMap = {
                'message': 'Need more data about this file',
                'md5': clientMd5,
			    'status': clientStatus
		    	}
            fs.put(b"data2", md5=clientMd5, status=clientStatus)
            logToDB(clientMd5, clientStatus)
            return jsonify(retMap)	
		   
api.add_resource(Scan, "/scan")
if __name__=="__main__":
    app.run(host='127.0.0.0')
