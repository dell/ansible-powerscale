# Copyright: (c) 2024, Dell Technologies

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

"""Mock Api response for Unit tests of server certificate module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type


class MockServerCertificateApi:
    MODULE_UTILS_PATH = 'ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell.utils'

    SERVER_CERTIFICATE_COMMON_ARGS = {
        "onefs_host": "**.***.**.***",
        "description": "The test description",
        "state": 'present',
        "verify_ssl": False
    }

    GET_SERVER_CERTIFICATE_RESPONSE = {
        "certificates": [
            {
                "description": "This the example test description",
                "dnsnames": ["powerscale"],
                "fingerprints": [
                    {
                        "type": "SHA1",
                        "value": "68:b2:d5:5d:cc:b0:70:f1:f0:39:3a:bb:e0:44:49:70:6e:05:c3:ed",
                    },
                    {
                        "type": "SHA256",
                        "value": "69:99:b9:c0:29:49:c9:62:e8:4b:60:05:60:a8:fa:f0:01:ab:24:43:8a:47:4c:2f:66:2c:95:a1:7c:d8:10:34",
                    },
                ],
                "id": "6999b9c02949c962e84b600560a8faf001ab24438a474c2f662c95a17cd81034",
                "issuer": "C=IN, ST=Karnataka, L=Bangalore, O=Dell, OU=ISG, CN=powerscale, emailAddress=contact@dell.com",
                "name": "test",
                "not_after": 1769586969,
                "not_before": 1706514969,
                "status": "valid",
                "subject": "C=IN, ST=Karnataka, L=Bangalore, O=Dell, OU=ISG, CN=powerscale, emailAddress=contact@dell.com",
            },
            {
                "description": "This the example new_test description",
                "dnsnames": ["powerscale"],
                "fingerprints": [
                    {
                        "type": "SHA1",
                        "value": "68:b2:d5:5d:cc:b0:70:f1:f0:39:3a:bb:e0:44:49:70:6e:05:c3:ed",
                    },
                    {
                        "type": "SHA256",
                        "value": "69:99:b9:c0:29:49:c9:62:e8:4b:60:05:60:a8:fa:f0:01:ab:24:43:8a:47:4c:2f:66:2c:95:a1:7c:d8:10:34",
                    },
                ],
                "id": "6999b9c02949c962e84b600560a8faf001ab24438a474c2f662c95a17cd81035",
                "issuer": "C=IN, ST=Karnataka, L=Bangalore, O=Dell, OU=ISG, CN=powerscale, emailAddress=contact@dell.com",
                "name": "new_test",
                "not_after": 1769586969,
                "not_before": 1706514969,
                "status": "valid",
                "subject": "C=IN, ST=Karnataka, L=Bangalore, O=Dell, OU=ISG, CN=powerscale, emailAddress=contact@dell.com",
            },
        ]
    }

    GET_DEFAULT_CERTIFICATE = {
        "settings": {
            "default_https_certificate": "6999b9c02949c962e84b600560a8faf001ab24438a474c2f662c95a17cd81034"
        }
    }

    IMPORT_CERTIFICATE_GET_RESPONSE = {
        "certificates": [
            {
                "description": "This the example new_test description",
                "dnsnames": ["powerscale"],
                "fingerprints": [
                    {
                        "type": "SHA1",
                        "value": "68:b2:d5:5d:cc:b0:70:f1:f0:39:3a:bb:e0:44:49:70:6e:05:c3:ed",
                    },
                    {
                        "type": "SHA256",
                        "value": "69:99:b9:c0:29:49:c9:62:e8:4b:60:05:60:a8:fa:f0:01:ab:24:43:8a:47:4c:2f:66:2c:95:a1:7c:d8:10:34",
                    },
                ],
                "id": "6999b9c02949c962e84b600560a8faf001ab24438a474c2f662c95a17cd81036",
                "issuer": "C=IN, ST=Karnataka, L=Bangalore, O=Dell, OU=ISG, CN=powerscale, emailAddress=contact@dell.com",
                "name": "test_new_cert",
                "not_after": 1769586969,
                "not_before": 1706514969,
                "status": "valid",
                "subject": "C=IN, ST=Karnataka, L=Bangalore, O=Dell, OU=ISG, CN=powerscale, emailAddress=contact@dell.com",
            }
        ]
    }

    IMPORT_CERTIFICATE_RESPONSE = {"id": "6999b9c02949c962e84b600560a8faf001ab24438a474c2f662c95a17cd81036"}
    UPDATE_DEFAULT_CERTIFICATE = ""
    IMPORT_CERTIFICATE_RESPONSE_EMPTY = {}

    @staticmethod
    def get_default_certificate_error():
        return "The removal of the default certificate is not allowed."

    @staticmethod
    def get_module_params_error(response_type):
        if response_type == "alias_name_error" or response_type == "new_alias_name_error":
            return "The maximum length for alias_name"
        elif response_type == "description_error":
            return "The maximum length for description"
        elif response_type == "key_password_error":
            return "The maximum length for certificate_key_password"
        elif response_type == "threshold_error":
            return "The range of certificate_pre_expiration_threshold"

    @staticmethod
    def get_certificate_error(response_type):
        if response_type == "get_certificate_error_id":
            return "Failed to retrieve the server certificate"

    @staticmethod
    def get_import_certificate_error(response_type):
        if response_type == "certificate_required_error":
            return "Required both certificate_path|certificate_key_path for importing a new server certificate."
        elif response_type == "certificate_exception":
            return "Failed to create the server certificate"

    @staticmethod
    def update_server_certificate_error(response_type):
        if response_type == "update_failure_response":
            return "Failed to update the server certificate"
