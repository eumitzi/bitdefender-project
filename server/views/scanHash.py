from flask import Blueprint

scan_hash = Blueprint('scan_hash', __name__)



@scan_hash.route('/scanHash',methods=["POST", "GET"])
def scanHash():
    return "dummy"