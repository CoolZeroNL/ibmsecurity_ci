#!/usr/bin/python

import logging
import logging.config
import sys
import importlib
from ansible.module_utils.basic import AnsibleModule
from io import StringIO
import datetime

from ibmsecurity.appliance.awxappliance import AWXAppliance
from ibmsecurity.appliance.ibmappliance import IBMError

logger = logging.getLogger(sys.argv[0])
try:
    basestring
except NameError:
    basestring = (str, bytes)


def main():
    module = AnsibleModule(
        argument_spec=dict(
            log=dict(required=False, default='INFO', choices=['DEBUG', 'INFO', 'ERROR', 'CRITICAL']),
            appliance=dict(required=True),
            lmi_port=dict(required=False, default=443, type='int'),
            action=dict(required=True),
            force=dict(required=False, default=False, type='bool'),
            awxapi=dict(required=False, type='dict'),
            header=dict(required=False),
            awx_user=dict(required=False),
            awx_password=dict(required=False)
        ),
        supports_check_mode=True
    )

    module.debug('Started Cloud Identity module')

    # Process all Arguments
    logLevel = module.params['log']
    force = module.params['force']
    action = module.params['action']
    appliance = module.params['appliance']
    lmi_port = module.params['lmi_port']
    header = module.params['header']
    awx_user = module.params['awx_user']
    awx_password = module.params['awx_password']

    # Setup logging for format, set log level and redirect to string
    strlog = StringIO()
    DEFAULT_LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '[%(asctime)s] [PID:%(process)d TID:%(thread)d] [%(levelname)s] [%(name)s] [%(funcName)s():%(lineno)s] %(message)s'
            },
        },
        'handlers': {
            'default': {
                'level': logLevel,
                'formatter': 'standard',
                'class': 'logging.StreamHandler',
                'stream': strlog
            },
        },
        'loggers': {
            '': {
                'handlers': ['default'],
                'level': logLevel,
                'propagate': True
            },
            'requests.packages.urllib3.connectionpool': {
                'handlers': ['default'],
                'level': 'ERROR',
                'propagate': True
            }
        }
    }
    logging.config.dictConfig(DEFAULT_LOGGING)

    # define awx_server
    awx_server = AWXAppliance(hostname=appliance, header=header, lmi_port=lmi_port, awx_user=awx_user, awx_password=awx_password)
    
    # Create options string to pass to action method
    options = 'awxAppliance=awx_server, force=' + str(force)
    
    if module.check_mode is True:
        options = options + ', check_mode=True'
    if isinstance(module.params['awxapi'], dict):
        for key, value in module.params['awxapi'].items():
            if isinstance(value, basestring):
                options = options + ', ' + key + '="' + value + '"'
            else:
                options = options + ', ' + key + '=' + str(value)
    module.debug('Option to be passed to action: ' + options)

    # Dynamically process the action to be invoked
    # Simple check to restrict calls to just "AWX" ones for safety
    if action.startswith('ibmsecurity.awx.'):    
        try:
            
            module_name, method_name = action.rsplit('.', 1)
            module.debug('Action method to be imported from module: ' + module_name)
            module.debug('Action method name is: ' + method_name)          
            mod = importlib.import_module(module_name)
            
            func_ptr = getattr(mod, method_name)  # Convert action to actual function pointer
            func_call = 'func_ptr(' + options + ')'

            startd = datetime.datetime.now()

            # Execute requested 'action'
            ret_obj = eval(func_call)

            endd = datetime.datetime.now()
            delta = endd - startd

            ret_obj['stdout'] = strlog.getvalue()
            ret_obj['stdout_lines'] = strlog.getvalue().split()
            ret_obj['start'] = str(startd)
            ret_obj['end'] = str(endd)
            ret_obj['delta'] = str(delta)
            ret_obj['cmd'] = action + "(" + options + ")"
            ret_obj['ansible_facts'] = awx_server.facts

            module.exit_json(**ret_obj)

        except ImportError:
            module.fail_json(name=action, msg='Error> action belongs to a module that is not found!',
                             log=strlog.getvalue())
        except AttributeError:
            module.fail_json(name=action, msg='Error> invalid action was specified, method not found in module!',
                             log=strlog.getvalue())
        except TypeError:
            module.fail_json(name=action,
                             msg='Error> action does not have the right set of arguments or there is a code bug! Options: ' + options,
                             log=strlog.getvalue())
        except IBMError as e:
            module.fail_json(name=action, msg=str(e), log=strlog.getvalue())
    else:
        module.fail_json(name=action, msg='Error> invalid action specified!',
                         log=strlog.getvalue())


if __name__ == '__main__':
    main()
