# -*- coding: utf-8 -*-
# Copyright: (c) 2019, Dell EMC.

from __future__ import absolute_import, division, print_function
__metaclass__ = type


class ModuleDocFragment(object):

    DOCUMENTATION = r'''
options:
  - See respective platform section for more details
requirements:
  - See respective platform section for more details
notes:
  - Ansible modules are available for Dell EMC PowerScale Storage Platform
'''
    # Documentation fragment for PowerScale (powerscale)
    POWERSCALE = r'''
    options:
        onefs_host:
            description:
            - IP address or FQDN of the PowerScale cluster.
            type: str
            required: True
        port_no:
            description:
            - Port number of the PowerScale cluster.It defaults to 8080 if
              not specified.
            type: str
            required: False
            default: '8080'
        verify_ssl:
            description:
            - boolean variable to specify whether to validate SSL
              certificate or not.
            - True - indicates that the SSL certificate should be
              verified.
            - False - indicates that the SSL certificate should not be
              verified.
            type: bool
            required: True
            choices: [True, False]
        api_user:
            type: str
            description:
            - username of the PowerScale cluster.
            required: True
        api_password:
            type: str
            description:
            - the password of the PowerScale cluster.
            required: True
    requirements:
      - A Dell EMC PowerScale Storage system.
      - Ansible 2.10, 2.11 or 2.12.
    notes:
      - The modules present in this collection named as 'dellemc.powerscale'
        are built to support the Dell EMC PowerScale storage platform.
    '''
