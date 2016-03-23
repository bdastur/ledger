# ledger
Ledger is a utility to aggregate and manage configuration files.
---

Ledger allows you to view configuration files from multiple hosts remotely (and in the future edit them), remotely 
without having to login to each host to view or change configuration. 

## How does it work:
Ledger does not require any agents running on remote hosts. It can be simply installed on any Linux host by a git pull
of this repository and sourcing the setup.sh script, which sets the correct environment variables.

It uses secure tunnel to connect to the hosts to get the configuration files, parses the config data and ouputs the results.
Currently users can use the ledgercli to show configurations and compare configs between different hosts.

See examples of CLI commands and outputs.

## Features:
| *Description*| *Availability*|
|---|---|
| Show configuration from remote host | yes |
| Show configurations for multiple remote hosts | yes |
| Highlight configuration differences | yes |
| Ability to Update or Add configuration options | Not yet |
| Ability to track configuration changes over time | Not yet|


## Usage Examples:
Here's an example of the ledgercli to display nova.conf configuration from multiple hosts:

    server-4bff-#./cliclient/ledgercli.py show -h
    usage: ledgercli.py show [-h] -e ENVIRONMENT [-f {table,json}] [-n NODE]
                             resource

    positional arguments:
      resource              Configuration names eg nova, keystone

    optional arguments:
      -h, --help            show this help message and exit
      -e ENVIRONMENT, --environment ENVIRONMENT
                        Specify environment for the resource
      -f {table,json}, --format {table,json}
                            Output format (Default: tabular)
      -n NODE, --node NODE  Show configuration for specific host
    server-4bff-#
    server-4bff-#./cliclient/ledgercli.py show --environment sanjose nova
    +---------------------------+---------------------------+------------------------------------------+------------------------------------------+------------------------------------------+
    | SECTIONS                  | OPTIONS                   |    100.20.20.100                         |    100.20.20.101                         |                        100.10.10.102     |
    +---------------------------+---------------------------+------------------------------------------+------------------------------------------+------------------------------------------+
    | ephemeral_storage_encrypt | notification_driver       |                messaging                 |                messaging                 |                messaging                 |
    | ion                       |                           |                                          |                                          |                                          |
    |                           | state_path                |              /var/lib/nova               |              /var/lib/nova               |              /var/lib/nova               |
    |                           | quota_instances           |                   1000                   |                   1000                   |                   1000                   |
    |                           | quota_cores               |                   1024                   |                   1024                   |                   1024                   |
    |                           | quota_driver              |         nova.quota.DbQuotaDriver         |         nova.quota.DbQuotaDriver         |         nova.quota.DbQuotaDriver         |
    |                           | quota_ram                 |                 1024000                  |                 1024000                  |                 1024000                  |
    |                           | quota_metadata_items      |                   128                    |                   128                    |                   128                    |
    |                           | quota_floating_ips        |                    10                    |                    10                    |                    10                    |
    | ------------------------- | ------------------------- | ---------------------------------------- | ---------------------------------------- | ---------------------------------------- |
    :
    | ------------------------- | ------------------------- | ---------------------------------------- | ---------------------------------------- | ---------------------------------------- |
    | oslo_messaging_rabbit     | rabbit_userid             |                   quest                  |                   guest                  |                   guest                  |
    |                           | notification_driver       |                messaging                 |                messaging                 |                messaging                 |
    |                           | rabbit_virtual_host       |                    /                     |                    /                     |                    /                     |
    |                           | quota_instances           |                   1000                   |                   1000                   |                   1000                   |
    |                           | rabbit_password           |               aaaaaaaaaaa                |               aaaaaaaaaaa                |               aaaaaaaaaaa                |
    |                           | rabbit_ha_queues          |                   True                   |                   True                   |                   True                   |
    |                           | quota_cores               |                   1024                   |                   1024                   |                   1024                   |
    |                           | quota_driver              |         nova.quota.DbQuotaDriver         |         nova.quota.DbQuotaDriver         |         nova.quota.DbQuotaDriver         |
    |                           | rabbit_hosts              | 192.16.96.5:5672,192.16.96.6:5672,192    | 192.16.96.5:5672,192.16.96.6:5672,192    | 192.16.96.5:5672,192.16.96.6:5672,192    |
    |                           |                           |             .16.96.8:5672                |             .16.96.8:5672                |             .16.96.8:5672                |
    |                           | quota_metadata_items      |                   128                    |                   128                    |                   128                    |
    |                           | quota_floating_ips        |                    10                    |                    10                    |                    10                    |
    |                           | rpc_backend               |           nova.rpc.impl_kombu            |           nova.rpc.impl_kombu            |           nova.rpc.impl_kombu            |
    | ------------------------- | ------------------------- | ---------------------------------------- | ---------------------------------------- | ---------------------------------------- |
    :


Another example to display keystone configuration from a remote host:

    server-4bff-#./cliclient/ledgercli.py show --environment sanjose keystone --node 100.100.21.123
    +---------------------------+---------------------------+------------------------------------------+
    | SECTIONS                  | OPTIONS                   |     100.100.21.123                       |
    +---------------------------+---------------------------+------------------------------------------+
    | app:public_service        | paste.app_factory         |   keystone.service:public_app_factory    |
    | ------------------------- | ------------------------- | ---------------------------------------- |
    | composite:admin           | /                         |            admin_version_api             |
    :
    | default                   | /v2.0                     |                admin_api                 |
    |                           | suffix                    |         dc=mgmt,dc=symcpe,dc=net         |
    |                           | project_domain_id_attribu |             businessCategory             |
    |                           | te                        |                                          |
    |                           | notification_topics       |              notifications               |
    |                           | backward_compatible_ids   |                   true                   |
    |                           | verbose                   |                   true                   |
    :

Display All environments configured in ledger conf:

    server-4bff-#./cliclient/ledgercli.py list-env
    list env
    +-------------------+-------------+
    | Name              | Description |
    +-------------------+-------------+
    | test_environment2 |             |
    | sanjose           |             |
    +-------------------+-------------+


## Configuration File Example:

    ---
    "sanjose":
      ledger_root: "/tmp/ledger/env1"
      resources:
          nova:
              hosts:
                  - "100.20.20.100"
                  - "100.20.20.101"
                  - "100.20.20.102"
              resource_paths:
                  - "/etc/nova/nova.conf"
          keystone:
              hosts:
                  - "100.20.20.150"
                  - "100.20.20.151"
                  - "100.20.20.152"
              resource_paths:
                  - "/etc/keystone/keystone.conf"
          glance:
              hosts:
                  - "100.20.20.160"
                  - "100.20.20.161"
                  - "100.20.20.162"
              resource_paths:
                  - "/etc/glance/glance-api.conf"
                  - "/etc/glance/glance-registry.conf"

    "test_environment2":
      ledger_root: "/tmp/ledger/env2"
      resources:
          nova:
              hosts:
                  - "34.34.22.22"
              resource_paths:
                  - "/etc/nova/nova.conf"
    ...

## Setup:
Setting up Ledger is super simple:

Here's how we set up:

    <bold>:~ behzad_dastur$ mkdir ledger_workingdir</bold>
    <bold>:~ behzad_dastur$ cd ledger_workingdir/</bold>
    :ledger_workingdir behzad_dastur$ git clone https://github.com/bdastur/ledger.git
       Cloning into 'ledger'...
       remote: Counting objects: 148, done.
       remote: Compressing objects: 100% (120/120), done.
       remote: Total 148 (delta 63), reused 73 (delta 11), pack-reused 0
       Receiving objects: 100% (148/148), 59.20 KiB | 0 bytes/s, done.
       Resolving deltas: 100% (63/63), done.
       Checking connectivity... done.
    <bold>:ledger_workingdir behzad_dastur$ cd ledger/</bold>
    <bold>:ledger behzad_dastur$ source setup.sh</bold>

The setup.sh script will ask for your remote password to access the hosts. Also a path to your ledger config file.
It will pull other repositories like ansible, pyansible and set the correct python path.

If the setup. is successfull, you should be able to use ledgercli.py from that point on.

Here's how the setup.sh script run looks:

    <bold>:ledger behzad_dastur$ source setup.sh</bold>
    <bold>Remote Password for behzad_dastur:</bold> 
    Set LEDGER_CONFIG_FILE (y/n):<bold>y</bold>

    Ledger config file: <bold>/home/behzad_dastur/ledgerconf.yaml</bold>
    pulling repo: [http://github.com/ansible/ansible.git]   ---> [DONE]
    pulling repo: [https://github.com/bdastur/spam.git]   ---> [DONE]
    running egg_info
    creating lib/ansible.egg-info
    writing requirements to lib/ansible.egg-info/requires.txt
    writing lib/ansible.egg-info/PKG-INFO
    writing top-level names to lib/ansible.egg-info/top_level.txt
    writing dependency_links to lib/ansible.egg-info/dependency_links.txt
    writing manifest file 'lib/ansible.egg-info/SOURCES.txt'
    reading manifest file 'lib/ansible.egg-info/SOURCES.txt'
    reading manifest template 'MANIFEST.in'
    no previously-included directories found matching 'v2'
    no previously-included directories found matching 'docsite'
    no previously-included directories found matching 'ticket_stubs'
    no previously-included directories found matching 'test'
    no previously-included directories found matching 'hacking'
    no previously-included directories found matching 'lib/ansible/modules/core/.git'
    no previously-included directories found matching 'lib/ansible/modules/extras/.git'
    writing manifest file 'lib/ansible.egg-info/SOURCES.txt'

    Setting up Ansible to run out of checkout...

    PATH=/Users/behzad_dastur/ledger_workingdir/ansible_stable1.9/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin
    PYTHONPATH=/Users/behzad_dastur/ledger_workingdir/ansible_stable1.9/lib:/Users/behzad_dastur/ledger_workingdir/pyansible:/Users/behzad_dastur/ledger_workingdir/ledger
    MANPATH=/Users/behzad_dastur/ledger_workingdir/ansible_stable1.9/docs/man:

    Remember, you may wish to specify your host file with -i

    Done!


