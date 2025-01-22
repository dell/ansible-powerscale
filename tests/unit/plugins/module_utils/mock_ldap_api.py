# Copyright: (c) 2025, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Mock API responses for PowerScale LDAP module"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

MODULE_UTILS_PATH = 'ansible_collections.dellemc.powerscale.plugins.modules.ldap.utils'

LDAP = {'ldap': [{
        "linked_access_zones": [
            "System"
        ],
        "base_dn": "dc=sample,dc=ldap,dc=domain,dc=com",
        "bind_dn": "cn=administrator,dc=sample,dc=ldap,dc=domain,dc=com",
        "groupnet": "groupnet",
        "name": "sample-ldap",
        "server_uris": "ldap://xx.xx.xx.xx",
        "status": "online"
        }
]
}


def create_ldap_failed_msg():
    return 'Add an LDAP provider failed'


def modify_ldap_failed_msg():
    return 'Modifying LDAP provider failed'


def delete_ldap_failed_msg():
    return 'Deleting LDAP provider failed'


def invalid_server_uri_failed_msg():
    return 'The value for server_uris is invalid'


def no_server_uri_msg():
    return 'The parameter server_uris is mandatory while creating'


def invalid_server_uri_state_msg():
    return 'Please specify the server_uri_state as present-in-ldap.'


def no_base_dn_msg():
    return 'The parameter base_dn is mandatory while creating'


def ldap_access_msg():
    return 'Update LDAP with access zone details'


def ldap_exception_msg():
    return 'SDK Error message'


def ldap_exception2_msg():
    return 'failed with error'
