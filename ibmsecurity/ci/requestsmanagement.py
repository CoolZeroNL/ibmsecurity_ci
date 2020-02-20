import logging
import ibmsecurity.utilities.tools
# import os.path
# import urllib.parse
# import json
# import ast
# import itertools

logger = logging.getLogger(__name__)

def get_all(ciAppliance, check_mode=False, force=False):
    """
    Find all requestable applications in the catalog.
    """
    return ciAppliance.invoke_get("Find all requestable applications in the catalog.", "/v1.0/users/applications/catalog")

