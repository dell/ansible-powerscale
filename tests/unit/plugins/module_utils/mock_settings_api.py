# Copyright: (c) 2021, Dell Technologies

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

"""Mock API responses for PowerScale Settings module"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type


class MockSettingsApi:

    MODULE_UTILS_PATH = 'ansible_collections.dellemc.powerscale.plugins.modules.settings.utils'

    IP_ADDRESS = "**.***.**.***."

    SETTINGS_COMMON_ARGS = {
        "onefs_host": "**.***.**.***",
        "ntp_servers": "**.***.**.***",
        "mail_relay": "mailrelay.itp.xyz.net",
        "mail_sender": "lab-a2@dell.com",
        "mail_subject": "lab-alerts",
        "name": "PIE-IsilonS-24241-Cluster",
        "description": "description",
        "logon_details": {"message_title": "This is the new title",
                          "description": "This is new description"},
        "company": "Test company",
        "location": "Test location",
        "primary_contact": {"name": "primary_name",
                            "phone1": "primary_phone1",
                            "phone2": "primary_phone2",
                            "email": "primary_email@email.com"},
        "secondary_contact": {"name": "secondary_name",
                              "phone1": "secondary_phone1",
                              "phone2": "secondary_phone2",
                              "email": "secondary_email@email.com"},
        "state": "present"}

    SETTINGS = {'NTP_server': [{"id": IP_ADDRESS,
                                "key": None,
                                "name": IP_ADDRESS}],
                'NTP_servers': [{"resume": None,
                                 "servers": [{"id": IP_ADDRESS,
                                              "key": None,
                                              "name": IP_ADDRESS}],
                                 "total": 1}],
                "cluster_owner": {"company": "Test company",
                                  "location": "Test location",
                                  "primary_email": "primary_email@email.com",
                                  "primary_name": "primary_name",
                                  "primary_phone1": "primary_phone1",
                                  "primary_phone2": "primary_phone2",
                                  "secondary_email": "secondary_email@email.com",
                                  "secondary_name": "secondary_name",
                                  "secondary_phone1": "secondary_phone1",
                                  "secondary_phone2": "secondary_phone2"},
                "cluster_identity": {"description": "asdadasdasdasdadadadds",
                                     "logon": {"motd": "This is new description",
                                               "motd_header": "This is the new title"},
                                     "mttdl_level_msg": "none",
                                     "name": "PIE-IsilonS-24241-Clusterwrerwerwrewr"}}

    GET_SETTINGS = {'settings': {'mail_relay': 'mailrelay.itp.xyz.net',
                                 'mail_sender': 'lab-a2@dell.com',
                                 'mail_subject': 'lab-alerts'}}

    @staticmethod
    def get_settings_exception_response(response_type):
        if response_type == 'update_email_exception':
            return "Modifying email setting failed with error: SDK Error message"
        elif response_type == 'update_cluster_identity':
            return "Updating cluster identity failed with error SDK Error message"
        elif response_type == 'update_cluster_owner':
            return "Updating cluster owner failed with error SDK Error message"
        elif response_type == 'adding_invalid_server':
            return "Failed to add NTP server:"
        elif response_type == 'removing_invalid_server':
            return "Deleting NTP server failed with error"
        elif response_type == 'invalid_NTP_value':
            return "Please provide valid value for NTP server"
        elif response_type == 'update_invalid_cluster_name':
            return "The maximum length for name is 40"
        elif response_type == 'update_invalid_cluster_description':
            return "The maximum length for description is 255"
        elif response_type == 'update_invalid_mail_sender_email':
            return "Email address of mail_sender is not in the correct format"
