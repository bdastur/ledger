#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import unittest
import ledger.ledgerconf as ledgerconf
import ledger.resource as resource
import ledger.ledger as ledger


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

    def test_fetch_ledger_resource(self):
        print "Test fetch ledger resource"
        homedir = os.environ.get('HOME', None)
        configfile = os.path.join(homedir, "ledgerconf.yaml")
        print "config file: ", configfile

        ledgermgr = ledger.Ledger(configfile)
        ledgermgr.populate_resource("test_environment",
                                    "nova")

    def test_fetch_all_ledger_resources(self):
        print "Test populate all resources"
        homedir = os.environ.get('HOME', None)
        configfile = os.path.join(homedir, "ledgerconf.yaml")
        print "config file: ", configfile

        ledgermgr = ledger.Ledger(configfile)
        ledgermgr.populate_all_resources()

    def test_display_resource(self):
        print "Test displaying resource"
        homedir = os.environ.get('HOME', None)
        configfile = os.path.join(homedir, "ledgerconf.yaml")
        print "Config file: ", configfile

        ledgermgr = ledger.Ledger(configfile)
        ledgermgr.display_resource("test_environment",
                                   "nova")

    def test_parse_resource_valid_ini(self):
        print "test parse resource (valid ini)"
        curpath = os.getcwd()
        resource_path = os.path.join(curpath,
                                     "testdata/nova.conf")
        print "resource path: ", resource_path
        resparse = resource.Parse()
        resparse.parse_resource(resource_path)

    def test_parse_resource_invalid_ini(self):
        print "test parse resource (invalid ini)"
        curpath = os.getcwd()
        resource_path = os.path.join(curpath,
                                     "testdata/invalid.conf")

        resparse = resource.Parse()
        resparse.parse_resource(resource_path)







