import json
def detect(det):

    buffer = det['buffers']
    response = []

    for file in buffer:
        entryPoint=file['oh']['ep']
        sectionCount=0
        NumberOfSections=file['fh']['ns']
        md5=file['md5']

        for sec in file['sec']:
            virtualAdress=sec['va']
            sizeOfRawData=sec['s']
            if(entryPoint< virtualAdress+sizeOfRawData):
              #Todo: do something
              break
            else:
                sectionCount=sectionCount+1

        if sectionCount==NumberOfSections:
            print("infected")
            status='infected'

        else:
            status='clean'
            print("clean")

        item = {'md5': md5, 'status': status}
        response.append(item)

    response = json.dumps(response)
    return response


