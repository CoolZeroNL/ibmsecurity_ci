import logging
import ibmsecurity.utilities.tools
import json

logger = logging.getLogger(__name__)

def get_all(ciAppliance, check_mode=False, force=False):
    """
    Gets the list of all Identity Sources.
    """ 
    return ciAppliance.invoke_get("Retrieving Identity Sources", "/v1.0/identitysources")


# delete
# check if idenity source is provisiond 
    # Get ID of `idenity source`
        # Check each application if ID in "identitySources": [], is found.
              
def resolve_name_to_id(ciAppliance, name):
    """
    resolve
    """ 
    name = name.lower()
    data = get_all(ciAppliance=ciAppliance)

    for node in data['data']['identitySources']:
        if node['instanceName'].lower() == name:
            id = node['id']
            if id != '':    
                return id
            else:
                return None
                  
def nested_get(input_dict, nested_key):
    internal_dict_value = input_dict
    for k in nested_key:
        internal_dict_value = internal_dict_value.get(k, None)
        if internal_dict_value is None:
            return None
    return internal_dict_value

def add(ciAppliance, sourcetypeid, instancename, new_instancename, enabled, properties, check_mode=False, force=False):
    """
    Add a Identity Source.
    """

   # Create base Json
    client_json = {
        "sourceTypeId": sourcetypeid,
        "instanceName": new_instancename if new_instancename else instancename,
        "enabled": enabled,     
    } 
    
    if properties != '':
        client_json['properties'] = []      
        for item in properties:
            for key in item:
                client_json['properties'].append({
                    "sensitive": nested_get(item,[key,"sensitive"]),
		            "key": key,
		            "value": nested_get(item,[key,"value"])
                })
    
    # logging.debug("------")
    # logging.debug(client_json)
                        
    id = resolve_name_to_id(ciAppliance, instancename)
    if id is None:
        return ciAppliance.invoke_post("POST Identity source", "/v1.0/identitysources", client_json)
    else:
        return ciAppliance.invoke_put("PUT Identity Sources", "/v1.0/identitysources/" + id, client_json)    
            
    return ciAppliance.create_return_object()
    
