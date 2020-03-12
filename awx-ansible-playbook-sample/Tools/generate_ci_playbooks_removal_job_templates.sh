#!/bin/bash

export='generated-awx_delete_all_ci_playbooks_from_job_template.yml'

echo "" > $export

cat <<EOT >> $export
- name: Delete tower job template
  hosts: "{{ hosts | default('all') }}"
  gather_facts: false
  connection: local
  tasks:
EOT


for OUTPUT in $(ls ../ci-ansible-playbook-sample/*.yml)
do
	filename=$(echo "$OUTPUT" | awk -F"/" '{print $3}')
	stripedfilename=$(echo "$OUTPUT" | awk -F"/" '{print $3}' | sed 's/.yml//g' | sed 's/_/ /g')
	echo "-----------------------------------"
  echo $filename



cat <<EOT >> $export
    - name: Delete tower job template - $stripedfilename
      tower_job_template:      
        tower_username: "{{admin_username}}"
        tower_password: "{{admin_password}}"
        tower_host: "{{tower_url}}"
        tower_verify_ssl: False   
        ####################################
        name: "CIC - $stripedfilename"
        project: "ibmsecurity_ci (master)"
        playbook: "null"
        state: "absent"

EOT

done
