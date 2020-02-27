# Index

<!-- TOC -->

- [Index](#index)
- [1. IBM Security CI Module](#1-ibm-security-ci-module)
    - [1.1. Make a inventory](#11-make-a-inventory)
    - [1.2. Run playbooks?](#12-run-playbooks)
- [1. AWX Module](#1-awx-module)
    - [1.1. Make a inventory](#11-make-a-inventory-1)
    - [1.2. Run playbooks?](#12-run-playbooks-1)

<!-- /TOC -->

# 1. IBM Security CI Module
- This will install python3.6 and [ibmsecurity](https://github.com/IBM-Security/ibmsecurity) library !
- Run `00-install-ibmsecurity-with-python3.6 - centos/ubuntu.sh` to install [ibmsecurity](https://github.com/IBM-Security/ibmsecurity) and Python 3.6
- Run `01-install-ci-for-python-3.6 - centos/ubuntu.sh` to merge the CIC module into [ibmsecurity](https://github.com/IBM-Security/ibmsecurity) library
- Roles must (are) been installed at `/etc/ansible/roles`

## 1.1. Make a inventory
- see [ci-ansible-inventories/readme.md](https://github.com/CoolZeroNL/ibmsecurity_ci/blob/master/ci-ansible-inventories/readme.md)

## 1.2. Run playbooks?
- see [ci-ansible-playbook-sample/readme.md](https://github.com/CoolZeroNL/ibmsecurity_ci/blob/master/ci-ansible-playbook-sample/readme.md)

# 1. AWX Module
- This will install python3.6 and [ibmsecurity](https://github.com/IBM-Security/ibmsecurity) library !
- Run `00-install-ibmsecurity-with-python3.6 - centos/ubuntu.sh` to install [ibmsecurity](https://github.com/IBM-Security/ibmsecurity) and Python 3.6
- Run `01-install-awx-for-python-3.6 - centos/ubuntu.sh` to merge the AWX module into [ibmsecurity](https://github.com/IBM-Security/ibmsecurity) library
- Roles must (are) been installed at `/etc/ansible/roles`

## 1.1. Make a inventory
- see [awx-ansible-inventories/readme.md](https://github.com/CoolZeroNL/ibmsecurity_ci/blob/master/awx-ansible-inventories/readme.md)

## 1.2. Run playbooks?
- see [awx-ansible-playbook-sample/readme.md](https://github.com/CoolZeroNL/ibmsecurity_ci/blob/master/awx-ansible-playbook-sample/readme.md)
