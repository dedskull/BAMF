#!/usr/bin/env python
import bamfdetect
import json


if __name__ == "__main__":
    from argparse import ArgumentParser, RawDescriptionHelpFormatter
    parser = ArgumentParser(
        prog=__file__,
        description="Identifies and extracts information from bots",
        epilog="v%s by Brian Wallace (@botnet_hunter)" % bamfdetect.get_version()
    )
    parser.add_argument('path', metavar='path', type=str, nargs='+', default=None,
                        help="Paths to files or directories to scan")
    parser.add_argument('-d', '--detect', default=False, required=False, action='store_true', help="Only detect files")
    parser.add_argument('-r', '--recursive', default=False, required=False, action='store_true',
                        help="Scan paths recursively")

    args = parser.parse_args()

    if args.help or args.path is None:
        print_help()
        exit()

    results = bamfdetect.scan_paths(args.path, args.detect, args.recursive)

    print json.dumps(results, sort_keys=True, indent=4, separators=(',', ': '))