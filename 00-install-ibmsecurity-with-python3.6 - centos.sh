#!/bin/bash

if [[ $EUID -ne 0 ]]; then
  echo "You must be a root user" 2>&1
  exit 1
fi

# install in home dir.
cd ~

    # Centos check
    version=`rpm --eval '%{centos_ver}'`

    if [ "$version" -eq "7" ]; then
        echo "version 7"
    elif [ "$version" -eq "8" ]; then
        echo "version 8"
        yum install -y dnf-plugins-core
        yum config-manager --set-enabled PowerTools
    else
        echo "No Centos 7 or 8 found"
        exit 1
    fi

# Install OS pre-requisites
yum -y update; yum clean all
yum -y install epel-release; yum clean all
yum -y install nano unzip gcc curl openssl-devel git openssh-clients; yum clean all
yum -y install python3 python3-pip python3-devel ; yum clean all

# Install/Update Python modules
pip3 install --upgrade pip requests ansible python3-ldap pygments
pip install --upgrade git+https://github.com/ibm-security/ibmsecurity#egg=ibmsecurity
pip3 install --upgrade git+https://github.com/ibm-security/ibmsecurity#egg=ibmsecurity

# Prepare Ansible environment
mkdir /etc/ansible/ /ansible /etc/ansible/roles/
echo "[local]" >> /etc/ansible/hosts
echo "localhost" >> /etc/ansible/hosts

mkdir -p /ansible/playbooks

# Prepare ISAM Ansible Common Roles 
ansible-galaxy install -c -p /etc/ansible/roles git+https://github.com/ibm-security/isam-ansible-roles.git 

# Prepare ISDS Ansible Common Roles 
ansible-galaxy install -c -p /etc/ansible/roles git+https://github.com/IBM-Security/isds-ansible-roles.git

if [[ -z "${ANSIBLE_ROLES_PATH}" ]]; then
  
  echo 'ANSIBLE_GATHERING=smart' >> /etc/bashrc
  echo 'ANSIBLE_HOST_KEY_CHECKING=false' >> /etc/bashrc
  echo 'ANSIBLE_RETRY_FILES_ENABLED=false' >> /etc/bashrc
  echo 'ANSIBLE_ROLES_PATH=/etc/ansible/roles/ci-ansible-roles' >> /etc/bashrc
  echo 'DEFAULT_ROLES_PATH=/etc/ansible/roles/ci-ansible-roles:$DEFAULT_ROLES_PATH' >> /etc/bashrc 
  echo 'ANSIBLE_SSH_PIPELINING=True' >> /etc/bashrc
  echo 'PYTHONPATH=/ansible/lib' >> /etc/bashrc
  echo 'PATH=/ansible/bin:$PATH' >> /etc/bashrc

  echo "Done loading rules into: /etc/bashrc"
else
  echo "rules already exists in: /etc/bashrc"
fi

# To load the new environment variables into the current shell session use the source command:
source ~/.bashrc

cd 
git clone https://github.com/IBM-Security/isam-ansible-playbook-sample.git


cat <<EOT >> /etc/ansible/ansible.cfg
[defaults]
roles_path=/etc/ansible/roles/isam-ansible-roles:/etc/ansible/roles/ci-ansible-roles:/etc/ansible/roles/isds-ansible-roles
EOT
