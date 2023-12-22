# Copyright: (c) 2023, Dell Technologies

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import utils

LOG = utils.get_logger('protocol')


class Protocol:

    '''Class with shared protocol operations'''

    def __init__(self, protocol_api, module):
        """
        Initialize the protocol class
        :param protocol_api: The protocol sdk instance
        :param module: Ansible module object
        """
        self.protocol_api = protocol_api
        self.module = module

    def get_nfs_default_settings(self, access_zone):
        """
        Get details of an NFS default settings for a given access zone.
        :param access_zone: Access zone
        :type access_zone: str
        :return: NFS default settings
        :rtype: dict
        """
        msg = f"Getting NFS default settings for {access_zone} access zone"
        LOG.info(msg)
        try:
            nfs_settings_export = self.protocol_api.get_nfs_settings_export(zone=access_zone).to_dict()
            if nfs_settings_export:
                nfs_default_settings = nfs_settings_export['settings']
                msg = f"NFS default settings are: {nfs_default_settings}"
                LOG.info(msg)
                return nfs_default_settings
        except Exception as e:
            error_msg = utils.determine_error(error_obj=e)
            error_message = f'Fetching NFS default settings failed with error: {error_msg}'
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def get_s3_bucket_list(self):
        """
        Get the list of S3 buckets of a given PowerScale Storage
        :return: s3 bucket list
        :rtype: dict
        """
        try:
            s3_bucket_details = (self.protocol_api.list_s3_buckets()).to_dict()
            if s3_bucket_details:
                return s3_bucket_details
        except Exception as e:
            error_msg = utils.determine_error(error_obj=e)
            error_message = f'Fetching S3 bucket list failed with error: {error_msg}'
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def get_smb_global_settings(self):
        """
        Get details of SMB global settings
        """
        msg = "Getting SMB global settings details"
        LOG.info(msg)
        try:
            smb_global_obj = self.protocol_api.get_smb_settings_global().to_dict()
            if smb_global_obj:
                msg = f"SMB global settings details are: {smb_global_obj}"
                LOG.info(msg)
                return smb_global_obj['settings']

        except Exception as e:
            error_msg = f"Got error {utils.determine_error(e)} while getting" \
                        f" SMB global setings details "
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def get_ntp_server_list(self):
        """
        Get the list of NTP Servers configured a given PowerScale Storage
        :return: NTP server list
        :rtype: dict
        """
        try:
            ntp_server_list = self.protocol_api.list_ntp_servers()
            return ntp_server_list.to_dict()
        except Exception as e:
            error_message = f"Failed to get NTP server list: {utils.determine_error(e)}"
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def get_snmp_settings(self):
        """
        Get details of SNMP settings
        :return: SNMP settings
        :rtype: dict
        """
        try:
            snmp_settings = self.protocol_api.get_snmp_settings().to_dict()
            if snmp_settings:
                snmp_setting = snmp_settings['settings']
                msg = f"SNMP settings are: {snmp_setting}"
                LOG.info(msg)
                return snmp_setting
        except Exception as e:
            error_msg = utils.determine_error(error_obj=e)
            error_message = f'Fetching SNMP settings failed with ' \
                            f'error: {error_msg}'
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)
