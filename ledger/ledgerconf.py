#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import yaml




class LedgerConf(object):
    '''
    Class to manage the ledger config file
    '''
    def __init__(self, config_file):
        '''
        Ledger Configfile
        '''
        self.config = self.__parse_ledger_config(config_file)

    def __parse_ledger_config(self, config_file):
        '''
        Check the validity of the config file.
        '''
        parsed = None

        try:
            if not os.path.isabs(config_file):
                print "Provide absolute path to Ledger config file [%s]" % \
                    config_file
                return None

            if not os.path.exists(config_file):
                print "Invalid file [%s]. Does not exist" % config_file
                return None

            fhandle = open(config_file)

            parsed = yaml.safe_load(fhandle)
            fhandle.close()

        except OSError as err:
            print "OS Exception: [%s] [file: %s]" % (err, config_file)
            return None

        except IOError as err:
            print "IO Exception: [%s] [file: %s]" % (err, config_file)
            return None

        except yaml.parser.ParserError as parse_err:
            print "[%s] Parsing failed: [%s]" % (config_file, parse_err)
            return None

        return parsed

    def get_resource_info(self, resourcename, env=None):
        '''
        Given a resource name return the dict
        '''
        if env is None:
            env = self.config.keys()[0]
            envdata = self.config[env]
        else:
            envdata = self.config[env]

        resource_data = envdata['resources'][resourcename]

        return resource_data



