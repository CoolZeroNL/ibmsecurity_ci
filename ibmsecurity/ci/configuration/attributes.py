import logging
import ibmsecurity.utilities.tools
import os.path
import urllib.parse
import json
import random
# import ast
# import itertools

logger = logging.getLogger(__name__)

def get_all(ciAppliance, check_mode=False, force=False):
    """
    Gets the list of all Attributes.
    """
    return ciAppliance.invoke_get("Retrieving Attributes", "/v1.0/attributes")


def delete(ciAppliance, attributename, check_mode=False, force=False):
    """
    delete Attribute. 
    """   
    # convert the name of the attribute to lowercase.
    attributename = attributename.lower()
    
    # Find  id:
    attribute_data = get_all(ciAppliance=ciAppliance)

    for node in attribute_data['data']:       
        if node['name'].lower() == attributename:
            id = node['id']
            if id != '':    
                return ciAppliance.invoke_delete("Delete a Attribute", "/v1.0/attributes/" + id)
    
    return ciAppliance.create_return_object()

def add(ciAppliance, 
               attributename, 
               attributedescription, 
               sourcetype, 
               singlesignon, 
               attributeidentifier,
               datatype,
               scope,
               identitysource,
               attributenamefromtheidentitysource,
               value,
               applytransformation,
               check_mode=False, force=False):

    """
    add attribute. 
    """
   # Create base Json
    client_json = {
        "name": attributename,
        "description": attributedescription,
        "sourceType": sourcetype,
        "scope": scope,
        "datatype": datatype,
        "tags": [],
    } 
    
    # Build JSON
    ## Check if variable is pressent, if so append to json.
    if sourcetype != '':
        if sourcetype == 'schema':
            rand = random.randint(1,150)                    ## need fixing, find the latest nr of customAttribute[nn] and + 1
            client_json['schemaAttribute'] = { 
                "customAttribute": True,
		        "name": "customAttribute" + str(rand),
		        "scimName": attributeidentifier                               
            }
    
    if attributeidentifier != '':
        client_json['args'] = { }
        client_json['args']['name'] = attributeidentifier
        
    if singlesignon != '':
        client_json['tags'] = [ singlesignon ]

    if identitysource != '':
        client_json['credNameOverrides'] = { }
        client_json['credNameOverrides'][identitysource] = attributenamefromtheidentitysource
        
    if value != '':
        client_json['value'] = value

    if attributenamefromtheidentitysource != '':
        if identitysource == '':
            client_json['credName'] = attributenamefromtheidentitysource

    if applytransformation != '':
        client_json['function'] = { }
        client_json['function']['name'] = applytransformation

    return ciAppliance.invoke_post("Add Attributes", "/v1.0/attributes", client_json)
        
    # if force is True:
    #     if check_mode is True:
    #         return ciAppliance.create_return_object(changed=True)
    #     else:
    #         return ciAppliance.invoke_post("Add Attributes","v1.0/attributes")

    return ciAppliance.create_return_object()