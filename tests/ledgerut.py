#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import unittest
import ledger.ledgerconf as ledgerconf
import ledger.resource as resource


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

    def test_fetch_resource(self):
        print "test fetch resource"
        fetch = resource.Fetch()
        hostlist = ["v-cephmon-001-prod.lhr1.symcpe.net"]
        resourcename = "/tmp/ceph.conf"
        destpath = "/tmp/"

        (result, failed_hosts) = fetch.fetch_resource(hostlist,
                                                      resourcename,
                                                      destpath)





