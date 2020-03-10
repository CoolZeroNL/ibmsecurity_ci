#!/bin/bash

export='awx_add_all_ci_playbooks_into_job_templates.yml'

echo "" > $export

cat <<EOT >> $export
- name: Add tower job template
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
    - name: Create tower job template - $stripedfilename
      tower_job_template:      
        tower_username: "{{admin_username}}"
        tower_password: "{{admin_password}}"
        tower_host: "{{tower_url}}"
        tower_verify_ssl: False   
        ####################################
        name: "CIC - $stripedfilename"
        # description:
        job_type: "run"
        project: "ibmsecurity_ci (master)"
        playbook: "ci-ansible-playbook-sample/$filename"
        ask_diff_mode: yes
        ask_extra_vars: yes
        ask_limit: yes
        ask_tags: yes
        ask_skip_tags: yes
        ask_job_type: yes
        ask_verbosity: yes
        ask_inventory: yes
        ask_credential: yes
        state: "present"

EOT

done
