#exception thrown
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
from pymongo import MongoClient
from rq import Queue

import redis
import os
import json
import time
import gridfs

client = MongoClient("mongodb://localhost:27017")
#connect to the db
db = client.filesDB
#get the files collection 
files = db["files"]

grid_fs = gridfs.GridFS(db)

r = redis.Redis()
q = Queue(connection=r)

# add extension for binaries - maybe.exe ??
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'old'])

app = Flask(__name__)

#Get more_data from each file
def create_file_header(file):
    fh = {}
    fh['ns'] = file.FILE_HEADER.NumberOfSections
    fh['c']  = file.FILE_HEADER.Characteristics
    return fh

def create_optional_header(file):
    oh = {}
    oh['m']  = file.OPTIONAL_HEADER.Magic
    oh['ep'] = file.OPTIONAL_HEADER.AddressOfEntryPoint
    return oh

def create_sections(file):
    sect_arr = []
    for section in file.sections:
        new_section = {}

        sectionName = section.Name[:section.Name.index(0)]
        new_section['n']    = sectionName.decode("utf-8")
        new_section['va']   = hex(section.VirtualAddress)
        new_section['size'] = hex(section.SizeOfRawData)
        new_section['c']    = hex(section.Characteristics)
        sect_arr.append(new_section)
    return sect_arr

def create_json(file):

    dict = {}
    dict['md5'] = 'md5 pe intreg fisierul'
    dict['fh']  = create_file_header(file)
    dict['oh']  = create_optional_header(file)
    dict['sec'] = create_sections(file)
    
    #print(dict)
    #return dict
    return json.dumps(dict)

#TO DO: create tasks.py containing all bg tasks

def background_task(file):

    """ upload to gridfs the important data and simulate a delay """

    print("Task running")
    
    # not working
    # cannot serialize '_io.BufferedRandom' object
    pe_file = pefile.PE(file)

    delay = 2

    print(f"Simulating a {delay} second delay")

    time.sleep(delay)

    data = create_json(pe_file)

    file_name = secure_filename(file.filename)

    with grid_fs.new_file(filename=file_name) as fp:
        # do not write the file to gridfs
        # write buffer / important data to gridfs
        fp.write(file)

    print("Task completed")

    return data

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploadFile', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':    
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            
            # Exception: cannot serialize '_io.BufferedRandom' object
            job = q.enqueue(background_task, file)

            return f"Task ({job.id}) added to queue at {job.enqueued_at}"
        else:
            return "No value for count provided"
    return "<!doctype html><title>Upload new File</title><h1>Upload new File</h1><form method=post enctype=multipart/form-data><p><input type=file name=file><input type=submit value=Upload></form>"
    
