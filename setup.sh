#!/bin/bash
set -e

# TODO: Complete this file

if [[ $EUID -ne 0 ]]; then
    echo "You must be root to run this! Authenticate now."
    sudo "$0" "$@"
    exit $?
fi

CURR_DIR=$(pwd)
CRON_JOB="*/5 * * * * /usr/bin/python3 $CURR_DIR/main.py >/dev/null 2>&1"
(crontab -l; echo $CRON_JOB) | crontab -
