#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Ledger CLI
'''

import os
import sys
import argparse
import textwrap
import prettytable
import ledger.ledger as ledger
import ledger.prettyterm as prettyterm


class LedgerCli(object):
    '''
    Cli client for Ledger
    '''
    def __init__(self):
        # Parse Command line arguments.
        self.namespace = self.__parse_arguments()

        # Get the ledger configration file.
        #1. Check in ~/$HOME/ledger.conf
        #2. Check the environ variable LEDGER_CONFIG_FILE
        homedir = os.environ.get('HOME', None)
        ledgerfile = os.path.join(homedir, "ledger.conf")
        ledgerenvfile = os.environ.get('LEDGER_CONFIG_FILE', None)

        if os.path.exists(ledgerfile):
            self.config_file = ledgerfile
        elif ledgerenvfile is not None and \
            os.path.exists(ledgerenvfile):
            self.config_file = ledgerenvfile
        else:
            print "Ledger config file not found [$HOME/ledger.conf or ", \
                " environment variable LEDGER_CONFIG_FILE"
            sys.exit()


        if self.namespace.operation == "show":
            self.perform_show_operation()
        elif self.namespace.operation == "list-env":
            self.perform_list_env()

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
        showparser.add_argument("-e", "--environment",
                                required=True,
                                help="Specify environment for the resource")
        showparser.add_argument("-f", "--format",
                                choices=["table", "json"],
                                required=False,
                                help="Output format (Default: tabular)")
        showparser.add_argument("-n", "--node",
                                required=False,
                                help="Show configuration for specific host")

        showparser.add_argument("resource",
                                help="Configuration names eg nova, keystone")

        # List env.
        subparsers.add_parser("list-env",
                              help="List all the env to access")


        namespace = parser.parse_args()

        return namespace

    def perform_show_operation(self):
        '''
        SHOW Operation handler.
        '''
        if not self.__is_valid_env(self.namespace.environment):
            sys.exit()

        hostname = None
        if self.namespace.node is not None:
            hostname = self.namespace.node

        ledgermgr = ledger.Ledger(self.config_file)
        cfgdict = ledgermgr.display_resource(self.namespace.environment,
                                             self.namespace.resource,
                                             host=hostname)

        # Parse the config dict.
        # Generate options list.
        sections = {}
        for host in cfgdict.keys():
            hostobj = cfgdict[host]['config']
            for section in hostobj.keys():
                sections[section] = {}
                options = set()
                for option in hostobj[section].keys():
                    options.add(option)
                sections[section]['options'] = options

        #import pprint
        #pp = pprint.PrettyPrinter()
        #pp.pprint(sections)

        SECTION_COLUMN_WIDTH = 30
        OPTIONS_COLUMN_WIDTH = 30
        VALUES_COLUMN_WIDTH = 40

        # Build table.
        headers = []
        fmt_sectionstr = prettyterm.fmtstring("SECTIONS",
                                              attrs=['bold'])
        fmt_optionstr = prettyterm.fmtstring("OPTIONS",
                                             attrs=['bold'])
        headers.append(fmt_sectionstr)
        headers.append(fmt_optionstr)
        for host in cfgdict.keys():
            fmt_hoststr = prettyterm.fmtstring(host,
                                               attrs=['bold'])
            headers.append(fmt_hoststr)

        table = prettytable.PrettyTable(headers)
        table.align[fmt_sectionstr] = "l"
        table.align[fmt_optionstr] = "l"
        for section in sections.keys():
            section_start = True

            # Check if there are any options within this section.
            # If not we skip over this.
            if len(sections[section]['options']) == 0:
                continue
            for option in sections[section]['options']:
                row = []
                if section_start is True:
                    sectionstr = textwrap.fill(section,
                                               width=SECTION_COLUMN_WIDTH)
                    section_start = False
                else:
                    sectionstr = textwrap.fill("",
                                               width=SECTION_COLUMN_WIDTH)
                row.append(sectionstr)
                optionstr = textwrap.fill(option, width=OPTIONS_COLUMN_WIDTH)
                row.append(optionstr)
                for host in cfgdict.keys():
                    sectionval = cfgdict[host]['config'].get(section, None)
                    if sectionval is None:
                        row.append(" No Section")
                        continue

                    optionval = cfgdict[host]['config'][section].get(option,
                                                                     None)
                    if optionval is None:
                        row.append("No options")
                        continue
                    optionstr = textwrap.fill(optionval,
                                              width=VALUES_COLUMN_WIDTH)

                    row.append(optionstr)
                table.add_row(row)
            blank_row = ["-"*SECTION_COLUMN_WIDTH,
                         "-" * OPTIONS_COLUMN_WIDTH]
            for host in cfgdict.keys():
                blank_row.append("-"*VALUES_COLUMN_WIDTH)
            table.add_row(blank_row)

        print table

    def perform_list_env(self):
        '''
        List all the environments.
        '''
        print "list env"
        ledgermgr = ledger.Ledger(self.config_file)
        envlist = ledgermgr.get_environments_from_config()

        fmt_name = prettyterm.fmtstring("Name", attrs=['bold'])
        fmt_desc = prettyterm.fmtstring("Description", attrs=['bold'])

        table = prettytable.PrettyTable([fmt_name, fmt_desc])
        table.align[fmt_name] = "l"
        table.align[fmt_desc] = "l"
        for env in envlist:
            table.add_row([env, ""])

        print table

    def __is_valid_env(self, env):
        '''
        Validate the env variable
        '''
        ledgermgr = ledger.Ledger(self.config_file)
        envlist = ledgermgr.get_environments_from_config()

        if env not in envlist:
            print "Invalid environment [%s]" % env
            return False

        return True



def main():
    ledgercli = LedgerCli()


if __name__ == '__main__':
    main()
