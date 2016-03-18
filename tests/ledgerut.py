#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import unittest
import ledger.ledgerconf as ledgerconf


class LedgerUT(unittest.TestCase):
    '''
    Ledger unit tests
    '''
    def test_ledgerconfig_basic(self):
        print "test ledgerconfig_basic"
        curpath = os.getcwd()
        ledgerconf_file = os.path.join(curpath,
                                       "../sample_configs/ledger.yaml.sample")
        print "conf file: ", ledgerconf_file
        lconf = ledgerconf.LedgerConf(ledgerconf_file)
        print lconf.config

        data = lconf.get_resource_info("nova")
        print "data: ", data



