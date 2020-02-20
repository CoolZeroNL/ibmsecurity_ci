import logging
import ibmsecurity.utilities.tools

logger = logging.getLogger(__name__)

def get_all_signercert(ciAppliance, check_mode=False, force=False):
    """
    Gets the list of all signer certs.
    """
    return ciAppliance.invoke_get("Retrieving signer certs", "/keyservice/v1.0/signercert")

def get_all_personalcert(ciAppliance, check_mode=False, force=False):
    """
    Gets the list of all personal certs.
    """
    return ciAppliance.invoke_get("Retrieving personal certs", "/keyservice/v1.0/personalcert")

def add_signercert(ciAppliance, 
               pemcertfile,
               pemcert, 
               label, 
               check_mode=False, force=False):

    """
    add signer cert. 
    """
   # Create base Json
    client_json = {
        "label": label,
    } 
    
    # if no pem is given, check if there is a file locate.
    if pemcert == '':
        if pemcertfile != '':
            import pem
            certs = pem.parse_file(pemcertfile)
            client_json['cert'] = str(certs[0])
            
    # check if pemcert is given.
    if pemcert != '':
        client_json['cert'] = pemcert

    return ciAppliance.invoke_post("add signer cert.", "/keyservice/v1.0/signercert", client_json)
        
    # if force is True:
    #     if check_mode is True:
    #         return ciAppliance.create_return_object(changed=True)
    #     else:
    #         return ciAppliance.invoke_post("add signer cert.","/keyservice/v1.0/signercert")

    return ciAppliance.create_return_object()


def add_personalcert(ciAppliance, 
               p12certfile,
               p12cert, 
               isdefault,
               password,
               label,
               check_mode=False, force=False):

    """
    add personal cert. 
    """
        
   # Create base Json
    client_json = {
        "isdefault": isdefault,
        "password": password,
    } 
    
    if p12cert == '':  
        if p12certfile != '':    
            import base64
            p12data = open(p12certfile, "rb").read()
            p12encoded = base64.b64encode(p12data).decode()
            client_json['cert'] = p12encoded
    
    if p12cert != '':
        client_json['cert'] = p12cert
            
    if label != '':
        client_json['label'] = label
            
    return ciAppliance.invoke_post("add personal cert.", "/keyservice/v1.0/personalcert", client_json)
        
    # if force is True:
    #     if check_mode is True:
    #         return ciAppliance.create_return_object(changed=True)
    #     else:
    #         return ciAppliance.invoke_post("add personal cert","/keyservice/v1.0/personalcert")

    return ciAppliance.create_return_object()
