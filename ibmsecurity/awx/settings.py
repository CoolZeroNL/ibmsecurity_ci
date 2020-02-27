import logging
import ibmsecurity.utilities.tools
import os.path
# import urllib.parse
# import json

logger = logging.getLogger(__name__)

def update(awxAppliance, 
               SOCIAL_AUTH_SAML_SP_ENTITY_ID,
               SOCIAL_AUTH_SAML_CALLBACK_URL,
               SOCIAL_AUTH_SAML_METADATA_URL,
               SOCIAL_AUTH_SAML_SP_PUBLIC_CERT,
               SOCIAL_AUTH_SAML_SP_PRIVATE_KEY,
               SOCIAL_AUTH_SAML_ORG_INFO,
               SOCIAL_AUTH_SAML_TECHNICAL_CONTACT,
               SOCIAL_AUTH_SAML_SUPPORT_CONTACT,
               SOCIAL_AUTH_SAML_ENABLED_IDPS,
               SOCIAL_AUTH_SAML_ORGANIZATION_MAP,
               SOCIAL_AUTH_SAML_ORGANIZATION_ATTR,
               SOCIAL_AUTH_SAML_TEAM_MAP,
               SOCIAL_AUTH_SAML_TEAM_ATTR,
               SOCIAL_AUTH_SAML_SECURITY_CONFIG,
               SOCIAL_AUTH_SAML_SP_EXTRA,
               SOCIAL_AUTH_SAML_EXTRA_DATA,
               check_mode=False, force=False):

    """
    AWX - Update Settings. 
    """
   # Create base Json
    client_json = {
        "SOCIAL_AUTH_SAML_SP_ENTITY_ID": SOCIAL_AUTH_SAML_SP_ENTITY_ID,       
    } 
    
    # Build JSON
    ## Check if variable is pressent, if so append to json.
    if SOCIAL_AUTH_SAML_CALLBACK_URL != '':
        client_json['SOCIAL_AUTH_SAML_CALLBACK_URL'] = SOCIAL_AUTH_SAML_CALLBACK_URL

    if SOCIAL_AUTH_SAML_METADATA_URL != '':
        client_json['SOCIAL_AUTH_SAML_METADATA_URL'] = SOCIAL_AUTH_SAML_METADATA_URL

    if SOCIAL_AUTH_SAML_SP_PUBLIC_CERT != '':
        client_json['SOCIAL_AUTH_SAML_SP_PUBLIC_CERT'] = SOCIAL_AUTH_SAML_SP_PUBLIC_CERT

    if SOCIAL_AUTH_SAML_SP_PRIVATE_KEY != '':
        client_json['SOCIAL_AUTH_SAML_SP_PRIVATE_KEY'] = SOCIAL_AUTH_SAML_SP_PRIVATE_KEY

    if SOCIAL_AUTH_SAML_ORG_INFO != '':
        client_json['SOCIAL_AUTH_SAML_ORG_INFO'] = SOCIAL_AUTH_SAML_ORG_INFO

    if SOCIAL_AUTH_SAML_TECHNICAL_CONTACT != '':
        client_json['SOCIAL_AUTH_SAML_TECHNICAL_CONTACT'] = SOCIAL_AUTH_SAML_TECHNICAL_CONTACT

    if SOCIAL_AUTH_SAML_SUPPORT_CONTACT != '':
        client_json['SOCIAL_AUTH_SAML_SUPPORT_CONTACT'] = SOCIAL_AUTH_SAML_SUPPORT_CONTACT

    if SOCIAL_AUTH_SAML_ENABLED_IDPS != '':
        client_json['SOCIAL_AUTH_SAML_ENABLED_IDPS'] = SOCIAL_AUTH_SAML_ENABLED_IDPS

    if SOCIAL_AUTH_SAML_ORGANIZATION_MAP != '':
        client_json['SOCIAL_AUTH_SAML_ORGANIZATION_MAP'] = SOCIAL_AUTH_SAML_ORGANIZATION_MAP

    if SOCIAL_AUTH_SAML_ORGANIZATION_ATTR != '':
        client_json['SOCIAL_AUTH_SAML_ORGANIZATION_ATTR'] = SOCIAL_AUTH_SAML_ORGANIZATION_ATTR

    if SOCIAL_AUTH_SAML_TEAM_MAP != '':
        client_json['SOCIAL_AUTH_SAML_TEAM_MAP'] = SOCIAL_AUTH_SAML_TEAM_MAP
        
    if SOCIAL_AUTH_SAML_TEAM_ATTR != '':
        client_json['SOCIAL_AUTH_SAML_TEAM_ATTR'] = SOCIAL_AUTH_SAML_TEAM_ATTR
        
    if SOCIAL_AUTH_SAML_SECURITY_CONFIG != '':
        client_json['SOCIAL_AUTH_SAML_SECURITY_CONFIG'] = SOCIAL_AUTH_SAML_SECURITY_CONFIG
        
    if SOCIAL_AUTH_SAML_SP_EXTRA != '':
        client_json['SOCIAL_AUTH_SAML_SP_EXTRA'] = SOCIAL_AUTH_SAML_SP_EXTRA
        
    if SOCIAL_AUTH_SAML_EXTRA_DATA != '':
        client_json['SOCIAL_AUTH_SAML_EXTRA_DATA'] = SOCIAL_AUTH_SAML_EXTRA_DATA
         
    return awxAppliance.invoke_patch("AWX - Update Settings", "/api/v2/settings/all/", client_json)
        
    # if force is True:
    #     if check_mode is True:
    #         return ciAppliance.create_return_object(changed=True)
    #     else:
    #         return ciAppliance.invoke_post("Add Attributes","v1.0/attributes")

    return awxAppliance.create_return_object()
    
