from flask import Blueprint
from flask import request
from . import DB
import json
scan_hash = Blueprint('scan_hash', __name__)


@scan_hash.route('/scanHash',methods=["POST", "GET"])
def scanHash():
    statusList = {}
    response = []

    data = request.get_json()
    hashes = data['md5']

    #id_client = data['id_client']

    base_Coll = DB.getBaseColl()

    for md5 in hashes:
        hash = base_Coll.find_one({"md5": md5})
        if hash:
            statusList[md5] = hash['status']
        else:
            statusList[md5] = 'more_data'

    for md5, status in statusList.items():
        response.append({'md5':md5,'status':status})

    response=json.dumps(response)
    return response

