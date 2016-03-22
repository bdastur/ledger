#!/bin/bash

####################################################
# Ledger Setup:
# --------------------------------------------------
####################################################

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

curdir=$(pwd)
export PYTHONPATH=${curdir}

