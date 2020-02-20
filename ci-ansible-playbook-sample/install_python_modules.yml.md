# install_python_modules.yml

This role is made to install the `ibmsecurity_ci/ibmsecurity` into your python library folder and merge with the existing `ibmsecurity` library. This to extend that library with the CIC module.

# AWX
This role can be used to install the modules.

1. Login Ansible Tower/AWX with administrator privileges.

## Create Inventory
1. Navigate to inventories and click on “+” to create new.
<p align="center">
  <img width="50%" src="./install_python_modules.yml.images/inventory.png">
</p>

2. Update the name field with desired values: `AWX - localhost`
<p align="center">
  <img width="50%" src="./install_python_modules.yml.images/inventory-add.png">
</p>

3. Here is the newly created inventory.
<p align="center">
  <img width="50%" src="./install_python_modules.yml.images/inventory-added.png">
</p>

4. Navigate to Host Tab and click on “+” to create new.
<p align="center">
  <img width="50%" src="./install_python_modules.yml.images/inventory-host.png">
</p>

5. Update the host name field with the value: `localhost`
<p align="center">
  <img width="50%" src="./install_python_modules.yml.images/inventory-host-add.png">
</p>

6. Here is the newly created inventory with a host.
<p align="center">
  <img width="50%" src="./install_python_modules.yml.images/inventory-host-added.png">
</p>

## Create Project
1. Navigate to Projects and click on “+” to create new.
<p align="center">
  <img width="50%" src="./install_python_modules.yml.images/projects.png">
</p>

2. Update the name, SCM Type, SCM URL fields with desired values, and enable `clean & delete on update`: 
- name: `AWX - localhost`
- SCM Type: `GIT`
- SCM URL: `https://github.com/CoolZeroNL/ibmsecurity_ci.git`
<p align="center">
  <img width="50%" src="./install_python_modules.yml.images/projects-add.png">
</p>

3. Here is the newly created Project, and see that the bullet in front is `green`.
<p align="center">
  <img width="50%" src="./install_python_modules.yml.images/projects-added.png">
</p>

## Create Template
1. Navigate to Templates and click on “+” to create new.
<p align="center">
  <img width="50%" src="./install_python_modules.yml.images/templates.png">
</p>

2. Update the name, Job Type, Inventory, Project, Playbook fields with desired values:
- Name: `Install Python Modules`
- Job Type: `Run`
- Inventory: `AWX - localhost`
- Project: `ibmsecurity_ci (Master)`
- Playbook: `ci-ansible-playbook-sample/install_python_modules.yml`

<p align="center">
  <img width="50%" src="./install_python_modules.yml.images/templates-add.png">
</p>

3. Here is the newly created Template.
<p align="center">
  <img width="50%" src="./install_python_modules.yml.images/templates-added.png">
</p>

4. Use the Rocket to launch a Job with this Template. ( This will install the modules on the local machine. )














