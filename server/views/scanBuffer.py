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



@scan_buffer.route('/scanBuffer',methods=["POST", "GET"])
def scanBuffer():

    if request.method == 'POST':
        data = request.get_json()
        #id_client = data['id_client']  # use id_client for logging
        job = q.enqueue(scan.detect,data)
        return job.id


    if request.method == 'GET':
        req = request.args.get('id_job')
        #id = req.split('=',0)
        id=req


        job2 = Job.fetch(id, connection=redis_conn)
        
        if job2.get_status() == 'started':
            return 'pending'
        elif job2.get_status() == 'finished':
            print(job2.result)

            # for file in job2.result:
            #   base_Coll.insert_one({'md5': file['md5'], 'status': file['status']})

            response = {'status': 'ready',
                        'result': []
                        }

            response['result'].append(job2.result)
            return json.dumps(response)


        elif job2.get_status() == 'failed':
            return 'failed'

    return "scanBuffer default"




