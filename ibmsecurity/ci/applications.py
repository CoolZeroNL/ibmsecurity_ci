import logging
import ibmsecurity.utilities.tools
import os.path
import urllib.parse
import json
# import ast
# import itertools

logger = logging.getLogger(__name__)

# def listToStringWithoutBrackets(list1):
#     return str(list1).replace('[','').replace(']','').replace("'", '"')


def get_all(ciAppliance, check_mode=False, force=False):
    """
    Gets the list of all applications.
    """
    return ciAppliance.invoke_get("Retrieving applications", "/v1.0/applications")

def resolve_name_to_id(ciAppliance, appname):
    """
    resolve
    """ 
    appname = appname.lower()
    
    # Find app id:
    app_data = get_all(ciAppliance=ciAppliance)
    for node in app_data['data']['_embedded']['applications']:
        if node['name'].lower() == appname:
            ref = node['_links']['self']['href']
            appid = os.path.basename(os.path.normpath(ref))
            if appid != '':    
                return appid
            else:
                return None
            
def delete(ciAppliance, appname, check_mode=False, force=False):
    """
    delete app. 
    """   
    # convert the name of the app to lowercase.
    appname = appname.lower()

    #resolve appname id
    appid = resolve_name_to_id(ciAppliance, appname)
    
    # check result resolving appname to id, if not none
    if appid is not None:
        return ciAppliance.invoke_delete("Delete a application", "/v1.0/applications/" + appid)
    else:
        from ibmsecurity.appliance.ibmappliance import IBMFatal
        raise IBMFatal("Application dont exist!")  
    
    return ciAppliance.create_return_object()


def add(ciAppliance, 
               entitlement, 
               visibleonlaunchpad, 
               applicationstate, 
               templateid, 
               appname, 
               new_appname, 
               description, 
               providers_saml_properties_signauthnresponse, 
               providers_saml_properties_signaturealgorithm, 
               providers_saml_properties_defaultnameidformat, 
               providers_saml_assertionconsumerservice_url, 
               providers_saml_assertionconsumerservice_default, 
               providers_saml_assertionconsumerservice_index, 
               providers_oidc_restrictscopes, 
               providers_oidc_properties_granttypes_authorizationcode, 
               providers_oidc_properties_granttypes_implicit, 
               providers_oidc_properties_granttypes_deviceflow, 
               providers_oidc_properties_granttypes_ropc, 
               providers_oidc_properties_donotgenerateclientsecret, 
               providers_oidc_properties_generaterefreshtoken, 
               providers_oidc_properties_sendallknownuserattributes, 
               providers_oidc_properties_accesstokenexpiry, 
               providers_oidc_properties_idtokensigningalg, 
               providers_oidc_properties_redirecturis, 
               providers_oidc_token_accesstokentype, 
               providers_oidc_token_audiences, 
               providers_oidc_token_attributemappings, 
               providers_oidc_requirepkceverification, 
               providers_oidc_consentaction, 
               providers_oidc_applicationurl, 
               providers_oidc_scopes, 
               providers_oidc_restrictentitlements, 
               providers_oidc_entitlements,
               providers_saml_justintimeprovisioning, 
               providers_saml_properties_companyname, 
               providers_saml_properties_providerid, 
               providers_saml_properties_generateuniqueid, 
               providers_saml_properties_validateauthnrequest, 
               providers_saml_properties_encryptassertion, 
               providers_saml_properties_ici_reserved_subjectnameid, 
               providers_saml_properties_includeallattributes, 
               providers_saml_properties_assertionconsumerserviceurl, 
               providers_sso_domainname, 
               providers_sso_useroptions, 
               providers_sso_idpinitiatedssosupport,
               providers_sso_spssourl,                
               providers_bookmarkurl, 
               customicon,      
               attributemappings,
               target_connectedapp,
               themeid,
               provpolicy,
               deprovpolicy,
               deprovpction,
               graceperiod,
               provisionattributemappings,               
               provisionbearertoken,
               provisionscimbaseurl,
               authpolicy,
               check_mode=False, force=False):

    """
    add custom app bookmark. 
    """
   # Create base Json
    client_json = {
        "visibleOnLaunchpad": visibleonlaunchpad,
        'name': new_appname if new_appname else appname,
        "applicationState": applicationstate,
        "description": description,
        "templateId": templateid,
    } 
    
    # Build JSON
    ## Check if variable is pressent, if so append to json.
    if customicon != '':
        client_json['customIcon'] = customicon

    if attributemappings != '':
        # logging.debug('attributemappings == availible')
        client_json['attributeMappings'] = []
        for element in attributemappings:
            client_json['attributeMappings'].append({"targetName":element["targetName"], "sourceId":element["sourceId"], "targetAttrFormat":element["targetAttrFormat"]})

    if authpolicy != '':
       client_json['authPolicy'] = {}
       authpolicy_id = authpolicy[0]['id']
       authpolicy_name = authpolicy[0]['name']
           if authpolicy_id != '' and authpolicy_name != '':
              client_json['authPolicy']['id'] = authpolicy_id
              client_json['authPolicy']['name'] = authpolicy_name
	
    ## if Govern is active.....
    if provpolicy != '' and \
       deprovpolicy != '' and \
       deprovpction != '' and \
       graceperiod != '':
           client_json['provisioning'] = { }
           
           if provisionscimbaseurl != '' or \
              provisionbearertoken != '':
                  client_json['provisioning']['extension'] = {}
                  client_json['provisioning']['extension']['properties'] = {}
                  client_json['provisioning']['extension']['properties']['endpointBaseUrl'] = provisionscimbaseurl
                  client_json['provisioning']['authentication'] = {}
                  client_json['provisioning']['authentication']['properties'] = {}
                  client_json['provisioning']['authentication']['properties']['pwd_token'] = provisionbearertoken
                             
           client_json['provisioning']['policies'] = { }
           client_json['provisioning']['policies']['provPolicy'] = provpolicy
           client_json['provisioning']['policies']['deProvPolicy'] = deprovpolicy
           client_json['provisioning']['policies']['deProvAction'] = deprovpction
           client_json['provisioning']['policies']['gracePeriod'] = graceperiod
                  
           client_json['provisioning']['attributeMappings'] = []
           if provisionattributemappings != '':
               for element in provisionattributemappings:
                   client_json['provisioning']['attributeMappings'].append({"targetName":element["targetName"], "sourceId":element["sourceId"]})
                
    if target_connectedapp != '':
        client_json['target'] = target_connectedapp[0]
    
    # https://community.ibm.com/community/user/security/blogs/meenakshi-kumari1/2020/01/17/theme-management-ibm-cloud-identity?CommunityKey=e7c36119-46d7-42f2-97a9-b44f0cc89c6d&tab=recentcommunityblogsdashboard    
    if themeid != '':
        client_json['customization'] = {}
        client_json['customization']['themeId'] = themeid
        
    if providers_saml_properties_companyname != '' or \
       providers_saml_properties_providerid != '' or \
       providers_saml_properties_generateuniqueid != '' or \
       providers_saml_properties_validateauthnrequest != '' or \
       providers_saml_properties_encryptassertion != '' or \
       providers_saml_properties_ici_reserved_subjectnameid != '' or \
       providers_saml_properties_includeallattributes != '' or \
       providers_saml_properties_assertionconsumerserviceurl != '' or \
       providers_sso_useroptions != '' or \
       providers_sso_idpinitiatedssosupport != '' or \
       providers_sso_domainname != '' or \
       providers_saml_properties_signauthnresponse != '' or \
       providers_saml_properties_signaturealgorithm != '' or \
       providers_saml_properties_defaultnameidformat != '' or \
       providers_saml_justintimeprovisioning != '':
        client_json['providers'] = { }
        
        if providers_sso_spssourl != '' or providers_sso_domainname != '' or providers_sso_idpinitiatedssosupport != '' or providers_sso_domainname != '':
            client_json['providers']['sso'] = { }
       
            if providers_sso_spssourl != '':
                client_json['providers']['sso']['spssoUrl'] = providers_sso_spssourl

            if providers_sso_useroptions != '':
                client_json['providers']['sso']['userOptions'] = providers_sso_useroptions
            
            if providers_sso_idpinitiatedssosupport != '':
                client_json['providers']['sso']['idpInitiatedSSOSupport'] = providers_sso_idpinitiatedssosupport

            if providers_sso_domainname != '':
                client_json['providers']['sso']['domainName'] = providers_sso_domainname           
        
        if providers_bookmarkurl != '':
            client_json['providers']['bookmark'] = { }
            client_json['providers']['bookmark']['bookmarkUrl'] =providers_bookmarkurl
              
        if providers_saml_properties_companyname != '' or \
           providers_saml_properties_providerid != '' or \
           providers_saml_properties_generateuniqueid != '' or \
           providers_saml_properties_validateauthnrequest != '' or \
           providers_saml_properties_encryptassertion != '' or \
           providers_saml_properties_ici_reserved_subjectnameid != '' or \
           providers_saml_properties_includeallattributes != '' or \
           providers_saml_properties_assertionconsumerserviceurl != '' or  \
           providers_sso_useroptions != '' or \
           providers_sso_idpinitiatedssosupport != '' or \
           providers_saml_properties_signauthnresponse != '' or \
           providers_saml_properties_signaturealgorithm != '' or \
           providers_saml_properties_defaultnameidformat != '' or \
           providers_saml_justintimeprovisioning != '':
            client_json['providers']['saml'] = { }
            
            if providers_saml_justintimeprovisioning != '':
                client_json['providers']['saml']['justInTimeProvisioning'] = providers_saml_justintimeprovisioning
    
        if providers_saml_properties_companyname != '' or \
           providers_saml_properties_providerid != '' or \
           providers_saml_properties_generateuniqueid != '' or \
           providers_saml_properties_validateauthnrequest != '' or \
           providers_saml_properties_encryptassertion != '' or \
           providers_saml_properties_ici_reserved_subjectnameid != '' or \
           providers_saml_properties_includeallattributes != '' or \
           providers_saml_properties_assertionconsumerserviceurl != '' or  \
           providers_sso_useroptions != '' or \
           providers_saml_properties_signauthnresponse != '' or \
           providers_saml_properties_signaturealgorithm != '' or \
           providers_saml_properties_defaultnameidformat != '' or \
           providers_sso_idpinitiatedssosupport != '':
            client_json['providers']['saml']['properties'] = { }
                
            if providers_saml_properties_companyname != '':
                client_json['providers']['saml']['properties']['companyName'] = providers_saml_properties_companyname
        
            if providers_saml_properties_providerid != '':
                client_json['providers']['saml']['properties']['providerId'] = providers_saml_properties_providerid
                
            if providers_saml_properties_generateuniqueid != '':
                client_json['providers']['saml']['properties']['generateUniqueID'] = providers_saml_properties_generateuniqueid
            
            if providers_saml_properties_validateauthnrequest != '':
                client_json['providers']['saml']['properties']['validateAuthnRequest'] = providers_saml_properties_validateauthnrequest
            
            if providers_saml_properties_encryptassertion != '':
                client_json['providers']['saml']['properties']['encryptAssertion'] = providers_saml_properties_encryptassertion
            
            if providers_saml_properties_ici_reserved_subjectnameid != '':
                client_json['providers']['saml']['properties']['ici_reserved_subjectNameID'] = providers_saml_properties_ici_reserved_subjectnameid
            
            if providers_saml_properties_includeallattributes != '':
                client_json['providers']['saml']['properties']['includeAllAttributes'] = providers_saml_properties_includeallattributes
            
            if providers_saml_properties_assertionconsumerserviceurl != '':
                client_json['providers']['saml']['properties']['assertionConsumerServiceUrl'] = providers_saml_properties_assertionconsumerserviceurl
                
            if providers_saml_properties_signauthnresponse != '':
                client_json['providers']['saml']['properties']['signAuthnResponse'] = providers_saml_properties_signauthnresponse  
                
            if providers_saml_properties_signaturealgorithm != '':
                client_json['providers']['saml']['properties']['signatureAlgorithm'] = providers_saml_properties_signaturealgorithm                      

            if providers_saml_properties_defaultnameidformat != '':
                client_json['providers']['saml']['properties']['defaultNameIdFormat'] = providers_saml_properties_defaultnameidformat                      

        if providers_saml_assertionconsumerservice_url != '' or \
           providers_saml_assertionconsumerservice_default != '' or \
           providers_saml_assertionconsumerservice_index != '':
            client_json['providers']['saml']['assertionConsumerService'] = [{
                "url": providers_saml_assertionconsumerservice_url,
				"default": providers_saml_assertionconsumerservice_default,
				"index": providers_saml_assertionconsumerservice_index
                }]   


        if providers_oidc_properties_granttypes_authorizationcode != '' or \
           providers_oidc_properties_granttypes_implicit != '' or \
           providers_oidc_properties_granttypes_deviceflow != '' or \
           providers_oidc_properties_granttypes_ropc != '' or \
           providers_oidc_properties_donotgenerateclientsecret != '' or \
           providers_oidc_properties_generaterefreshtoken != '' or \
           providers_oidc_properties_sendallknownuserattributes != '' or \
           providers_oidc_properties_accesstokenexpiry != '' or \
           providers_oidc_properties_idtokensigningalg != '' or \
           providers_oidc_properties_redirecturis != '' or \
           providers_oidc_token_accesstokentype != '' or \
           providers_oidc_token_audiences != '' or \
           providers_oidc_token_attributemappings != '' or \
           providers_oidc_requirepkceverification != '' or \
           providers_oidc_consentaction != '' or \
           providers_oidc_applicationurl != '' or \
           providers_oidc_scopes != '' or \
           providers_oidc_restrictentitlements != '' or \
           providers_oidc_entitlements != '' or \
           providers_oidc_restrictscopes != '':
            client_json['providers']['oidc'] = { }

            if providers_oidc_restrictscopes != '':
                client_json['providers']['oidc']['restrictScopes'] = providers_oidc_restrictscopes                      

            if providers_oidc_requirepkceverification != '':
                client_json['providers']['oidc']['requirePkceVerification'] = providers_oidc_requirepkceverification
                        
            if providers_oidc_consentaction != '':
                client_json['providers']['oidc']['consentAction'] = providers_oidc_consentaction
                        
            if providers_oidc_applicationurl != '':
                client_json['providers']['oidc']['applicationUrl'] = providers_oidc_applicationurl
                        
            if providers_oidc_scopes != '':
                client_json['providers']['oidc']['scopes'] = providers_oidc_scopes              # input = [ "foo","bar".... ]
                      
            if providers_oidc_restrictentitlements != '':
                client_json['providers']['oidc']['restrictEntitlements'] = providers_oidc_restrictentitlements
                        
            if providers_oidc_entitlements != '':
                client_json['providers']['oidc']['entitlements'] = providers_oidc_entitlements  # input = [ "foo","bar".... ]
            

            if providers_oidc_properties_granttypes_authorizationcode != '' or \
               providers_oidc_properties_granttypes_implicit != '' or \
               providers_oidc_properties_granttypes_deviceflow != '' or \
               providers_oidc_properties_granttypes_ropc != '' or \
               providers_oidc_properties_donotgenerateclientsecret != '' or \
               providers_oidc_properties_generaterefreshtoken != '' or \
               providers_oidc_properties_sendallknownuserattributes != '' or \
               providers_oidc_properties_accesstokenexpiry != '' or \
               providers_oidc_properties_idtokensigningalg != '' or \
               providers_oidc_properties_redirecturis != '':
                client_json['providers']['oidc']['properties'] = { }

                if providers_oidc_properties_donotgenerateclientsecret != '':
                    client_json['providers']['oidc']['properties']['doNotGenerateClientSecret'] = providers_oidc_properties_donotgenerateclientsecret  
                    
                if providers_oidc_properties_generaterefreshtoken != '':
                    client_json['providers']['oidc']['properties']['generateRefreshToken'] = providers_oidc_properties_generaterefreshtoken  
                    
                if providers_oidc_properties_sendallknownuserattributes != '':
                    client_json['providers']['oidc']['properties']['sendAllKnownUserAttributes'] = providers_oidc_properties_sendallknownuserattributes  
                    
                if providers_oidc_properties_accesstokenexpiry != '':
                    client_json['providers']['oidc']['properties']['accessTokenExpiry'] = providers_oidc_properties_accesstokenexpiry                                                      

                if providers_oidc_properties_idtokensigningalg != '':
                    client_json['providers']['oidc']['properties']['idTokenSigningAlg'] = providers_oidc_properties_idtokensigningalg                                                      

                if providers_oidc_properties_redirecturis != '':
                    client_json['providers']['oidc']['properties']['redirectUris'] = [ providers_oidc_properties_redirecturis ]

                if providers_oidc_properties_granttypes_authorizationcode != '' or \
                   providers_oidc_properties_granttypes_implicit != '' or \
                   providers_oidc_properties_granttypes_deviceflow != '' or \
                   providers_oidc_properties_granttypes_ropc != '':
                    client_json['providers']['oidc']['properties']['grantTypes'] = { }
                    
                    if providers_oidc_properties_granttypes_authorizationcode != '':
                        client_json['providers']['oidc']['properties']['grantTypes']['authorizationCode'] = providers_oidc_properties_granttypes_authorizationcode  
                   
                    if providers_oidc_properties_granttypes_implicit != '':
                        client_json['providers']['oidc']['properties']['grantTypes']['implicit'] = providers_oidc_properties_granttypes_implicit

                    if providers_oidc_properties_granttypes_deviceflow != '':
                        client_json['providers']['oidc']['properties']['grantTypes']['deviceFlow'] = providers_oidc_properties_granttypes_deviceflow
                        
                    if providers_oidc_properties_granttypes_ropc != '':
                        client_json['providers']['oidc']['properties']['grantTypes']['ropc'] = providers_oidc_properties_granttypes_ropc                        

            if providers_oidc_token_accesstokentype != '' or \
               providers_oidc_token_audiences != '' or \
               providers_oidc_token_attributemappings != '':
                client_json['providers']['oidc']['token'] = { }
                                        
                if providers_oidc_token_accesstokentype != '':
                    client_json['providers']['oidc']['token']['accessTokenType'] = providers_oidc_token_accesstokentype 
                                        
                if providers_oidc_token_audiences != '':
                    client_json['providers']['oidc']['token']['audiences'] = [ providers_oidc_token_audiences ]
                                                                        
                if providers_oidc_token_attributemappings != '':
                    client_json['providers']['oidc']['token']['attributeMappings'] = [ providers_oidc_token_attributemappings ]

    ## check if there is a app with the same name.
    appid = resolve_name_to_id(ciAppliance, appname)            
    if appid is None:
        
        # check
        if entitlement != '':
            ret_obj = ciAppliance.invoke_post("Add Application Entitlements", "/v1.0/applications", client_json)
            ref = ret_obj['data']['_links']['self']['href']
            appid = os.path.basename(os.path.normpath(ref))
                    
            from ibmsecurity.ci.entitlements import add as add_application_entitlements
            add_application_entitlements(ciAppliance=ciAppliance, appid=appid, entitlement=entitlement)
            
            return ret_obj
        
        else:
            return ciAppliance.invoke_post("Add Appliation", "/v1.0/applications", client_json)

    else:
        
        if entitlement != '':
            logging.debug("TODO: entitlement update")
        
        return ciAppliance.invoke_put("PUT Appliation", "/v1.0/applications/" + appid, client_json)    
            
    return ciAppliance.create_return_object()
    
