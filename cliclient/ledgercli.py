#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Ledger CLI
'''

import argparse


class LedgerCli(object):
    '''
    Cli client for Ledger
    '''


def parse_arguments():
    '''
    Parse the command line arguments.
    '''
    parser = argparse.ArgumentParser(
        prog="ledgercli.py",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='Ledger command line')
    subparsers = parser.add_subparsers(
        dest="operation",
        help="sub commands")

    # Summary.
    showparser = subparsers.add_parser("show",
                                       help="Show configuration")
    showparser.add_argument("-f", "--format",
                            choices=["text", "json"],
                            required=False,
                            help="Output format")
    showparser.add_argument("-n", "--node",
                            required=False,
                            help="Show configuration for specific host")

    showparser.add_argument("resource",
                            help="Configuration names eg nova, keystone")



    namespace = parser.parse_args()

    return namespace


def main():
    namespace = parse_arguments()
    print namespace



if __name__ == '__main__':
    main()
