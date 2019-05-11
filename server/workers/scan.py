import json
def detect(det):

    buffer = det['buffers']

    for file in buffer:
        entryPoint=file['oh']['ep']
        sectionCount=0
        NumberOfSections=file['fh']['ns']


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
        else:
            print("clean")

        #Todo: return json w/ result
        #Todo: check for name in a list of known sections ?


    return 1


