import logging
import ibmsecurity.utilities.tools
# import os.path
# import urllib.parse
import json

logger = logging.getLogger(__name__)

def get(ciAppliance, appid, check_mode=False, force=False):
    """
    Get entitlements for an application.
    """
    if appid != '':
        return ciAppliance.invoke_get("Updates entitlements to an application.", "/v1.0/owner/applications/"+ appid +"/entitlements")
    else:
        from ibmsecurity.appliance.ibmappliance import IBMFatal
        raise IBMFatal("!! appid = none")           
        
def add(ciAppliance, appid, entitlement, check_mode=False, force=False):
    """
    Updates entitlements to an application.
    """
        
    # Map var to json. (all)
    entitlement_for = entitlement[0]['for']
    
    # declare var.
    client_json = {}

    if entitlement_for == "all":
    # govern: Automatic access for all users and groups
        logging.debug("all")
        client_json = {
            "birthRightAccess": True,
            "requestAccess": False,
            "additions": [],
            "deletions": []
        }        
    else:
        logging.debug("ELSE.... non of all above...")     
    
    if appid != '':
        return ciAppliance.invoke_post("Updates entitlements to an application.", "/v1.0/owner/applications/"+ appid +"/entitlements", client_json)
    else:
        from ibmsecurity.appliance.ibmappliance import IBMFatal
        raise IBMFatal("!! appid = none")           
        


