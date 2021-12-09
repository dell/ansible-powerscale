# Copyright: (c) 2021, DellEMC

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

"""Mock API responses for PowerScale Settings module"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type
ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'
                    }

MODULE_UTILS_PATH = 'ansible_collections.dellemc.powerscale.plugins.modules.dellemc_powerscale_settings.utils'

SETTINGS = {'email_settings': [{'mail_relay': 'mailrelay.itp.xyz.net',
                                'mail_sender': 'lab-a2@dell.com',
                                'mail_subject': 'lab-alerts'}],
            'email_settings_mod': [{'mail_relay': 'mailrelaymod.itp.xyz.net',
                                    'mail_sender': 'lab-a2_mod@dell.com',
                                    'mail_subject': 'lab_mod-alerts'}],
            'NTP_server': [{"id": "1.1.1.1",
                            "key": None,
                            "name": "1.1.1.1"}],
            'NTP_servers': [{"resume": None,
                             "servers": [{"id": "1.1.1.1",
                                          "key": None,
                                          "name": "1.1.1.1"}],
                             "total": 1}]}

GET_SETTINGS = {'settings': {'mail_relay': 'mailrelay.itp.xyz.net',
                             'mail_sender': 'lab-a2@dell.com',
                             'mail_subject': 'lab-alerts'}}


def get_ntp_server_failed_msg(ntp_server):
    return 'Failed to get NTP server ' + ntp_server


def add_blank_ntp_server_msg(ntp_server):
    return 'Failed to add NTP server'


def delete_ntp_server_failed_msg(ntp_server):
    return 'Deleting NTP server ' + ntp_server[0] + ' failed with error'


def get_email_setting_failed_msg():
    return 'Failed to get the details of email settings'


def update_email_setting_failed_msg():
    return 'Modifying email setting failed with error'
