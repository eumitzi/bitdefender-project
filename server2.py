import os
import json
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
from pymongo import MongoClient

import gridfs

client = MongoClient("mongodb://localhost:27017")
#connect to the db
db = client.filesDB
#get the files collection 
files = db["files"]

grid_fs = gridfs.GridFS(db)

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
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
            
            file_name = secure_filename(file.filename)
            
            with grid_fs.new_file(filename=file_name) as fp:
                # real working scenario: 
                # CALL FUNCTION TO GET THE IMPORTANT DATA FROM FILE
                # UPLOAD TO GRID FS ONLY THE IMPORTANT DATA, not the whole file
                # run this as a background job 
                fp.write(file)
                file_id = fp._id

            if grid_fs.find_one(file_id) is not None:
                return json.dumps({'status': 'File saved successfully'}), 200
            else:
                return json.dumps({'status': 'Error occurred while saving file.'}), 500
    return "<!doctype html><title>Upload new File</title><h1>Upload new File</h1><form method=post enctype=multipart/form-data><p><input type=file name=file><input type=submit value=Upload></form>"
    
