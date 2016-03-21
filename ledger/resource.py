#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
from ConfigParser import RawConfigParser
from ConfigParser import NoOptionError
import ConfigParser
import pyansible.ansirunner as ansirunner


class Fetch(object):
    '''
    Fetch remote files.
    '''
    def __init__(self,
                 sudo=True,
                 sudo_pass=None):
        '''
        Given a hostlist and a filename, fetch it
        from the remote host
        '''
        self.username = os.environ.get("PYANSI_USERNAME", None)
        self.password = os.environ.get("PYANSI_PASSWORD", None)
        self.sudo = sudo
        if sudo_pass is None:
            self.sudo_pass = self.password
        else:
            self.sudo_pass = sudo_pass

    def fetch_resource(self,
                       hostlist,
                       resourcename,
                       destpath):
        '''
        Fetch a file from the provided hosts.
        '''
        runner = ansirunner.AnsibleRunner()

        complex_args = {"src": resourcename,
                        "dest": destpath}

        result, failed_hosts = runner.ansible_perform_operation(
            module="fetch",
            complex_args=complex_args,
            host_list=hostlist,
            remote_user=self.username,
            remote_pass=self.password,
            sudo=self.sudo,
            sudo_user="root",
            sudo_pass=self.sudo_pass,
            forks=5)

        return(result, failed_hosts)


class Parse(object):
    '''
    Parse a resource (config file)
    '''
    def __init__(self):
        self.cfgparser = None

    def parse_resource(self, resourcepath):
        '''
        Given a path to the resource (on local filesystem)
        parse the file and return appropriate result.
        '''

        if not os.path.exists(resourcepath):
            print "[%s] Invalid. Does not exist" % resourcepath
            return None

        # ini file.
        ret = self.__parse_ini_file(resourcepath)
        if ret is None:
            # Not an ini file. Try other format.
            pass

        for section in self.cfgparser.sections():
            print "Section: ", section
            try:
                for (name, value) in self.cfgparser.items(section):
                    print "%s: %s = %s" % (section, name, value)
            except ConfigParser.InterpolationMissingOptionError as err:
                print "[%s]" % err
                continue



    def __parse_ini_file(self, resourcepath):
        '''
        The function checks if the file is of type INI and
        '''

        # Preprocess the ini file:
        # Remove comments, blanklines, also modify section name
        # from Default to COMMON.
        randomname = self.__generate_random_filename()
        print "Random name: ", randomname
        randomfile = os.path.join("/tmp", randomname)

        fhandle = open(resourcepath, 'r')
        whandle = open(randomfile, 'w')
        try:
            data = fhandle.read()
            for line in data.splitlines():
                if re.match(r'#.*', line) or \
                        len(line) == 0:
                    continue
                if re.match(r'[Default]', line, re.IGNORECASE):
                    line = '[COMMON]'

                line = line + "\n"
                whandle.write(line)
        except IOError as ioerr:
            print "[%s]" % ioerr
            return None

        fhandle.close()
        whandle.close()

        resourcepath = randomfile

        self.cfgparser = RawConfigParser()
        try:
            self.cfgparser.read(resourcepath)
        except ConfigParser.MissingSectionHeaderError as err:
            print "[%s] Invalid INI config [%s]" % \
                (resourcepath, err)

            return None

        os.remove(randomfile)

    def __generate_random_filename(self):
        import string
        import random

        size = 8
        chars = string.digits + string.ascii_letters
        return ''.join(random.choice(chars) for _ in range(size))



