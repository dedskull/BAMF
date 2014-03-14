#!/usr/bin/env python
import bamfdetect
import json


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

    results = bamfdetect.scan_paths(args.file, args.detect, args.recursive)

    print json.dumps(results, sort_keys=True, indent=4, separators=(',', ': '))