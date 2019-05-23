from flask import Blueprint, jsonify
from gridfs import GridFS
from pymongo import MongoClient

import gridfs

client = MongoClient("mongodb://localhost:27017")

db = client.filesDB

grid_fs = gridfs.GridFS(db)

download_file = Blueprint('download_file', __name__)

@download_file.route('/downloadFile/<md5>',methods=["GET"])
def downloadFile(md5):

   grid_fs_file = grid_fs.find_one({'md5': md5})

   response = {
      'status': 'ready',
      'result': {
         'md5': md5,
         'status': 'clean',
         'md5_clean': grid_fs_file.md5
      }
   }
   return jsonify(response)
