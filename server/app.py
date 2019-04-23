from flask import Flask
from views.scanHash import scan_hash
from views.scanBuffer import scan_buffer
from views.uploadFile import upload_file

app = Flask(__name__)
app.register_blueprint(scan_hash)
app.register_blueprint(scan_buffer)
app.register_blueprint(upload_file)

# from flask import Flask
# from pymongo import MongoClient

# def main():
#     app=FLask(__name__)
#     mongoClient= MongoClient("mongodb://localhost:27017")
#     db = mongoClient.bitDef
#     base_Coll=db["files"]
#     app.run(debug=True)


# if __name__=='__main__':
#     main()