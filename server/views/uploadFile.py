from flask import Blueprint, jsonify, request, redirect
from flask import flash
from workers import disinfect
from werkzeug.utils import secure_filename
from pymongo import MongoClient
from rq import Queue

import redis
import json
import time
import gridfs
import pefile
import hashlib

client = MongoClient("mongodb://localhost:27017")
#connect to the files db
db = client.filesDB

grid_fs = gridfs.GridFS(db)

#get the results collection 
results = db["jobResults"]

r = redis.Redis()
q = Queue(connection=r)

ALLOWED_EXTENSIONS = set(['exe', 'dll', 'scr', 'sys', 'iso']) 

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def compare_hashes(md5_client, md5_server):

    return md5_client == md5_server

upload_file = Blueprint('upload_file', __name__)    

@upload_file.route('/uploadFile/<md5>',methods=["POST"])
def uploadFile(md5):   
        
    if request.files:
        file_storage = request.files["file"]
        if allowed_file(file_storage.filename):
        
            file_name = secure_filename(file_storage.filename) 
            file_content = file_storage.stream.read()
            
            if not compare_hashes(md5, hashlib.md5(file_content).hexdigest()):
                return jsonify({"error": "incompatible hashes"}), 400     
            with grid_fs.new_file(filename=file_name) as fp:
               # fp.write(file_storage)
               fp.write(file_content)
            
        job = q.enqueue(disinfect.start_cleanup, md5)

        response = {
            'jobId': job.id,
            'error': False
        }
        return jsonify(response)
    else:
        return jsonify({"error": "Wrong format"}), 400


@upload_file.route('/uploadFile/<job_id>',methods=["GET"])
def check_job_id(job_id):

    job = Job.fetch(job_id, connection=r)
    
    resp = {}
    if job.get_status() == 'started':
        resp['status'] = 'pending'
    elif job.get_status() == 'failed':
        resp['status'] = 'failed'
    elif job.get_status() == 'finished':
        resp['status'] = 'ready'
        resp['result'] = job.result
    return resp
