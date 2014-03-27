#!/usr/bin/env python
import bamfbrute
import json


if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser(
        prog=__file__,
        description="Brute forces credentials to botnet panels",
        epilog="v%s by Brian Wallace (@botnet_hunter)" % bamfbrute.get_version()
    )
    parser.add_argument('-l', '--list', default=False, required=False, action='store_true',
                        help='List available modules')

    args = parser.parse_args()

    if args.list:
        for mod in bamfbrute.get_loaded_modules():
            print mod
    else:
        if None is None:
            parser.print_help()
            exit()
