#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
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



