import logging
import ibmsecurity.utilities.tools
# import os.path
# import urllib.parse
# import json

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
              
              
              
def add(ciAppliance, sourcetypeid, instancename, enabled, properties_client_id_sensitive, properties_client_id_value, properties_client_secret_sensitive, properties_client_secret_value, properties_identitylinkingenabled_sensitive, properties_identitylinkingenabled_value, properties_identitylinkingjitenabled_sensitive, properties_identitylinkingjitenabled_value, properties_identitylinkingprincipalattribute_sensitive, properties_identitylinkingprincipalattribute_value, properties_realm_sensitive, properties_realm_value, check_mode=False, force=False):
    """
    Add a Identity Source.
    """
    # todo:
    # - add nice check
    # - add 

   # Create base Json
    client_json = {
        "sourceTypeId": sourcetypeid,
        "instanceName": instancename,
        "enabled": enabled,
        "properties": [{
            "sensitive": properties_realm_sensitive,
            "key": "realm",
            "value": properties_realm_value
        }, {
            "sensitive": properties_client_id_sensitive,
            "key": "client_id",
            "value": properties_client_id_value
        }, {
            "sensitive": properties_client_secret_sensitive,
            "key": "client_secret",
            "value": properties_client_secret_value
        }, {
            "sensitive": properties_identitylinkingenabled_sensitive,
            "key": "identityLinkingEnabled",
            "value": properties_identitylinkingenabled_value
        }, {
            "sensitive": properties_identitylinkingprincipalattribute_sensitive,
            "key": "identityLinkingPrincipalAttribute",
            "value": properties_identitylinkingprincipalattribute_value
        }, {
            "sensitive": properties_identitylinkingjitenabled_sensitive,
            "key": "identityLinkingJitEnabled",
            "value": properties_identitylinkingjitenabled_value
        }]        
    } 
    
    # build JSON for Bookmarks & Salesforce
    ## Check if variable is pressent, if so append to json.
    # if customicon != '':
    #     client_json['customIcon'] = customicon
    
    return ciAppliance.invoke_post("add identity source", "/v1.0/identitysources", client_json)
    
    return ciAppliance.create_return_object()        