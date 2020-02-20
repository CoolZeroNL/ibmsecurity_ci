
# 1. Info
1. This will install python3.6 and `ibmsecurity` library !
2. Run `00-install-ibmsecurity-with-python3.6 - centos/ubuntu.sh` to install [ibmsecurity](https://github.com/IBM-Security/ibmsecurity) and Python 3.6
3. Run `01-install-ci-for-python-3.6 - centos/ubuntu.sh` to merge the CIC module into `ibmsecurity` library
3. Roles must (are) been installed at `/etc/ansible/roles`

# 2. Make a inventory
see [ci-ansible-inventories/readme.md](https://github.com/CoolZeroNL/ibmsecurity_ci/blob/master/ci-ansible-inventories/readme.md)

Changes the following files/folders. This is needed before you can run the ansible-playbook

- Folder:
    - inventories/`<yourtenant>`.ice.ibmcloud.com
    - inventories/`<yourtenant>`.ice.ibmcloud.com/host_vars/`<yourtenant>`.ice.ibmcloud.com

- Files:
    - inventories/< yourtenant >.ice.ibmcloud.com/group_vars/all/`vars.yml`
    - inventories/< yourtenant >.ice.ibmcloud.com/host_vars/< yourtenant >.ice.ibmcloud.com/`vars.yml`
    - inventories/< yourtenant >.ice.ibmcloud.com/host_vars/< yourtenant >.ice.ibmcloud.com/`vault.yml`

## 2.1. Change python interpreter
The interpreter for python is defined in the next file:

- inventories/< yourtenant >.ice.ibmcloud.com/group_vars/all/`vars.yml`

# 3. Run playbooks?
see [ci-ansible-playbook-sample/readme.md](https://github.com/CoolZeroNL/ibmsecurity_ci/blob/master/ci-ansible-playbook-sample/readme.md)

```
cd ci-ansible-playbook-sample
ansible-playbook -i ../ci-ansible-inventories/inventories/<yourtentant>.ice.ibmcloud.com/ get_all_users.yml
```