import os
import random
import hashlib
import pymongo

client = pymongo.MongoClient()
#please select your own db
db = client['practice']
#please select your own collection
collection = db['md5_uri']

current_dir = os.getcwd()
selection_one = ['downloader.', 'risker.', 'agent.', 'sniffer.', 'coinminer.']
selection_two = ['adson.', 'rammint.', 'zmist.', 'zeus.']


def get_random_race():
    return 'trojan.' + random.choice(selection_one) + random.choice(selection_two) + str(random.randint(400,9000))


with open("icardagt_malware.old", "rb") as mal:
    malwr_buffer = mal.read()

with open("icardagt_clean.old", "rb") as clean:
    clean_buffer = clean.read()


# populate trebuie sa creeze fisierul si apoi sa il puna in db
# db format : _id, sta


def populate_dir(dir, n):
    global clean_buffer
    global malwr_buffer

    for i in range(n):
        status = '?'
        my_hex = '?'
        race = '?'

        new_file = open(dir + '/' + str(i), "wb")

        if random.randint(0,1000) % 3 == 0:
            status = 'clean'
            clean_buffer += bytes(9)
            new_file.write(clean_buffer)
            new_file.close()
            my_hex = hashlib.md5(clean_buffer).hexdigest()
            race = 'clean'
        else:
            status = 'malware'
            malwr_buffer += bytes(9)
            new_file.write(malwr_buffer)
            new_file.close()
            my_hex = hashlib.md5(malwr_buffer).hexdigest()
            race = get_random_race()

        if random.randint(0,10) > 4:
            post = {'_id': my_hex, 'status': status, 'description': race}
            try:
                collection.insert_one(post)
            except:
                pass

def gen_dir(dir):
    os.mkdir(dir + '/sub_dir_one')
    os.mkdir(dir + '/sub_dir_two')
    return [dir + '/sub_dir_one', dir + '/sub_dir_two']


def gen_files(n, dir):
    directories = [dir]
    dir_to_generate_from = 0
    dir_to_populate = 0

    while n > 0:
        no_of_files = random.randint(5, 13)

        if n >= no_of_files:
            n -= no_of_files
        else:
            no_of_files = n
            n = 0

        populate_dir(directories[dir_to_populate], no_of_files)

        dir_to_populate += 1

        if dir_to_populate >= len(directories):
            directories.extend(gen_dir(directories[dir_to_generate_from]))
            dir_to_generate_from += 1


gen_files(1000, current_dir)
