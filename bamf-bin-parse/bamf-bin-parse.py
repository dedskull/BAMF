#!/usr/bin/env python
import modules
import modules.common
import json


def print_help():
    print("usage: bamf-bin-parse.py [-h] binary [binary] [...]")
    print("")
    print("Bot binary parsing and identification tool")
    print("Identifies and extracts information from bots")
    print("By Brian Wallace (@botnet_hunter)")
    print("")
    print("  binary                        Bot file")
    print("  -h --help                     Print this message")
    print("")

if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser(add_help=False)
    parser.add_argument('file', metavar='file', type=str, nargs='+', default=None)
    parser.add_argument('-h', '--help', default=False, required=False, action='store_true')
    parser.add_argument('-v', '--verbose', default=False, required=False, action='store_true')

    args = parser.parse_args()

    if args.help or args.file is None:
        print_help()
        exit()

    results = {}

    for file_name in args.file:
        with open(file_name, mode='rb') as file_handle:
            fileContent = file_handle.read()
            for m in modules.common.Modules.list:
                if m.is_bot(fileContent):
                    #print "%s matches %s" % (file_name, m.get_name())
                    results[file_name] = {}
                    results[file_name]["information"] = m.get_bot_information(fileContent)
                    results[file_name]["type"] = m.get_name()

    print json.dumps(results, sort_keys=True, indent=4, separators=(',', ': '))