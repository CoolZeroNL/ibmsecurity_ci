import logging
import ibmsecurity.utilities.tools
import os.path
# import urllib.parse
# import json

logger = logging.getLogger(__name__)

def add(awxAppliance, 
               name,
               organization,
               variables,
               check_mode=False, force=False):

    """
    AWX - Add Inventory. 
    """
   # Create base Json
    client_json = {
        "name": name,
        "organization": organization,
        "scm_type": scm_type,
    } 

    # Build JSON
    ## Check if variable is pressent, if so append to json.
    if description != '':
        client_json['description'] = description

    if base_dir != '':
        client_json['base_dir'] = base_dir

    if scm_url != '':
        client_json['scm_url'] = scm_url
        
    if scm_branch != '':
        client_json['scm_branch'] = scm_branch
        
    if scm_refspec != '':
        client_json['scm_refspec'] = scm_refspec
        
    if scm_clean != '':
        client_json['scm_clean'] = scm_clean
        
    if scm_delete_on_update != '':
        client_json['scm_delete_on_update'] = scm_delete_on_update
        
    if scm_update_on_launch != '':
        client_json['scm_update_on_launch'] = scm_update_on_launch
        
    if allow_override != '':
        client_json['allow_override'] = allow_override
        
    if scm_update_cache_timeout != '':
        client_json['scm_update_cache_timeout'] = scm_update_cache_timeout
        
    if custom_virtualenv != '':
        client_json['custom_virtualenv'] = custom_virtualenv
                                                                                                         
    return awxAppliance.invoke_patch("AWX - Add Project", "/api/v2/projects/", client_json)
        
    return awxAppliance.create_return_object()
    
