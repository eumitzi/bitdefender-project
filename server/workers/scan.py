import json

def detect(det):

    buffer = det['buffers']
    response = []
    expected_sections=['.text','.data','.rsrc']
    section_name=''

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
              section_name=sec['n']
              break
            else:
                sectionCount=sectionCount+1

        if sectionCount==int(NumberOfSections, 16) and section_name not in expected_sections:
            status='malware'
        else:

            status='clean'

        item = {'md5': md5, 'status': status}
        response.append(item)

    return response


