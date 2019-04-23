from flask import Blueprint

scan_buffer = Blueprint('scan_buffer', __name__)

@scan_buffer.route('/scanBuffer',methods=["POST", "GET"])
def scanBuffer():
    return "dummy from scanBuffer"