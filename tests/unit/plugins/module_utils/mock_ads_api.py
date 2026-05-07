# Copyright: (c) 2022-2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Mock Ads Api for Ads Test module on PowerScale"""

from __future__ import (absolute_import, division, print_function)
from unittest.mock import MagicMock

__metaclass__ = type

ADS_NAME = 'ads.domain.com'
DOMAIN_NAME = 'SAMPLE.LAB.EMC.COM'
PASS1 = 'pass'
USER1 = 'user'

ADS_COMMAN_ARG = {
    'onefs_host': '***.***.***.***',
    'api_user': "user",
    'api_password': "None",
    'port_no': 880,
    'verify_ssl': False,
    'domain_name': None,
    'instance_name': None,
    'ads_user': None,
    'ads_password': None,
    'state': 'present',
    'ads_parameters': {
        'groupnet': None,
        'home_directory_template': None,
        'login_shell': None,
        'machine_account': None,
        'organizational_unit': None,
        'allocate_gids': None,
        'allocate_uids': None,
        'assume_default_domain': None,
        'authentication': None,
        'check_online_interval': None,
        'create_home_directory': None,
        'domain_offline_alerts': None,
        'ignore_all_trusts': None,
        'ignored_trusted_domains': None,
        'include_trusted_domains': None,
        'ldap_sign_and_seal': None,
        'lookup_groups': None,
        'lookup_normalize_groups': None,
        'lookup_normalize_users': None,
        'lookup_users': None,
        'machine_password_changes': None,
        'nss_enumeration': None,
        'restrict_findable': None,
        'store_sfu_mappings': None,
        'machine_password_lifespan': None,
        'rpc_call_timeout': None,
        'server_retry_limit': None,
        'sfu_support': None,
        'extra_expected_spns': None,
        'findable_groups': None,
        'findable_users': None,
        'lookup_domains': None,
        'unfindable_groups': None,
        'unfindable_users': None,
    },
    'spns': None,
    'spn_command': None
}

ADS_DETAILS = {
    "ads": [
        {
            "allocate_gids": True,
            "allocate_uids": True,
            "assume_default_domain": False,
            "authentication": True,
            "check_online_interval": 300,
            "controller_time": 1726470128,
            "create_home_directory": True,
            "domain_offlin,e_alerts": False,
            "extra_expected_spns": [],
            "findable_groups": [],
            "findable_users": [],
            "forest": DOMAIN_NAME,
            "groupnet": "groupnet0",
            "home_directory_template": "/ifs/home/%D/%D",
            "hostname": "sample-isilon-x.sample.lab.emc.com",
            "id": DOMAIN_NAME,
            "ignore_all_trusts": False,
            "ignored_trusted_domains": [],
            "include_trusted_domains": [
                "SAMPLE.LAB.EMC.COM"
            ],
            "ldap_sign_and_seal": False,
            "login_shell": "/bin/zsh",
            "lookup_domains": [],
            "lookup_groups": True,
            "lookup_normalize_groups": True,
            "lookup_normalize_users": True,
            "lookup_users": True,
            "machine_account": "SAMPLE-ISILON-X$",
            "machine_password_changes": True,
            "machine_password_lifespan": 2592000,
            "name": DOMAIN_NAME,
            "netbios_domain": "SAMMPLERTP",
            "nss_enumeration": False,
            "primary_domain": DOMAIN_NAME,
            "recommended_spns": [
                "HOST/sample-isilon-x",
                "nfs/sample-isilon-x",
            ],
            "restrict_findable": False,
            "rpc_call_timeout": 400,
            "server_retry_limit": 6,
            "sfu_support": "none",
            "site": "Default-First-Site-Name",
            "spns": [
                "HOST/sample-isilon-x",
                "nfs/sample-isilon-x",
            ],
            "status": "online",
            "store_sfu_mappings": False,
            "system": False,
            "unfindable_groups": [],
            "unfindable_users": [],
            "zone_name": "System"
        }
    ]
}

CREATE_ARGS = {
    'domain_name': ADS_NAME,
    'instance_name': ADS_NAME,
    'ads_user': 'ads_user',
    'ads_password': 'ads_password',
    'state': 'present',
    'ads_parameters': {
        'groupnet': 'groupnet',
        'home_directory_template': '/home',
        'login_shell': '/bin/zsh',
        'machine_account': 'test_account',
        'organizational_unit': 'OU',
        'allocate_gids': True,
        'allocate_uids': False,
        'assume_default_domain': True,
        'authentication': True,
    }
}

MODIFY_ARGS = {
    'domain_name': ADS_NAME,
    'ads_user': 'ads_user',
    'ads_password': 'ads_password',
    'state': 'present',
    'ads_parameters': {
        'allocate_gids': True,
        'allocate_uids': False,
        'assume_default_domain': True,
        'authentication': True
    },
    'spns':
        [{'spn': 'abc', 'state': 'present'},
         {'spn': 'def', 'state': 'present'},
         {'spn': 'HOST/sample-isilon-x', 'state': 'absent'}],
    'spn_command': 'fix'
}


def get_ads_response():
    ads_response = MagicMock()
    ads_response.id = "ads_domain"
    return ads_response


def create_ads_ex_msg():
    return "Add an Active Directory provider failed with"


def get_ads_response_for_spn():
    return [{
        'id': 'ads_domain',
        'spns': [
            'abc',
            'def',
            'ghi',
        ],
        'recommended_spns': [
            'abc',
            'def',
            'ghi',
            'klm'
        ],
        'extra_expected_spns': []
    }]


def get_provider_summary():
    provider_summary = MagicMock()
    provider_summary.forest = 'ads_domain'
    provider_summary.type = 'ads'
    provider_summary.name = 'ads_domain'
    return [
        provider_summary
    ]
