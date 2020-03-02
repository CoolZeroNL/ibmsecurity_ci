# base config awx

0. add default org
1. install project
    - ibmsecurity_ci
        - awx playbooks
        - ibm cic playbooks
        - iventory awx-localhost
2. install inventory
    - awx-localhost
    - manual - sync inventory source.
3. update settings 
    - saml auth settings --> CIC

install job templates


ansible-playbook -i ../awx-ansible-inventories/inventories/awx.tempdata.nl/ awx_add_organization.yml
ansible-playbook -i ../awx-ansible-inventories/inventories/awx.tempdata.nl/ awx_add_project.yml
ansible-playbook -i ../awx-ansible-inventories/inventories/awx.tempdata.nl/ awx_add_inventory.yml
ansible-playbook -i ../awx-ansible-inventories/inventories/awx.tempdata.nl/ awx_add_inventory_source.yml