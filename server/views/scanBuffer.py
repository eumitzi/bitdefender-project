from flask import Blueprint, request
from . import DB
import json
from ..workers import scan

scan_buffer = Blueprint('scan_buffer', __name__)

base_Coll = DB.getBaseColl()

from rq.job import Job
from redis import Redis
from rq import Queue
redis_conn = Redis()
q = Queue(connection=redis_conn)

from flask import jsonify

@scan_buffer.route('/scanBuffer',methods=["POST"])
def scanBufferPost():

      data = request.get_json()
      #id_client = data['id_client']  # use id_client for logging
      job = q.enqueue(scan.detect,data)
      return jsonify({'id': job.id})

@scan_buffer.route('/scanBuffer/<path:id>', methods=["GET"])
def scanBufferGet(id):
   
    job2 = Job.fetch(id, connection=redis_conn)
    response = {}

    if job2.get_status() == 'started':
        response['status'] = 'pending'

    elif job2.get_status() == 'finished':
        response['status'] = 'ready'

            # for file in job2.result:
            #   base_Coll.insert_one({'md5': file['md5'], 'status': file['status']})


        response['result'] = job2.result

    elif job2.get_status() == 'failed':
        response['status'] = 'failed'

    return jsonify(response)



