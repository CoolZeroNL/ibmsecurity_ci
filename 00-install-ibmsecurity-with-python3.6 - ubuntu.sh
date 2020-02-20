#!/bin/bash

if [[ $EUID -ne 0 ]]; then
  echo "You must be a root user" 2>&1
  exit 1
fi

# install in home dir.
cd ~

set -e

 if cat /etc/*release | grep ^NAME | grep Ubuntu; then
    echo "==============================================="
    echo "Installing packages on Ubuntu"
    echo "==============================================="
 else
    echo "OS NOT DETECTED, couldn't install packages"
    exit 1;
 fi

# Install OS pre-requisites
sudo apt-get -y update; sudo apt-get -s clean
sudo apt-get -y install nano unzip gcc curl git 
sudo apt-get -y install python3 python3-pip 
sudo apt-get -y install ansible

# Install/Update Python modules
pip3 install --upgrade pip requests ansible python3-ldap pygments
pip3 install --upgrade git+https://github.com/ibm-security/ibmsecurity#egg=ibmsecurity

# Prepare Ansible environment
sudo mkdir -p /etc/ansible/ /ansible /etc/ansible/roles/
sudo touch /etc/ansible/hosts
sudo chmod 777 /etc/ansible/hosts
sudo echo "[local]" >> /etc/ansible/hosts
sudo echo "localhost" >> /etc/ansible/hosts

sudo mkdir -p /ansible/playbooks

# Prepare ISAM Ansible Common Roles 
sudo ansible-galaxy install -c -p /etc/ansible/roles git+https://github.com/ibm-security/isam-ansible-roles.git 

# Prepare ISDS Ansible Common Roles 
sudo ansible-galaxy install -c -p /etc/ansible/roles git+https://github.com/IBM-Security/isds-ansible-roles.git

# Download ISAM Sample Playbooks
cd 
git clone https://github.com/IBM-Security/isam-ansible-playbook-sample.git

# replace ansible.cfg
sudo bash -c 'echo "[defaults]" > /etc/ansible/ansible.cfg'
sudo bash -c 'echo "roles_path=/etc/ansible/roles/isam-ansible-roles:/etc/ansible/roles/ci-ansible-roles:/etc/ansible/roles/isds-ansible-roles" >> /etc/ansible/ansible.cfg'


