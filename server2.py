# not working yet

from flask import Flask, request
from flask_restful import Api, Resource
from pymongo import MongoClient
from datetime import datetime

import redis
from rq import Queue

import gridfs
import pefile
import json

app = Flask(__name__)

r = redis.Redis()
q = Queue(connection=r)

client = MongoClient("mongodb://localhost:27017")
#connect to the db
db = client.filesDB
#get the files collection 
files = db["files"]

grid_fs = gridfs.GridFS(db)

#Get more data from each file
def create_file_header(peClean):
    fh = {}
    fh['ns'] = peClean.FILE_HEADER.NumberOfSections
    fh['c']  = peClean.FILE_HEADER.Characteristics
    return fh

def create_optional_header(peClean):
    oh = {}
    oh['m']  = peClean.OPTIONAL_HEADER.Magic
    oh['ep'] = peClean.OPTIONAL_HEADER.AddressOfEntryPoint
    return oh

def create_sections(peClean):
    sect_arr = []
    for section in peClean.sections:
        new_section = {}

        sectionName = section.Name[:section.Name.index(0)]
        new_section['n']    = sectionName.decode("utf-8")
        new_section['va']   = hex(section.VirtualAddress)
        new_section['size'] = hex(section.SizeOfRawData)
        new_section['c']    = hex(section.Characteristics)
        sect_arr.append(new_section)
    return sect_arr

def createJson(file_to_upload):

        dict = {}
        dict['md5'] = 'md5 pe intreg fisierul'
        dict['fh']  = create_file_header(file_to_upload)
        dict['oh']  = create_optional_header(file_to_upload)
        dict['sec'] = create_sections(file_to_upload)
        
        print(dict)
        #return dict
        return json.dumps(dict)

#MAKE THIS WORK!!
#CREATE A FILE tasks.py and store all tasks there
'''
def upload_to_gridfs(file):
    with grid_fs.new_file(filename=file_name) as fp:
            fp.write(request.data)  # ??? call createJson() function to get all needed data for each file
            file_id = fp._id

        if grid_fs.find_one(file_id) is not None:
            return json.dumps({'status': 'File saved successfully'}), 200
        else:
            return json.dumps({'status': 'Error occurred while saving file.'}), 500 

            
'''

#Save info in gridfs
def background_task(files):

    delay = 2

    print("Task running...")
    # no need to simulate a delay later
    print(f"Simulating a {delay} second delay")

    # upload each file to gridfs
    upload_to_gridfs(file)
    
    #upload data to gridfs

    time.sleep(delay)

    print("Task complete!")

    return len(n)

#add files in URL with ?data="files to be inserted"	
@app.route("/task")
def index():

    if request.args.get("files"):

        job = q.enqueue(background_task, request.args.get("files"))

        return f"Task ({job.id}) added to queue at {job.enqueued_at}"

    return "No files provided"


if __name__=="__main__":
    app.run(host='127.0.0.0')
