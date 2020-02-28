import logging
import ibmsecurity.utilities.tools
import os.path
# import urllib.parse
# import json

logger = logging.getLogger(__name__)

def add(awxAppliance, 
                name,
                job_type,
                inventory,
                project,
                playbook,
                verbosity,
                description,
                job_tags,
                skip_tags,
                custom_virtualenv,
                job_slice_count,
                timeout,
                become_enabled,
                allow_callbacks,
                enable_webhook,
                allow_simultaneous,
                use_fact_cache,
                host_config_key,
                ebhook_credential,
                forks,
                ask_diff_mode_on_launch,
                ask_scm_branch_on_launch,
                ask_tags_on_launch,
                ask_skip_tags_on_launch,
                ask_limit_on_launch,
                ask_job_type_on_launch,
                ask_verbosity_on_launch,
                ask_inventory_on_launch,
                ask_variables_on_launch,
                ask_credential_on_launch,
                extra_vars,
                survey_enabled,
                check_mode=False, force=False):

    """
    AWX - Add Inventory. 
    """
   # Create base Json
    client_json = {
        "name": name,
        "job_type": job_type,
        "inventory": inventory,
        "project": project,
        "playbook": playbook,
        "verbosity": verbosity,
    } 

    # Build JSON
    ## Check if variable is pressent, if so append to json.
    if description != '':
        client_json['description'] = description
        
    if job_tags != '':
        client_json['job_tags'] = job_tags
        
    if skip_tags != '':
        client_json['skip_tags'] = skip_tags
        
    if custom_virtualenv != '':
        client_json['custom_virtualenv'] = custom_virtualenv
        
    if job_slice_count != '':
        client_json['job_slice_count'] = job_slice_count
        
    if timeout != '':
        client_json['timeout'] = timeout
        
    if become_enabled != '':
        client_json['become_enabled'] = become_enabled  

    if allow_callbacks != '':
        client_json['allow_callbacks'] = allow_callbacks

    if enable_webhook != '':
        client_json['enable_webhook'] = enable_webhook
        
    if allow_simultaneous != '':
        client_json['allow_simultaneous'] = allow_simultaneous
        
    if use_fact_cache != '':
        client_json['use_fact_cache'] = use_fact_cache
        
    if host_config_key != '':
        client_json['host_config_key'] = host_config_key
        
    if ebhook_credential != '':
        client_json['ebhook_credential'] = ebhook_credential
        
    if forks != '':
        client_json['forks'] = forks
        
    if ask_diff_mode_on_launch != '':
        client_json['ask_diff_mode_on_launch'] = ask_diff_mode_on_launch

    if ask_scm_branch_on_launch != '':
        client_json['ask_scm_branch_on_launch'] = ask_scm_branch_on_launch
        
    if ask_tags_on_launch != '':
        client_json['ask_tags_on_launch'] = ask_tags_on_launch
        
    if ask_skip_tags_on_launch != '':
        client_json['ask_skip_tags_on_launch'] = ask_skip_tags_on_launch
        
    if ask_limit_on_launch != '':
        client_json['ask_limit_on_launch'] = ask_limit_on_launch
        
    if ask_job_type_on_launch != '':
        client_json['ask_job_type_on_launch'] = ask_job_type_on_launch
        
    if ask_verbosity_on_launch != '':
        client_json['ask_verbosity_on_launch'] = ask_verbosity_on_launch
        
    if ask_inventory_on_launch != '':
        client_json['ask_inventory_on_launch'] = ask_inventory_on_launch
        
    if ask_variables_on_launch != '':
        client_json['ask_variables_on_launch'] = ask_variables_on_launch
                                        
    if ask_credential_on_launch != '':
        client_json['ask_credential_on_launch'] = ask_credential_on_launch
                                              
    if extra_vars != '':
        client_json['extra_vars'] = extra_vars
                                        
    if survey_enabled != '':
        client_json['survey_enabled'] = survey_enabled
                                                                                                                                             
    return awxAppliance.invoke_patch("AWX - Add Template", "/api/v2/job_templates/", client_json)
        
    return awxAppliance.create_return_object()
    
