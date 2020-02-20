import logging
import ibmsecurity.utilities.tools
import os.path
import json
import urllib.parse

logger = logging.getLogger(__name__)

## Users Management Version 2.0
def get_all(ciAppliance, check_mode=False, force=False):
    """
    Retrieves a list of users.
    """
    return ciAppliance.invoke_get("Retrieving users", "/v2.0/Users")

def get_filter(ciAppliance, filter, check_mode=False, force=False):
    """
    Retrieves a list of users and match the search filter criteria.
    """
    if filter == '':
        from ibmsecurity.appliance.ibmappliance import IBMFatal
        raise IBMFatal("!! Filter = none")   
    
    return ciAppliance.invoke_get("Retrieving users", "/v2.0/Users?filter=" + urllib.parse.quote(filter))

def add(ciAppliance, emails, username, givenname, familyname, phonenumbers, active, check_mode=False, force=False):
    """
    Creates a user in IBM Cloud Identity Cloud Directory. 
    Users are either created to use Cloud Directory as an identity source or as a just-in-time provisioning sequence when the user is authenticated at a remote identity source such as an enterprise authentication.
    """
   # Create base Json
    client_json = {
        "schemas": ["urn:ietf:params:scim:schemas:core:2.0:User", "urn:ietf:params:scim:schemas:extension:ibm:2.0:User", "urn:ietf:params:scim:schemas:extension:ibm:2.0:Notification"],
        
        "urn:ietf:params:scim:schemas:extension:ibm:2.0:User": {
            "userCategory": "regular"
            },
        
        "urn:ietf:params:scim:schemas:extension:ibm:2.0:Notification": {
            "notifyType": "EMAIL",
            "notifyManager": False
        }                  
    }
    
    # Add attributes that have been supplied, check if none raise error.
    if active != '':
        client_json['active'] = active
    else:
        from ibmsecurity.appliance.ibmappliance import IBMFatal
        raise IBMFatal("!! active = none") 
    
    if username != '':
        client_json['userName'] = username
    else:
        from ibmsecurity.appliance.ibmappliance import IBMFatal
        raise IBMFatal("!! userName = none") 
    
    if emails != '':
        client_json['emails'] = [{
            "type": "work",
            "value": emails
        }]
    else:
        from ibmsecurity.appliance.ibmappliance import IBMFatal
        raise IBMFatal("!! emails = none")

    if givenname != '' and familyname != '':
        client_json['name'] = {
            "givenName": givenname,
            "familyName": familyname
        }
    else:
        from ibmsecurity.appliance.ibmappliance import IBMFatal
        raise IBMFatal("!! givenName or familyName = none")

    if phonenumbers != '':
        client_json['phoneNumbers'] = [{
            "type": "mobile",
            "value": phonenumbers
        }]
    else:
        from ibmsecurity.appliance.ibmappliance import IBMFatal
        raise IBMFatal("!! phoneNumbers = none")
        
    # attr that are optional: #######################################3
    
    return ciAppliance.invoke_post(
        "Create an API protection definition", "/v2.0/Users", client_json)
    
    return ciAppliance.create_return_object()

    