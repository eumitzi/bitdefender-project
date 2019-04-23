from flask import Blueprint

upload_file = Blueprint('upload_file', __name__)



@upload_file.route('/uploadFile',methods=["POST", "GET"])
def uploadFile():
    return "dummy from upload file"