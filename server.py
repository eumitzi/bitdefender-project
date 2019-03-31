from flask import Flask, request
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/mongo-practice"
mongo = PyMongo(app)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route("/scan", methods=["GET"])
def queryDb():

    fromClient = request.args["md5"]

    data = mongo.db.files.find_one({"md5": fromClient})
    
    print(data)
    print(request)
    return "scanned"