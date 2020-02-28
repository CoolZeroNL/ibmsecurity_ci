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
        "variables": variables       
    } 
         
    return awxAppliance.invoke_patch("AWX - Add Inventory", "/api/v2/inventories/", client_json)
        
    return awxAppliance.create_return_object()
    
