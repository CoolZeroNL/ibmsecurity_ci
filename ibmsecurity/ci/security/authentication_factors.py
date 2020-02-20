import logging
import ibmsecurity.utilities.tools
# import os.path
# import urllib.parse
# import json

logger = logging.getLogger(__name__)

# To do:
## - build nice checks
## - build nice json payload, single item cant be updated, not all the items need to be present.     
      
      
def update_emailotp(ciAppliance, charset, maxtries, lifetimesec, length, enablevalidationonenroll, enabled, check_mode=False, force=False):
    """
    Updates the properties for specified authentication methods. 
    """
    # Create base Json
    client_json = {
        "charSet": charset,
        "maxTries": maxtries,
        "lifeTimeSec": lifetimesec,
        "length": length,
        "enableValidationOnEnroll": enablevalidationonenroll,
        "enabled": enabled
    }
    
    # Check
    if charset == '' or \
       maxtries == '' or \
       lifetimesec == '' or \
       length == '' or \
       enablevalidationonenroll == '' or \
       enabled == '':
        from ibmsecurity.appliance.ibmappliance import IBMFatal
        raise IBMFatal("!! one of the needed var is needed = none") 
    else:
        return ciAppliance.invoke_put(
            "update emailotp", "/v1.0/authnconfig/authnmethods/emailotp/properties", client_json)
    
    return ciAppliance.create_return_object()
          
      
def update_smsotp(ciAppliance, charset, maxtries, lifetimesec, length, enablevalidationonenroll, enabled, check_mode=False, force=False):
    """
    Updates the properties for specified authentication methods. 
    """
    # Create base Json
    client_json = {
        "charSet": charset,
        "maxTries": maxtries,
        "lifeTimeSec": lifetimesec,
        "length": length,
        "enableValidationOnEnroll": enablevalidationonenroll,
        "enabled": enabled
    }
    
    # Check
    if charset == '' or \
       maxtries == '' or \
       lifetimesec == '' or \
       length == '' or \
       enablevalidationonenroll == '' or \
       enabled == '':
        from ibmsecurity.appliance.ibmappliance import IBMFatal
        raise IBMFatal("!! one of the needed var is needed = none") 
    else:
        return ciAppliance.invoke_put(
            "update smsotp", "/v1.0/authnconfig/authnmethods/smsotp/properties", client_json)
    
    return ciAppliance.create_return_object()
          
          
def update_totp(ciAppliance, timestepskew, secretkeyurl, length, onetimeuse, timestepsizesec, enabled, algorithm, check_mode=False, force=False):
    """
    Updates the properties for specified authentication methods. 
    """
    # Create base Json
    client_json = {
        "timeStepSkew": timestepskew,
        "secretKeyUrl": secretkeyurl,
        "length": length,
        "oneTimeUse": onetimeuse,
        "timeStepSizeSec": timestepsizesec,
        "enabled": enabled,
        "algorithm": algorithm
    }
    
    # Check
    if timestepskew == '' or \
       secretkeyurl == '' or \
       length == '' or \
       onetimeuse == '' or \
       timestepsizesec == '' or \
       enabled == '' or \
       algorithm == '':
        from ibmsecurity.appliance.ibmappliance import IBMFatal
        raise IBMFatal("!! one of the needed var is needed = none") 
    else:
        return ciAppliance.invoke_put(
            "update totp", "/v1.0/authnconfig/authnmethods/totp/properties", client_json)
    
    return ciAppliance.create_return_object()



                
def update_verify(ciAppliance, face_supportedalgorithms, face_enabled, face_algorithm, userpresence_supportedalgorithms, userpresence_enabled, userpresence_algorithm, fingerprint_supportedalgorithms, fingerprint_enabled, fingerprint_algorithm, enabled, check_mode=False, force=False):
    """
    Updates the properties for specified authentication methods. 
    """
    # Create base Json
    client_json = {
        "face": {
            "supportedAlgorithms": face_supportedalgorithms,
            "enabled": face_enabled,
            "algorithm": face_algorithm
        },
        "userPresence": {
            "supportedAlgorithms": userpresence_supportedalgorithms,
            "enabled": userpresence_enabled,
            "algorithm": userpresence_algorithm
        },
        "fingerprint": {
            "supportedAlgorithms": fingerprint_supportedalgorithms,
            "enabled": fingerprint_enabled,
            "algorithm": fingerprint_algorithm
        },
        "enabled": enabled        
    }
    
    # Check
    if face_supportedalgorithms == '' or \
       face_enabled == '' or \
       face_algorithm == '' or \
       userpresence_supportedalgorithms == '' or \
       userpresence_enabled == '' or \
       userpresence_algorithm == '' or \
       fingerprint_supportedalgorithms == '' or \
       fingerprint_enabled == '' or \
       fingerprint_algorithm == '' or \
       enabled == '':
        from ibmsecurity.appliance.ibmappliance import IBMFatal
        raise IBMFatal("!! one of the needed var is needed = none") 
    else:
        return ciAppliance.invoke_put(
            "update verify", "/v1.0/authnmethods/signature", client_json)
    
    return ciAppliance.create_return_object()
          
      
                                            
def update_qr(ciAppliance, lsi_charset, lsi_length, dsi_charset, dsi_length, expiry, enabled, check_mode=False, force=False):
    """
    Updates the properties for specified authentication methods. 
    """
    # Create base Json
    client_json = {
        "lsi": {
            "charset": lsi_charset,
            "length": lsi_length
        },
        "dsi": {
            "charset": dsi_charset,
            "length": dsi_length
        },
        "expiry": expiry,
        "enabled": enabled  
    }
    
    # Check
    if lsi_charset == '' or \
       lsi_length == '' or \
       dsi_charset == '' or \
       dsi_length == '' or \
       expiry == '' or \
       enabled == '':
        from ibmsecurity.appliance.ibmappliance import IBMFatal
        raise IBMFatal("!! one of the needed var is needed = none") 
    else:
        return ciAppliance.invoke_put(
            "update verify", "/factors-mgmt/config/v2.0/factors/qr", client_json)
    
    return ciAppliance.create_return_object()
                            