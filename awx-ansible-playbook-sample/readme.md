# install:

```
ansible-playbook -i ../awx-ansible-inventories/inventories/localhost/ install_python_modules.yml
```

# use:

```
cd ./ibmsecurity_ci/awx-ansible-playbook-sample/
ansible-playbook -i ../awx-ansible-inventories/inventories/awx.domain.nl/ awx_update_settings.yml
```