import logging
import ibmsecurity.utilities.tools
import os.path

logger = logging.getLogger(__name__)

## Users Management Version 2.0
## Groups Management Version 2.0
# GET /v2.0/CSV/headerNames       | Get the list of supported header names.

## Implementation Notes
# The names that are returned can be used as the headers for the CSV file.
# The filter query parameter supports the options:

# "user" - the filter shows the user header names.
# "group" - the filter shows the group header names.

# No filter shows the user header names.

# Entitlement required: manageUserGroups (Manage users and groups) or manageAllUserGroups (Synchronize users and groups) or manageUserStandardGroups (Manage users and standard groups).
# Note: You only need one entitlement, but you can have more than one.

def get_all(ciAppliance, filter, check_mode=False, force=False):
    """
    Get the list of supported header names (USERS or GROUPS).
    """
    return ciAppliance.invoke_get("Retrieving header names",
                                "{0}?filter={1}".format("/v2.0/CSV/headerNames", filter))

