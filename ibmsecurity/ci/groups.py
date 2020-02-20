import logging
import ibmsecurity.utilities.tools
import os.path
import urllib.parse

logger = logging.getLogger(__name__)

## Groups Management Version 2.0
## POST /v2.0/Groups                | Creates a group for a specified tenant. To create a group, a displayName is required. An optional Description attribute can be set to describe the group. A group can be created with or without members. When a group is created with members, a list of members needs to be passed in.

def get(ciAppliance, id, check_mode=False, force=False):
    """
    Get information on existing group
    """
    return ciAppliance.invoke_get("Retrieving group", "/v2.0/Groups/" + id)


def get_all(ciAppliance, check_mode=False, force=False):
    """
    Get information on existing groups
    """
    return ciAppliance.invoke_get("Retrieving groups", "/v2.0/Groups")

def add(ciAppliance, displayname, description, check_mode=False, force=False):
    """
    Creates a group in IBM Cloud Identity Cloud Directory. 
    """
   # Create base Json
    client_json = {
        "members": [],
        "schemas": ["urn:ietf:params:scim:schemas:core:2.0:Group", "urn:ietf:params:scim:schemas:extension:ibm:2.0:Group"]
    }
    # Add attributes that have been supplied, check if none raise error.
    if displayname != '':
        client_json['displayName'] = displayname
    else:
        from ibmsecurity.appliance.ibmappliance import IBMFatal
        raise IBMFatal("!! displayname = none") 
    
    if description is None or description != '':
        client_json['description'] = {
            "urn:ietf:params:scim:schemas:extension:ibm:2.0:Group": {
                "description": description
            }
            }
    else:
        client_json['description'] = {
            "urn:ietf:params:scim:schemas:extension:ibm:2.0:Group": {
                "description": ""
            }
            }
    
    return ciAppliance.invoke_post(
        "Creates a group in IBM Cloud Identity Cloud Directory.", "/v2.0/Groups", client_json)
    
    return ciAppliance.create_return_object()

def get_filter(ciAppliance, filter, check_mode=False, force=False):
    """
    Retrieves a list of users and match the search filter criteria.
    """
    if filter == '':
        from ibmsecurity.appliance.ibmappliance import IBMFatal
        raise IBMFatal("!! Filter = none")   
    
    return ciAppliance.invoke_get("Retrieving users", "/v2.0/Groups?filter=" + urllib.parse.quote(filter)) 

def add_user(ciAppliance, group, user, email, check_mode=False, force=False):
    """
    Add user to a group in IBM Cloud Identity Cloud Directory. 
    """   
    from ibmsecurity.ci.users import get_filter as get_user_filter
    import json
    
    # Find group:
    group_data = get_filter(ciAppliance=ciAppliance, filter='displayName eq \"'+ group +'\"')
    group_ids = [element['id'] for element in group_data['data']['Resources']]
    
    # add check if there are more the 1 id....
    if len(group_ids) > 1:
        from ibmsecurity.appliance.ibmappliance import IBMFatal
        raise IBMFatal("!! More Groups Found then 1 with the current filter")  
    
    group_fulldata = get(ciAppliance=ciAppliance, id=group_ids[0])
    group_members_ids = [element['id'] for element in group_fulldata['data']['members']]

    # Get current name of Group & Desc (so we cant change the name of the group...:S)
    displayname = group_fulldata['data']['displayName']
    description = group_fulldata['data']['urn:ietf:params:scim:schemas:extension:ibm:2.0:Group']['description']
         
    # Get User Data    
    user_data = get_user_filter(ciAppliance=ciAppliance, filter='name.formatted eq \"'+ user +'\" and emails.value eq \"'+ email +'\"')
    user_ids = [element['id'] for element in user_data['data']['Resources']]
    
    ## if not all users are listed here that are current in the group, this will replace them..
    # Create base Json
    client_json = {
        "id": group_ids[0],
        "displayName": displayname,
        "urn:ietf:params:scim:schemas:extension:ibm:2.0:Group": {
            "description": description
        },
        "members": [],
        "schemas": ["urn:ietf:params:scim:schemas:core:2.0:Group", "urn:ietf:params:scim:schemas:extension:ibm:2.0:Group"]
    }
    
    # Add attributes that have been supplied, check if none raise error.
    if group_members_ids != '':
        for i in group_members_ids: 
            client_json['members'].append({
                "type": "user",
                "value": i
                })
    
    if user_ids != '':            
       client_json['members'].append({
                "type": "user",
                "value": user_ids[0]
                })                
    
    return ciAppliance.invoke_put(
        "Add user to a group in IBM Cloud Identity Cloud Directory.", "/v2.0/Groups/" + group_ids[0], client_json)
    
    return ciAppliance.create_return_object()
  