import logging
import ibmsecurity.utilities.tools
# import os.path
# import urllib.parse

import json
# from dictor import dictor

logger = logging.getLogger(__name__)

                  
def flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name)
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out                              

def update(ciAppliance, properties, schemas, check_mode=False, force=False):
    """
    Update Password Policies for a Identity Source.
    """
   # Create base Json
    client_json = {} 
        
    if properties != '':
        client_json = properties    
    
    # Flatten json        
    flat = flatten_json(client_json)

    if schemas != '':
        flat['schemas'] = [schemas]                        
   
    return ciAppliance.invoke_put("PUT Password Policies Identity Sources", "/v2.0/PasswordPolicies", flat)    
            
    return ciAppliance.create_return_object()
    
