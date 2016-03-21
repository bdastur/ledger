#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from distutils.dir_util import copy_tree
import datetime
import ledgerconf
import resource


class Ledger(object):
    def __init__(self, ledger_config):
        '''
        Initialze the Ledger class.
        '''
        conf = ledgerconf.LedgerConf(ledger_config)
        if conf.config is None:
            print "Failed to parse Config file [%s]" % ledger_config
            return

        self.confmgr = conf
        self.config = conf.config
        self.__generate_ledger_root_directory()

    def __generate_ledger_root_directory(self):
        '''
        Generate the root directories.
        '''
        for env in self.config.keys():
            print "env: ", env
            ledger_root = self.config[env]['ledger_root']
            print "ledger root: ", ledger_root
            try:
                if os.path.exists(ledger_root):
                    # Since the path exists, we need not do anything.
                    # <TODO: Assuming here it is a directory>
                    continue

                os.makedirs(ledger_root)

            except IOError as err:
                print "IOError: [%s] [%s]" % (err, ledger_root)
                return

    def populate_resource(self,
                          env,
                          resourcename,
                          host=None,
                          latestonly=False):
        '''
        Populate the resource/file info for specified resource
        '''

        # Create a latests directory if not already create.
        now = datetime.datetime.now()
        curdate = str(now.year) + str(now.month) + str(now.day) \
            + "_" + str(now.hour) + str(now.minute) + str(now.second)

        fetch = resource.Fetch()
        #for env in self.config.keys():
        resourceobj = self.confmgr.get_resource_info(resourcename,
                                                     env=env)
        if host is None:
            hostlist = resourceobj['hosts']
        else:
            hostlist = [host]
        print "hostlist: ", hostlist

        # Build the destination path to save the files.
        ledger_root = self.config[env]['ledger_root']
        latest_dir = os.path.join(ledger_root, "latest")
        latest_dest_dir = os.path.join(latest_dir, resourcename)

        if not os.path.exists(latest_dir):
            os.makedirs(latest_dir)

        if not os.path.exists(latest_dest_dir):
            os.makedirs(latest_dest_dir)

        print "latest dir:", latest_dir

        for resourcepath in resourceobj['resource_paths']:
            print "resource path: ", resourcepath
            (result, failed_hosts) = fetch.fetch_resource(hostlist,
                                                          resourcepath,
                                                          latest_dest_dir)

        if not latestonly:
            now = datetime.datetime.now()
            curdate = str(now.year) + str(now.month) + str(now.day) \
                + "_" + str(now.hour) + str(now.minute) + str(now.second)
            now_dest_dir = os.path.join(ledger_root, curdate)
            copy_tree(latest_dest_dir, now_dest_dir)

    def populate_all_resources(self):
        '''
        Populate all resources.
        '''
        for env in self.config.keys():
            resources = self.config[env]['resources'].keys()
            print "Resources: ", resources
            for resourcename in resources:
                print "Resourcename: ", resourcename
                self.populate_resource(env, resourcename)

    def display_resource(self,
                         env,
                         resourcename,
                         host=None):
        '''
        Display the specified resource.
        '''
        resourceobj = self.confmgr.get_resource_info(resourcename,
                                                     env=env)
        if host is None:
            hostlist = resourceobj['hosts']
            #print "hostlist: ", hostlist
        else:
            # Only one host in the list.
            hostlist = [host]

        self.populate_resource(env,
                               resourcename,
                               latestonly=True)

        # Now we Get the resource data.
        ledger_root = self.config[env]['ledger_root']
        latest_dir = os.path.join(ledger_root, "latest")
        resource_dir = os.path.join(latest_dir, resourcename)
        #print "resource dir: ", resource_dir

        ledger_dict = {}
        for hostname in hostlist:
            ledger_dict[hostname] = {}
            ledger_dict[hostname]['config'] = {}
            #print "hostname: ", hostname
            perhostpath = os.path.join(resource_dir, hostname)
            #print "perhostpath: ", perhostpath

            for respath in resourceobj['resource_paths']:
                srcpath = os.path.join(perhostpath, respath[1:])
                #print "File path: ", srcpath
                if not os.path.exists(srcpath):
                    #print "path %s does not exist" % srcpath
                    continue

                # Get the resource config data.
                parser = resource.Parse()
                cfgdict = parser.parse_resource(srcpath)
                ledger_dict[hostname]['config'] = cfgdict

        return ledger_dict



    def get_environments_from_config(self):
        '''
        The function returns the environments from
        the parsed config file
        '''
        envlist = []
        for env in self.config.keys():
            envlist.append(env)

        return envlist












