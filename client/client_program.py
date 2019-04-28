import requests
import hashlib
import pefile
import json
import os

with open('config.json') as config_file:
    data = json.load(config_file)

ID_CLIENT = data['DEFAULT']['ID_CLIENT']
SERVER_LINK = data['DEFAULT']['SERVER_LINK']

answer = {}
answer['items'] = []

# {items: [{file:, status:}...]}


def stage_one(files):
    items = {}
    items['id_client'] = ID_CLIENT
    files_md5 = []
    
    files_to_md5 = {}

    for i in files:
        with open(i, "rb") as file:
            files_md5.append(hashlib.md5(file.read()).hexdigest())
            files_to_md5[files_md5[-1]] = i

    items['hash'] = files_md5

    for ans in requests.post(SERVER_LINK + 'scanHash', json=items).json()['result']:
        answer['items'].append({'file': files_to_md5[ans['md5']],
                                'status': ans['status']})

    return answer


def wait_for_buffer_answer(job_id):
    
    response = requests.get(SERVER_LINK + 'scanBuffer/' + job_id).json();
    
    while response['status'] != 'ready':
        time.sleep(2)
        response = requests.get(SERVER_LINK + 'scanBuffer/' + job_id).json();

    return response


def stage_two(files):
    #check job until ready
    #return answer

    items = {}
    items['id_client'] = ID_CLIENT
    items['buffers'] = []

    files_to_md5 = {}

    for file in files:
        item = {}

        with open(file, "rb") as file:
            item["md5"] = hashlib.md5(file.read()).hexdigest()
            files_to_md5[item['md5']] = file

        pe = pefile.PE(file)
        sec = []

        for i in pe.sections:
            section = {"n": i.Name[:i.Name.index(b'\0')].decode("utf-8"), 'sa': hex(i.VirtualAddress),
                       's': hex(i.SizeOfRawData), 'c': hex(i.Characteristics)}
            sec.append(section)

        item["fh"] = {"ns": hex(pe.FILE_HEADER.NumberOfSections),
                      "c": hex(pe.FILE_HEADER.Characteristics)}
        item["oh"] = {"m": hex(pe.OPTIONAL_HEADER.Magic),
                      "ep": hex(pe.OPTIONAL_HEADER.AddressOfEntryPoint)}
        item["sec"] = sec

        items["buffers"].append(item)

    job_id = requests.post(SERVER_LINK + 'scanBuffer', json=items).json()['id']
    
    job_json = wait_for_buffer_answer(job_id)

    for ans in job_json['result']:
        answer['items'].append({'file': files_to_md5[ans['md5']],
                                'status': ans['status']})

    return answer


def wait_for_buffer_answer(job_id):
    
    response = requests.get(SERVER_LINK + 'uploadFile/' + job_id).json();
    
    while response['status'] != 'ready':
        time.sleep(2)
        response = requests.get(SERVER_LINK + 'uploadFile/' + job_id).json();

    return response


def stage_three(file):
    
    with open(file, "rb") as hfile:
        old_md5 = hashlib.md5(hfile.read()).hexdigest()

    upload_files = {'file': open(file, 'rb')}
    r = requests.post(SERVER_LINK + 'uploadFile/' + old_md5, files=upload_files)    

    job_json = wait_for_upload_answer(r.json()['jobID'])
    
    if job_json['result']['status'] == 'clean':
        new_md5 = job_json['result']['md5_clean']
        os.remove(file)

        with requests.get(SERVER_LINK + 'downloadFile/' + new_md5, stream=True) as r:
            r.raise_for_status()
            with open(file, 'wb') as f: #nu stiu daca mai merge ???
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

    return job_json['result']['status']
