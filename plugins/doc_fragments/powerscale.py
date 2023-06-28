# -*- coding: utf-8 -*-
# Copyright: (c) 2019, Dell Technologies

from __future__ import absolute_import, division, print_function
__metaclass__ = type


class ModuleDocFragment(object):
    # Documentation fragment for PowerScale (powerscale)
    DOCUMENTATION = r'''
    options:
        onefs_host:
            description:
            - IP address or FQDN of the PowerScale cluster.
            type: str
            required: true
        port_no:
            description:
            - Port number of the PowerScale cluster.It defaults to 8080 if
              not specified.
            type: str
            required: false
            default: '8080'
        verify_ssl:
            description:
            - boolean variable to specify whether to validate SSL
              certificate or not.
            - C(true) - indicates that the SSL certificate should be
              verified.
            - C(false) - indicates that the SSL certificate should not be
              verified.
            type: bool
            required: true
            choices: [true, false]
        api_user:
            type: str
            description:
            - username of the PowerScale cluster.
            required: true
        api_password:
            type: str
            description:
            - the password of the PowerScale cluster.
            required: true
    requirements:
      - A Dell PowerScale Storage system.
      - Ansible-core 2.13 or later.
      - Python 3.9, 3.10 or 3.11.
    notes:
      - The modules present in this collection named as 'dellemc.powerscale'
        are built to support the Dell PowerScale storage platform.
    '''
