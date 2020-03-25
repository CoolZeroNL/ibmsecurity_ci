import logging
import ibmsecurity.utilities.tools
import os
import os.path
import shutil
import zipfile
import pathlib
import tempfile

logger = logging.getLogger(__name__)

def reset(ciAppliance, check_mode=False, force=False):
    """
    Reset template customizations
    Eliminate all template customizations for a tenant, effectively resetting back to the Out of the Box templates.
    
    Entitlements required: manageTemplates (Manage Templates)
    """
    
    if force is True:
        if check_mode is True:
            return ciAppliance.create_return_object(changed=True)
        else:
            return ciAppliance.invoke_delete("Reset template customizations","/v1.0/branding/reset")

    return ciAppliance.create_return_object()


def download(ciAppliance, filename, customized, check_mode=False, force=False):
    """
    Download all templates, in a compressed ZIP file format. Typically used to later provide customizations to templates using Upload API. Can choose to download Out of the Box templates, or Out of the Box template, with customizations overlaid.

    Entitlements required: manageTemplates (Manage Templates) or readTemplates (Read Templates)
    """
    logger.info("Downloading....")

    if force is True or (
            os.path.exists(filename) is False):  # Don't overwrite if not forced to
        
        uri=''
        if customized is True:  
            uri='?customized=true'
        else:
            uri='?customized=false'
        
        if check_mode is False:                                            
            # Download 
            return ciAppliance.invoke_get_file("Download templates","/v1.0/branding/download" + uri, filename)

    return ciAppliance.create_return_object()


def upload_zip(ciAppliance, file, check_mode=False, force=False):
    """
    Upload template customizations in a ZIP file. The entries in the ZIP file should be in the following format:

    /templates/<component>/<name>/<variant>/<locale>/<file_name>

    Entitlements required: manageTemplates (Manage Templates)
    """

    # if force is True:
    #     if check_mode is True:
    #         return ciAppliance.create_return_object(changed=True)
    #     else:
    return ciAppliance.invoke_post_files(
        "Upload template",
        "/v1.0/branding/upload",
        [{
            'file_formfield': 'uploadedfile',
            'filename': file,
            'mimetype': 'application/octet-stream'
        }],
        {"type":"formData"}, json_response=False)

    return ciAppliance.create_return_object()

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        logging.debug('Error: Creating directory. ' +  directory)

def deleteFolder(directory):
    try:
        if os.path.exists(directory):
            # os.rmdir(directory)
            shutil.rmtree(directory)
    except OSError:
        logging.debug('Error: Deleting directory. ' +  directory)
        
def upload_page(ciAppliance, pages, keepzip, check_mode=False, force=False):
    """
    Upload template customizations
    
        - for each page (html), regenerate folder structure, place a copy of the html
        - compress tmp folder, call upload (tmp file)
        - remove tmp folder & files
        - remove tmp templates.zip
        
        Todo:
        - fix location for windows ? windows dont have /tmp ?
        - 
    
    """
    with tempfile.TemporaryDirectory() as directory:
        logging.debug('The created temporary directory is %s' % directory)
            
        for page in pages:
            logging.debug(page)
            
            # todo:
            ## - check for `customization_templates` dir. if not download all templates, extract them under `customization_templates`, and cleanup
            
            file_name = os.path.basename(page['value']) 
            location = os.path.dirname(page['value'])
            split_loc = location.split('/')
            extension = ''.join(pathlib.Path(file_name).suffixes)

            # create a temporary directory
            # with tempfile.TemporaryDirectory() as directory:
            #     logging.debug('The created temporary directory is %s' % directory)
        
            logging.debug(file_name)
            logging.debug(location)
            logging.debug(split_loc)
            logging.debug(extension)
            
            # 
            templates_begin_dir = [ 'actions', 'authbroker', 'authsvc', 'certmgr', 'common', 'commonfim', 'factors', 'oidc', 'reqmgr', 'risk', 'saml20', 'USC', 'USC_LEGACY', 'USER_MGMT' ]
            logging.debug(templates_begin_dir)
            
            createFolder(directory+'/templates/')
            logging.debug(os.listdir(directory))
            
            # createFolder('./tmp/tmppages/')
            cur=''
            parse=''
            for folder in split_loc:
                logging.debug(folder)
                if folder in templates_begin_dir or parse == True: 
                    parse = True
                    if parse:
                        cur=cur+folder+"/"
                        logging.debug("cur, " + cur)
                        createFolder(directory + '/templates/' + cur)
            
            #copy custom page. file on desc need to be named: page.html
            if '.html' in extension:

                ary = file_name.split("_")
                first = ary[0]

                if first== 'header':
                    shutil.copy(location+'/'+file_name, directory+'/templates/'+cur+'/header.html')
                elif first== 'footer':
                    shutil.copy(location+'/'+file_name, directory+'/templates/'+cur+'/footer.html')
                elif first== 'page':
                    shutil.copy(location+'/'+file_name, directory+'/templates/'+cur+'/page.html')
                
            else:
                restore_filename = file_name.rsplit('_', 1)[0] + extension  # split at '_', starting from the right, maximum 1 split
                shutil.copy(location+'/'+file_name, directory+'/templates/'+cur+'/'+restore_filename)

            logging.debug("next")

        
        # shutil.move("./tmp/tmppages/customization_templates/", "./tmp/tmppages/templates/")
        cur_dirpath = os.getcwd()
        
        # Go to the tmp dir.
        os.chdir(directory)
        
        # Create zip
        zf = zipfile.ZipFile("templates.zip", "w")
        
        # Zip the content.        
        for dirname, subdirs, files in os.walk("./templates"):
            zf.write(dirname)
            for filename in files:
                zf.write(os.path.join(dirname, filename))
        zf.close()
        
        # upload
        upload_zip(ciAppliance=ciAppliance, file='templates.zip')
        
        # delete tmp folder
        # deleteFolder('./tmp/')
        if keepzip == True:
            shutil.copy(directory+'/templates.zip', cur_dirpath)
        #     os.remove("templates.zip")
        
        
        # Back to the ansible playbook dir..
        # os.chdir(cur_dirpath)

    return ciAppliance.create_return_object()
