import json
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import logging
from .ibmappliance import IBMAppliance
from .ibmappliance import IBMError
from .ibmappliance import IBMFatal
from ibmsecurity.utilities import tools

try:
    basestring
except NameError:
    basestring = (str, bytes)

class CIAppliance(IBMAppliance):
    # def __init__(self, hostname, user, client_id, client_secret, lmi_port=443):
    def __init__(self, hostname, client_id, client_secret, header=None, lmi_port=443):

        self.logger = logging.getLogger(__name__)
        self.logger.debug('Creating an CIAppliance')

        if isinstance(lmi_port, basestring):
            self.lmi_port = int(lmi_port)
        else:
            self.lmi_port = lmi_port

        self.session = requests.session()
        self.client_id = client_id
        self.client_secret = client_secret
        self.header = header
        
        IBMAppliance.__init__(self, hostname, user=None)    # 
    
    def _url(self, uri):
        # Build up the URL
        url = "https://" + self.hostname + ":" + str(self.lmi_port) + uri
        self.logger.debug("Issuing request to: " + url)
        return url
    
    # New implemented for Requesting Access Token ###################################################################

    def check_arguments(self):        
        if self.client_id is None or self.client_id == '':
            raise IBMFatal("!! CLIENT_ID = none")
            
        if self.client_secret is None or self.client_secret == '':
            raise IBMFatal("!! CLIENT_SECRET = none")
      
    def fetch_access_token(self):
        self.check_arguments()

        data = {'grant_type':'client_credentials',
                'client_id':self.client_id,
                'client_secret':self.client_secret,
                'scope':'openid'} 

        # r = requests.post(url = 'https://'+ self.hostname +'/v1.0/endpoint/default/token', data = data) 
        r = requests.post(url=self._url('/v1.0/endpoint/default/token'), data = data, verify=False)
                
        if r.status_code == 200:
            data = r.json()
            access_token = data['access_token']
        else:
            raise IBMError("HTTP Return code: {0}".format(r.status_code), r.text)

        return access_token
                
    #######################################################################################################



    def _log_desc(self, description):
        if description != "":
            self.logger.info('*** ' + description + ' ***')

    def _suppress_ssl_warning(self):
        # Disable https warning because of non-standard certs on appliance
        try:
            self.logger.debug("Suppressing SSL Warnings.")
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        except AttributeError:
            self.logger.warning("load requests.packages.urllib3.disable_warnings() failed")

    def _process_response(self, return_obj, http_response, ignore_error):
        return_obj['rc'] = http_response.status_code

        # Examine the response.
        if (http_response.status_code == 403):
            self.logger.error("  Request failed: ")
            self.logger.error("     status code: {0}".format(http_response.status_code))
            if http_response.text != "":
                self.logger.error("     text: " + http_response.text)
            # Unconditionally raise exception to abort execution
            raise IBMFatal("HTTP Return code: {0}".format(http_response.status_code), http_response.text)
        elif (http_response.status_code != 200 and http_response.status_code != 204 and http_response.status_code != 201):
            self.logger.error("  Request failed: ")
            self.logger.error("     status code: {0}".format(http_response.status_code))
            if http_response.text != "":
                self.logger.error("     text: " + http_response.text)
            if not ignore_error:
                raise IBMError("HTTP Return code: {0}".format(http_response.status_code), http_response.text)
            return_obj['changed'] = False  # force changed to be False as there is an error
        else:
            return_obj['rc'] = 0

            # Handle if there was json on input but response was not in json format
        try:
            json_data = json.loads(http_response.text)
        except ValueError:
            return_obj['data'] = http_response.content
            return

        self.logger.debug("Status Code: {0}".format(http_response.status_code))
        if http_response.text != "":
            self.logger.debug("Text: " + http_response.content.decode("utf-8"))

        for key in http_response.headers:
            if key == 'g-type':
                if http_response.headers[key] == 'application/octet-stream; charset=UTF-8':
                    json_data = {}
                    return_obj.data = http_response.content
                    return

        if http_response.text == "":
            json_data = {}
        else:
            json_data = json.loads(http_response.text)

        return_obj['data'] = json_data

    def _process_connection_error(self, ignore_error, return_obj):
        if not ignore_error:
            self.logger.critical("Failed to connect to server.")
            raise IBMError("HTTP Return code: 502", "Failed to connect to server")
        else:
            self.logger.debug("Failed to connect to server.")
            return_obj['rc'] = 502

    def _process_warnings(self, uri, warnings=[]):
        # flag to indicate if processing needs to return and not continue
        return_call = False

        self.logger.debug("Warnings: {0}".format(warnings))
        return warnings, return_call

    def _invoke_request(self, func, description, uri, ignore_error, data={}, warnings=[]):
        """
        Send a request to the LMI.  This function is private and should not be
        used directly.  The invoke_get/invoke_put/etc functions should be used instead.
        """
        self._log_desc(description=description)

        warnings, return_call = self._process_warnings(uri=uri, warnings=warnings)
        return_obj = self.create_return_object(warnings=warnings)
        if return_call:
            return return_obj

        # There maybe some cases when header should be blank (not json)
        # default header usage: application/json = 400 | application/scim+json = 38
        # So default == application/json
        headers = {
            # 'Accept': 'text/html',
            'Content-type': 'application/json',
        }
        
        ## NEW
        access_token = self.fetch_access_token()

        if access_token:
            headers.update({
                'Authorization': 'Bearer {0}'.format(access_token),
            })       
              
        # this will overright the header, if applied in role
        if self.header:                 
            headers.update({
                'Content-type': self.header,
            })
                 
        self.logger.debug("Headers are: {0}".format(headers))
        ## END OF NEW

        # Process the input data into JSON
        json_data = json.dumps(data)
        # logging.debug(json_data)
                    
        self.logger.debug("Input Data: " + json_data)

        self._suppress_ssl_warning()

        try:
            if func == self.session.get or func == self.session.delete:

                if data != {}:
                    r = func(url=self._url(uri), data=json_data, verify=False, headers=headers)
                else:
                    r = func(url=self._url(uri), verify=False, headers=headers) 
            else:
                r = func(url=self._url(uri), data=json_data, verify=False, headers=headers)

            if func != self.session.get:
                return_obj['changed'] = True  # Anything but GET should result in change

            self._process_response(return_obj=return_obj, http_response=r, ignore_error=ignore_error)

        except requests.exceptions.ConnectionError:
            self._process_connection_error(ignore_error=ignore_error, return_obj=return_obj)

        return return_obj

    def invoke_put(self, description, uri, data, ignore_error=False, warnings=[]):
        """
        Send a PUT request to the LMI.
        """

        self._log_request("PUT", uri, description)
        response = self._invoke_request(self.session.put, description, uri, ignore_error, data, warnings=warnings)
        return response

    def invoke_post(self, description, uri, data, ignore_error=False, warnings=[]):
        """
        Send a POST request to the LMI.
        """

        self._log_request("POST", uri, description)
        response = self._invoke_request(self.session.post, description, uri, ignore_error, data, warnings=warnings)
        return response

    def invoke_post_files(self, description, uri, fileinfo, data, ignore_error=False, warnings=[], json_response=True, data_as_files=False):
        """
        Send multipart/form-data upload file request.
        """
        self._log_desc(description=description)

        warnings, return_call = self._process_warnings(uri=uri, warnings=warnings)
        return_obj = self.create_return_object(warnings=warnings)
        if return_call:
            return return_obj

        # Build up the URL and header information.
        if json_response:
            headers = {
                'Accept': 'application/json,text/html,application/xhtml+xml,application/xml'
            }
        else:
            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml'
            }
            
        ## NEW
        access_token = self.fetch_access_token()

        if access_token:
            headers.update({
                'Authorization': 'Bearer {0}'.format(access_token),
            })                   
            
        self.logger.debug("Headers are: {0}".format(headers))

        if data_as_files is False:
            files = list()
            for file2post in fileinfo:
                files.append((file2post['file_formfield'],
                              (tools.path_leaf(file2post['filename']), open(file2post['filename'], 'rb'),
                               file2post['mimetype'])))
        else:
            files = data

        self._suppress_ssl_warning()

        try:
            if data_as_files is False:
                r = self.session.post(url=self._url(uri=uri), data=data, files=files, verify=False, headers=headers)
            else:
                r = self.session.post(url=self._url(uri=uri), files=files, verify=False, headers=headers)
            return_obj['changed'] = True  # POST of file would be a change
            self._process_response(return_obj=return_obj, http_response=r, ignore_error=ignore_error)

        except requests.exceptions.ConnectionError:
            if not ignore_error:
                self.logger.critical("Failed to connect to server.")
                raise IBMError("HTTP Return code: 502", "Failed to connect to server")
            else:
                self.logger.debug("Failed to connect to server.")
                return_obj.rc = 502

        return return_obj


    def invoke_get(self, description, uri, ignore_error=False, warnings=[]):
        """
        Send a GET request to the LMI.
        """
        logging.debug('Send a GET request to the LMI.' + ' uri: ' + uri + ' desc: ' + description)
        
        self._log_request("GET", uri, description)

        response = self._invoke_request(self.session.get, description, uri, ignore_error, warnings=warnings)
        self._log_response(response)
        return response


    def invoke_get_file(self, description, uri, filename, no_headers=False, ignore_error=False, warnings=[]):
        """
        Invoke a GET request and download the response data to a file
        """
        self._log_desc(description=description)

        warnings, return_call = self._process_warnings(uri=uri, warnings=warnings)
        return_obj = self.create_return_object(warnings=warnings)
        if return_call:
            return return_obj
        
        # In some cases passing a header causes response to come back as JSON
        if no_headers is True:
            headers = {}
        else:
            headers = {
                'Accept': 'application/json,application/octet-stream'
            }
            
        ## NEW
        access_token = self.fetch_access_token()

        if access_token:
            headers.update({
                'Authorization': 'Bearer {0}'.format(access_token),
            })             
            
        self.logger.debug("Headers are: {0}".format(headers))

        self._suppress_ssl_warning()

        try:
            r = self.session.get(url=self._url(uri=uri), verify=False, stream=True, headers=headers)

            if (r.status_code != 200 and r.status_code != 204 and r.status_code != 201):
                self.logger.error("  Request failed: ")
                self.logger.error("     status code: {0}".format(r.status_code))
                if r.text != "":
                    self.logger.error("     text: " + r.text)
                if not ignore_error:
                    raise IBMError("HTTP Return code: {0}".format(r.status_code), r.text)
                else:
                    return_obj['rc'] = r.status_code
                    return_obj['data'] = {'msg': 'Unable to extract contents to file!'}
            else:
                with open(filename, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=1024):
                        if chunk:  # filter out keep-alive new chunks
                            f.write(chunk)
                return_obj['rc'] = 0
                return_obj['data'] = {'msg': 'Contents extracted to file: ' + filename}

        except requests.exceptions.ConnectionError:
            self._process_connection_error(ignore_error=ignore_error, return_obj=return_obj)

        except IOError:
            if not ignore_error:
                self.logger.critical("Failed to write to file: " + filename)
                raise IBMError("HTTP Return code: 999", "Failed to write to file: " + filename)
            else:
                self.logger.debug("Failed to write to file: " + filename)
                return_obj['rc'] = 999

        return return_obj


    def invoke_delete(self, description, uri, data={}, ignore_error=False, warnings=[]):
        """
        Send a DELETE request to the LMI.
        """
        self._log_request("DELETE", uri, description)
        if data != {}:
            self.logger.info("Input Data:{0}".format(data))
            response = self._invoke_request(self.session.delete, description, uri, ignore_error, data=data, warnings=warnings)
        else:
            response = self._invoke_request(self.session.delete, description, uri, ignore_error, warnings=warnings)
        self._log_response(response)
        return response

    def _log_request(self, method, url, desc):
        self.logger.debug("Request: %s %s desc=%s", method, url, desc)

    def _log_response(self, response):
        if response:
            # self.logger.debug("Response: %d", response.get('rc'))
            self.logger.debug("Response: %i %i warnings:%s",
                                response.get('rc'),
                                response.get('status_code'),
                                response.get('warnings'))
        else:
            self.logger.debug("Response: None")
