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
    def __init__(self):
        # Parse Command line arguments.
        self.namespace = self.__parse_arguments()
        print self.namespace

        if self.namespace.operation == "show":
            self.perform_show_operation()

    def __parse_arguments(self):
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

        # SHOW.
        showparser = subparsers.add_parser("show",
                                           help="Show configuration")
        showparser.add_argument("-f", "--format",
                                choices=["table", "json"],
                                required=False,
                                help="Output format (Default: tabular)")
        showparser.add_argument("-n", "--node",
                                required=False,
                                help="Show configuration for specific host")

        showparser.add_argument("resource",
                                help="Configuration names eg nova, keystone")

        namespace = parser.parse_args()

        return namespace

    def perform_show_operation(self):
        '''
        SHOW Operation handler.
        '''
        print "show operation: "
        hostname = None
        if self.namespace.node is not None:
            hostname = self.namespace.node




def main():
    ledgercli = LedgerCli()


if __name__ == '__main__':
    main()
