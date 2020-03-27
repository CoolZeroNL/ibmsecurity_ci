import logging
import ibmsecurity.utilities.tools
# import json

logger = logging.getLogger(__name__)

def get_all(ciAppliance, check_mode=False, force=False):
    """
    Gets the list of all API Clients.
    """
    return ciAppliance.invoke_get("Retrieving API Clients", "/v1.0/apiclients")

def resolve_name_to_id(ciAppliance, name):
    """
    resolve
    """ 
    name = name.lower()
    data = get_all(ciAppliance=ciAppliance)

    for node in data['data']['apiClients']:
        if node['clientName'].lower() == name:
            id = node['id']
            if id != '':    
                return id
            else:
                return None

def delete(ciAppliance, 
               clientName, 
               check_mode=False, force=False):

    """
    Delete api client. 
    """
    
    id = resolve_name_to_id(ciAppliance, clientName)  
    if id is None:
        # raise error
        from ibmsecurity.appliance.ibmappliance import IBMFatal
        raise IBMFatal("!! No API ClientName found!")      
    else:  
        return ciAppliance.invoke_delete("DELETE API Client", "/v1.0/apiclients/" + id)        
                
    # return ciAppliance.create_return_object()


def add(ciAppliance, 
               clientName, 
               new_clientName,
               enabled,
               entitlements,
               check_mode=False, force=False):

    """
    add api client. 
    """
   # Create base Json
    client_json = {
        "clientName": new_clientName if new_clientName else clientName,
        "enabled": enabled,
    } 
    
    # Build JSON
    ## Check if variable is pressent, if so append to json.     
    if entitlements != '':
        client_json['entitlements'] = entitlements  # input = [ "foo","bar".... ]

    # if force is True:
        #     if check_mode is True:
        #         return ciAppliance.create_return_object(changed=True)
        #     else:
        #         return ciAppliance.invoke_post("Add Attributes","v1.0/attributes")
        

    ## check if there is a API Clientname with the same name.
    id = resolve_name_to_id(ciAppliance, clientName)  
    if id is None:
        return ciAppliance.invoke_post("POST API Client", "/v1.0/apiclients", client_json)
    else:   
        return ciAppliance.invoke_put("PUT API Client", "/v1.0/apiclients/" + id, client_json)    
                
    # return ciAppliance.create_return_object()
