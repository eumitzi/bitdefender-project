import argparse
import client_program
from tqdm import tqdm
from termcolor import colored
import os

parser = argparse.ArgumentParser()

parser.add_argument("files", nargs='+',
                    help="display a square of a given number")
parser.add_argument("-s", "--scanHash", help="scans the database for the file \
                    hashes", action="store_true")
parser.add_argument("-b", "--scanBuff", help="takes vital info from the files and \
                    checks it", action="store_true")
parser.add_argument("-c", "--clean", help="disinfects the files", action="store_true")


args = parser.parse_args()

files_and_dirs = args.files


def get_files(files_dirs):
    answer = []

    for i in files_dirs:
        if os.path.isfile(i):
            answer.append(i)
        else:
            answer.extend(
                get_files(
                    map(lambda x: i + '/' + x,
                        os.listdir(i))))

    return answer


files = get_files(files_and_dirs)
# {items: [{file: '', status: ''}...]}
#
# def get_files(dir_list):
#
#
# files = get_files(files_and_dirs)


def print_one_two_three(answer):
    items = answer['items']
    for ans in items:
        if ans['status'] == 'clean':
            print(colored(ans['file'], 'blue'), 'is', colored(ans['status'], 'green'))
        elif ans['status'] == 'malware':
            print(colored(ans['file'], 'blue'), 'is', colored(ans['status'], 'red'))
        elif ans['status'] == 'failed':
            print(colored(ans['file'], 'blue'), colored(ans['status'], 'red'))
        elif ans['status'] == 'succeded':
            print(colored(ans['file'], 'blue'), colored(ans['status'], 'yellow'))
        else:
            print(colored(ans['file'], 'blue'), 'is', colored(ans['status'], 'grey'))


if (args.scanHash + args.scanBuff + args.clean) >= 2:
    parser.error('Too many options provided. Please specify at most one.')


def scanH(files):
    answer = client_program.stage_one(files)
    print_one_two_three(answer)
    return answer


if args.scanHash:
    scanH(files)


def scanB(files):
    answer = client_program.stage_two(files)
    if answer == 'failed':
        print("Stage 2 failed, please contact BitDefender")
    else:
        print_one_two_three(answer)

    return answer


if args.scanBuff:
    scanB(files)


def clean(files):
    no_of_files = len(files)
    files_done = 0
    answer = {'items': []}
    for file_number in tqdm(range(no_of_files)):
        status = client_program.stage_three(files[file_number])
        if status == 'failed':
            print("Stage 3 failed for file "
                  + files[file_number] +
                  ", please contact BitDefender")
        else:
            answer['items'].append({'file': files[file_number], 'status': status})
    print("Finished.")
    print_one_two_three(answer)

    return answer


if args.clean:
    clean(files)


def main_path(files):
    print("Starting Stage I")
    answer_one = scanH(files)

    files_two = []
    files_three = []

    for file in answer_one['items']:
        if file['status'] == 'more_data':
            files_two.append(file['file'])
        elif file['status'] == 'malware':
            files_three.append(file['file'])

    print("\n")
    print("Starting Stage II")
    if len(files_two) > 0:
        answer_two = scanB(files_two)

        for file in answer_two['items']:
            if file['status'] == 'malware':
                files_three.append(file['file'])

    print("\n")
    print("Starting Stage III")

    if len(files_three) > 0:
        answer_three = clean(files_three)


if (not args.scanHash) and (not args.scanBuff) and (not args.clean):
    main_path(files)
