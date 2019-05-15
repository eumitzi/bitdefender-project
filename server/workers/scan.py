import json

def detect(det):

    buffer = det['buffers']
    response = []

    for file in buffer:
        entryPoint=file['oh']['ep']
        sectionCount=1
        NumberOfSections=file['fh']['ns']
        md5=file['md5']
        print(NumberOfSections)
        for sec in file['sec']:
            virtualAdress=sec['va']
            sizeOfRawData=sec['s']
            if(entryPoint< virtualAdress+sizeOfRawData):
              #Todo: do something
              break
            else:
                sectionCount=sectionCount+1

        if sectionCount==int(NumberOfSections, 16):
            status='malware'
        else:

            status='clean'

        item = {'md5': md5, 'status': status}
        response.append(item)

    return response


