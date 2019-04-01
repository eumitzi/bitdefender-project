from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://localhost:27017")
#connect to the db
db = client.test
#get the files collection 
files = db["files"]

#create logging function

#Upload the file
class Scan(Resource):

    #call logging file  

    def get(self):
        fromClient = request.args["md5"]
        firstFile = files.find_one({"md5": fromClient})
        print(firstFile)
        return "scanned"

#Download the file
class Download(Resource):
    def get(self):
        return "downloaded"

api.add_resource(Scan, '/scan')
api.add_resource(Download, '/download')

if __name__=="__main__":
    app.run(host='127.0.0.0')

