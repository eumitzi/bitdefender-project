import argparse
import client_program
from tqdm import tqdm
from termcolor import colored

parser = argparse.ArgumentParser()

parser.add_argument("files", nargs='+',
                    help="display a square of a given number")
parser.add_argument("-s", "--scanHash", help="scans the database for the file \
                    hashes", action="store_true")
parser.add_argument("-b", "--scanBuff", help="takes vital info from the files and \
                    checks it", action="store_true")
parser.add_argument("-c", "--clean", help="disinfects the files", action="store_true")


args = parser.parse_args()


#{items: [{file: '', status: ''}...]}

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


if (not args.scanHash) and (not args.scanBuff) and (not args.clean):
    parser.error('No options provided. Please specify exaclty one.')


if (args.scanHash + args.scanBuff + args.clean) >= 2:
    parser.error('Too many options provided. Please specify exactly one.')


if args.scanHash:
    answer = client_program.stage_one(args.files)
    print_one_two_three(answer)


if args.scanBuff:
    answer = client_program.stage_two(args.files)
    if answer == 'failed':
        print("Stage 2 failed, please contact BitDefender")
    else:
        print_one_two_three(answer)


if args.clean:
    no_of_files = len(args.files)
    files_done = 0
    answer = {}
    answer['items'] = []
    for file_number in tqdm(range(no_of_files)):
        status = client_program.stage_three(args.files[file_number])
        if status == 'failed':
            print("Stage 3 failed, please contact BitDefender")
        else:
            answer['items'].append({'file': args.files[file_number], 'status': status})
    print("Finished.")
    print_one_two_three(answer)
