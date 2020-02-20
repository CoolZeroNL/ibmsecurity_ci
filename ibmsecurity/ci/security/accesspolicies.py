import logging
import ibmsecurity.utilities.tools
# import os.path
# import urllib.parse
# import json
# import random
# import ast
# import itertools

logger = logging.getLogger(__name__)

def get_all(ciAppliance, check_mode=False, force=False):
    """
    Gets the list of all Access Policies.
    """
    return ciAppliance.invoke_get("Retrieving Attributes", "/v1.0/policyvault/accesspolicy")

