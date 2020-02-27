#!/bin/bash

if [[ $EUID -ne 0 ]]; then
  echo "You must be a root user" 2>&1
  exit 1
fi

MY_PATH=`dirname "$0"`
MY_PATH=`( cd "$MY_PATH" && pwd )`

# Clean up current awx-ansibke-role, so that the current dev work is implementent, and wont trigger old roles with broken code.
sudo rm -R /etc/ansible/roles/awx-ansible-roles

# Append the ibmsecurity package with the AWX files 
sudo cp -R "$MY_PATH"/ibmsecurity /usr/local/lib/python3.6/dist-packages/           # note this can be different!

# Place new copy of the awx-ansible-roles
sudo mkdir -p /etc/ansible/roles/awx-ansible-roles
sudo cp -R "$MY_PATH"/awx-ansible-playbook-sample/roles/* /etc/ansible/roles/awx-ansible-roles
