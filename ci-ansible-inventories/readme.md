# Changes files
Changes the following files/folders. This is needed before you can run the ansible-playbook

- Folder:
    - inventories/`<yourtenant>`.ice.ibmcloud.com
    - inventories/`<yourtenant>`.ice.ibmcloud.com/host_vars/`<yourtenant>`.ice.ibmcloud.com

- Files:
    - inventories/< yourtenant >.ice.ibmcloud.com/group_vars/all/`vars.yml`
    - inventories/< yourtenant >.ice.ibmcloud.com/host_vars/< yourtenant >.ice.ibmcloud.com/`vars.yml`
    - inventories/< yourtenant >.ice.ibmcloud.com/host_vars/< yourtenant >.ice.ibmcloud.com/`vault.yml`

# Change python interpreter
The interpreter for python is defined in the next file:

- inventories/< yourtenant >.ice.ibmcloud.com/group_vars/all/`vars.yml`
