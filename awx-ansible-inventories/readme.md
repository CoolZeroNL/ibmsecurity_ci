# Changes files
Changes the following files/folders. This is needed before you can run the ansible-playbook

- Folder:
    - inventories/awx.`<domain>`.nl
    - inventories/awx.`<domain>`.nl/host_vars/awx.`<domain>`.nl

- Files:
    - inventories/awx.< domain >.nl/`hosts`
    - inventories/awx.< domain >.nl/group_vars/all/`vars.yml`
    - inventories/awx.< domain >.nl/host_vars/awx.< domain >.nl/`vars.yml`
    - inventories/awx.< domain >.nl/host_vars/awx.< domain >.nl/`vault.yml`

# Change python interpreter
The interpreter for python is defined in the next file:

- inventories/awx.`<domain>`.nl/group_vars/all/`vars.yml`
