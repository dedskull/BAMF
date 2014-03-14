#!/usr/bin/env python
import bamfdetect.modules
import bamfdetect.modules.common
import json
from os import listdir
from os.path import isfile, isdir, join, abspath


def print_help():
    print("usage: bamfdetect.py [-h] file or folder [file or folder] [...]")
    print("")
    print("Bot binary parsing and identification tool")
    print("Identifies and extracts information from bots")
    print("By Brian Wallace (@botnet_hunter)")
    print("")
    print("  binary                        Bot file")
    print("")
    print("  -r --recursive                Search recursively")
    print("  -d --detect                   Just detect bots, don't get configuration data")
    print("")
    print("  -h --help                     Print this message")
    print("")

if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser(add_help=False)
    parser.add_argument('file', metavar='file', type=str, nargs='+', default=None)
    parser.add_argument('-h', '--help', default=False, required=False, action='store_true')
    parser.add_argument('-d', '--detect', default=False, required=False, action='store_true')
    parser.add_argument('-r', '--recursive', default=False, required=False, action='store_true')

    args = parser.parse_args()

    if args.help or args.file is None:
        print_help()
        exit()

    results = {}
    paths = args.file

    while len(paths) != 0:
        path = abspath(paths[0])
        del paths[0]
        if isfile(path):
            with open(path, mode='rb') as file_handle:
                file_content = file_handle.read()
                for m in bamfdetect.modules.common.Modules.list:
                    if m.is_bot(file_content):
                        results[path] = {}
                        if not args.detect:
                            results[path]["information"] = m.get_bot_information(file_content)
                        results[path]["type"] = m.get_name()
        elif isdir(path):
            for p in listdir(path):
                p = join(path, p)
                if isfile(p) or (isdir(p) and args.recursive):
                    paths.append(p)

    print json.dumps(results, sort_keys=True, indent=4, separators=(',', ': '))