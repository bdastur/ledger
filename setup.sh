#!/bin/bash

####################################################
# Ledger Setup:
# --------------------------------------------------
####################################################

setup_logs="/tmp/setup.log_"`date +"%b%d%y_%H%M%S"`

ansible_repo="http://github.com/ansible/ansible.git"
ansible_branch="stable-1.9"
ansible_destdir="../ansible_stable1.9"

pyansible_repo="https://github.com/bdastur/spam.git"
pyansible_branch="master"
pyansible_destdir="../pyansible"

ledger_dir=$(pwd)
root_dir=${ledger_dir%/*}                                                                                                                                                                      

ansible_path="${root_dir}/ansible_stable1.9"
pyansible_path="${root_dir}/pyansible"

pythonpath="${pyansible_path}:${ledger_dir}"

###########################################
# The function does git pull if the dest 
# directory doesn't already exist.
# Args:
# $1 - git repo
# $2 - destination directory
# $3 - branch
############################################
function git_pull () 
{
    gitrepo=$1
    localgitrepo=$2
    branch=$3

    if [[ ! -z $branch ]]; then
        branch="-b $branch"
    fi

    echo -n "pulling repo: [$gitrepo]  "
    if [[ ! -d $localgitrepo ]]; then 
        echo "Pulling $gitrepo $branch" >> $setup_logs 2>&1
        git clone $gitrepo $branch $localgitrepo >>  $setup_logs 2>&1
    fi

    if [[ -d $localgitrepo ]]; then
        echo " ---> [DONE]"
    else
        echo " ---> [FAILED]";echo
        echo "Error logs: $setup_logs"
    fi
}

# Set ENV Variables
# Username, password, Ledger config path
export PYANSI_USERNAME=$LOGNAME

if [[ -z ${PYANSI_PASSWORD} ]]; then
    echo -n "Remote Password for ${PYANSI_USERNAME}: "; read -s PYANSI_PASSWORD
    echo ""
    export PYANSI_PASSWORD=$PYANSI_PASSWORD
fi

export ANSIBLE_HOST_KEY_CHECKING=False

if [[ -z ${LEDGER_CONFIG_FILE} ]]; then
    echo -n "Set LEDGER_CONFIG_FILE (y/n):"; read CONFFILE_OPTION 
    if [[ $CONFFILE_OPTION == "y" ]]; then
        echo ""
        echo -n "Ledger config file: "; read LEDGER_CONFIG_FILE
        export LEDGER_CONFIG_FILE=$LEDGER_CONFIG_FILE
    fi
fi


# Pull repositories.
git_pull ${ansible_repo} ${ansible_destdir} ${ansible_branch}
# Add the Ansible submodules
cd ${ansible_path}
git submodule update --init --recursive >> $setup_logs 2>&1
cd ${ledger_dir}
git_pull ${pyansible_repo} ${pyansible_destdir} ${pyansible_branch}


export PYTHONPATH=${pythonpath}

###################################################
# Source Ansible Environment
###################################################
source ../ansible_stable1.9/hacking/env-setup




