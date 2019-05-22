from pymongo import MongoClient
import pefile
import gridfs
import hashlib

client = MongoClient("mongodb://localhost:27017")
#connect to the files db
db = client.filesDB

grid_fs = gridfs.GridFS(db)


def start_cleanup(md5):

	# step 1 - get file from gridfs
	grid_fs_file = grid_fs.find_one({"md5": md5}, no_cursor_timeout=True) # type GridOut
	
	# step 2 - clean
	byte_data = grid_fs_file.read(size=grid_fs_file.length) # byte 
	str_data  = byte_data.decode("utf-8", "ignore") # str - actually not needed 
	
	pe = pefile.PE(data=byte_data, fast_load=True) 
	
	print(pe.sections[0].Name.decode('utf-8'))
	
	# change the virtual address of the .text section
	pe.sections[0].VirtualAddress = 1100
	print(pe.sections[0].VirtualAddress)
		
	# step 3 - insert file in bd
	with grid_fs.new_file(filename=grid_fs_file.filename) as fp:
                fp.write(pe.dump_info().encode())
	
	# step 4 - compute md5 clean file
	md5_clean_file = hashlib.md5(pe.dump_info().encode()).hexdigest()
	
	result = {}
	# step 5 return job result, md5 clean file
	if md5_clean_file:
		
		result['md5'] = md5_clean_file
		
		return result
	else:
		return "wait a second"
