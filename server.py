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

class Scan(Resource):
    def get(self):
        fromClient = request.args["md5"]
        firstFile = files.find_one({"md5": fromClient})
        print(firstFile)
        return "scanned"

api.add_resource(Scan, '/scan')

if __name__=="__main__":
    app.run(host='127.0.0.0')

