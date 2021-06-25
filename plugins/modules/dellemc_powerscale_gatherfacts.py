#!/usr/bin/python
# Copyright: (c) 2019, DellEMC

"""Ansible module for Gathering information about DellEMC PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type
ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'
                    }

DOCUMENTATION = r'''
---
module: dellemc_powerscale_gatherfacts

version_added: '1.2.0'

short_description: Gathering information about DellEMC PowerScale Storage

description:
- Gathering information about DellEMC PowerScale Storage System includes
  Get attributes of the PowerScale cluster,
  Get list of access zones in the PowerScale cluster,
  Get list of nodes in the PowerScale cluster,
  Get list of authentication providers for an access zone,
  Get list of users and groups for an access zone.
  Get list of smb_shares in the PowerScale cluster,
  Get list of nfs_exports in the PowerScale cluster,
  Get list of active clients in the PowerScale cluster.

extends_documentation_fragment:
  - dellemc.powerscale.dellemc_powerscale.powerscale

author:
- Ambuj Dubey (@AmbujDube) <ansible.team@dell.com>

options:
  access_zone:
    description:
    - The access zone. If no Access Zone is specified, the 'System' access
      zone would be taken by default.
    default: 'System'
    type: str
  gather_subset:
    description:
    - List of string variables to specify the PowerScale Storage System entities
      for which information is required.
    - List of all PowerScale Storage System entities supported by the module -
    - attributes
    - access_zones
    - nodes
    - providers
    - users
    - groups
    - smb_shares
    - nfs_exports
    - clients
    - The list of attributes, access_zones and nodes is for the entire PowerScale
      cluster
    - The list of providers, users and groups is specific to the specified
      access zone
    required: True
    choices: [attributes, access_zones, nodes, providers, users, groups,
              smb_shares, nfs_exports, clients]
    type: list
    elements: str
  '''

EXAMPLES = r'''
  - name: Get attributes of the PowerScale cluster
    dellemc_powerscale_gatherfacts:
      onefs_host: "{{onefs_host}}"
      port_no: "{{powerscaleport}}"
      verify_ssl: "{{verify_ssl}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      gather_subset:
        - attributes

  - name: Get access_zones of the PowerScale cluster
    dellemc_powerscale_gatherfacts:
      onefs_host: "{{onefs_host}}"
      port_no: "{{powerscaleport}}"
      verify_ssl: "{{verify_ssl}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      gather_subset:
        - access_zones

  - name: Get nodes of the PowerScale cluster
    dellemc_powerscale_gatherfacts:
      onefs_host: "{{onefs_host}}"
      port_no: "{{powerscaleport}}"
      verify_ssl: "{{verify_ssl}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      gather_subset:
        - nodes

  - name: Get list of authentication providers for an access zone of the
          PowerScale cluster
    dellemc_powerscale_gatherfacts:
      onefs_host: "{{onefs_host}}"
      port_no: "{{powerscaleport}}"
      verify_ssl: "{{verify_ssl}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      access_zone: "{{access_zone}}"
      gather_subset:
        - providers

  - name: Get list of users for an access zone of the PowerScale cluster
    dellemc_powerscale_gatherfacts:
      onefs_host: "{{onefs_host}}"
      port_no: "{{powerscaleport}}"
      verify_ssl: "{{verify_ssl}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      access_zone: "{{access_zone}}"
      gather_subset:
        - users

  - name: Get list of groups for an access zone of the PowerScale cluster
    dellemc_powerscale_gatherfacts:
      onefs_host: "{{onefs_host}}"
      port_no: "{{powerscaleport}}"
      verify_ssl: "{{verify_ssl}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      access_zone: "{{access_zone}}"
      gather_subset:
        - groups

  - name: Get list of smb shares in the PowerScale cluster
    dellemc_powerscale_gatherfacts:
      onefs_host: "{{onefs_host}}"
      port_no: "{{powerscaleport}}"
      verify_ssl: "{{verify_ssl}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      access_zone: "{{access_zone}}"
      gather_subset:
        - smb_shares

  - name: Get list of nfs exports in the PowerScale cluster
    dellemc_powerscale_gatherfacts:
      onefs_host: "{{onefs_host}}"
      port_no: "{{powerscaleport}}"
      verify_ssl: "{{verify_ssl}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      access_zone: "{{access_zone}}"
      gather_subset:
        - nfs_exports

  - name: Get list of clients in the PowerScale cluster
    dellemc_powerscale_gatherfacts:
      onefs_host: "{{onefs_host}}"
      port_no: "{{powerscaleport}}"
      verify_ssl: "{{verify_ssl}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      gather_subset:
        - clients
'''

RETURN = r''' '''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import dellemc_ansible_powerscale_utils as utils

LOG = utils.get_logger('dellemc_powerscale_gatherfacts')


class PowerScaleGatherFacts(object):
    """Class with Gather Fact operations"""

    def __init__(self):
        """Define all the parameters required by this module"""

        self.module_params = utils \
            .get_powerscale_management_host_parameters()
        self.module_params.update(get_powerscale_gatherfacts_parameters())

        # initialize the Ansible module
        self.module = AnsibleModule(argument_spec=self.module_params,
                                    supports_check_mode=False
                                    )

        PREREQS_VALIDATE = utils.validate_module_pre_reqs(self.module.params)
        if PREREQS_VALIDATE \
                and not PREREQS_VALIDATE["all_packages_found"]:
            self.module.fail_json(
                msg=PREREQS_VALIDATE["error_message"])

        self.api_client = utils.get_powerscale_connection(self.module.params)
        self.isi_sdk = utils.get_powerscale_sdk()
        LOG.info('Got python SDK instance for provisioning on PowerScale ')

        self.cluster_api = self.isi_sdk.ClusterApi(self.api_client)
        self.zone_api = self.isi_sdk.ZonesApi(self.api_client)
        self.auth_api = self.isi_sdk.AuthApi(self.api_client)
        self.protocol_api = self.isi_sdk.ProtocolsApi(self.api_client)
        self.statistics_api = self.isi_sdk.StatisticsApi(self.api_client)

    def get_attributes_list(self):
        """Get the list of attributes of a given PowerScale Storage"""
        try:
            config = (self.cluster_api.get_cluster_config()).to_dict()
            ips = self.cluster_api.get_cluster_external_ips()
            external_ip_str = ','.join(ips)
            external_ips = {"External IPs": external_ip_str}
            logon_msg = (self.cluster_api.get_cluster_identity()).to_dict()
            contact_info = (self.cluster_api.get_cluster_owner()).to_dict()
            cluster_version = (self.cluster_api.get_cluster_version())\
                .to_dict()
            attribute = {"Config": config, "Contact_Info": contact_info,
                         "External_IP": external_ips,
                         "Logon_msg": logon_msg,
                         "Cluster_Version": cluster_version}
            LOG.info("Got Attributes of PowerScale cluster %s",
                     self.module.params['onefs_host'])
            return attribute
        except Exception as e:
            error_msg = (
                'Get Attributes List for PowerScale cluster: {0} failed'
                ' with error: {1}' .format(
                    self.module.params['onefs_host'],
                    utils.determine_error(e)))
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def get_access_zones_list(self):
        """Get the list of access_zones of a given PowerScale Storage"""
        try:
            access_zones_list = (self.zone_api.list_zones()).to_dict()
            LOG.info("Got Access zones from PowerScale cluster %s",
                     self.module.params['onefs_host'])
            return access_zones_list
        except Exception as e:
            error_msg = (
                'Get Access zone List for PowerScale cluster: {0} failed'
                'with error: {1}' .format(
                    self.module.params['onefs_host'],
                    utils.determine_error(e)))
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def get_nodes_list(self):
        """Get the list of nodes of a given PowerScale Storage"""
        try:
            nodes_list = (self.cluster_api.get_cluster_nodes()).to_dict()
            LOG.info('Got Nodes from PowerScale cluster  %s',
                     self.module.params['onefs_host'])
            return nodes_list
        except Exception as e:
            error_msg = (
                'Get Nodes List for PowerScale cluster: {0} failed with'
                'error: {1}' .format(
                    self.module.params['onefs_host'],
                    utils.determine_error(e)))
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def get_providers_list(self, access_zone):
        """Get the list of authentication providers for an access zone of a
        given PowerScale Storage"""
        try:
            providers_list = (self.auth_api
                              .get_providers_summary(zone=access_zone))\
                .to_dict()
            LOG.info('Got authentication Providers from PowerScale cluster %s',
                     self.module.params['onefs_host'])
            return providers_list
        except Exception as e:
            error_msg = (
                'Get authentication Providers List for PowerScale'
                ' cluster: {0} and access zone: {1} failed with'
                ' error: {2}' .format(
                    self.module.params['onefs_host'],
                    access_zone,
                    utils.determine_error(e)))
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def get_users_list(self, access_zone):
        """Get the list of users for an access zone of a given PowerScale
        Storage"""
        try:
            users_list = (self.auth_api.list_auth_users(zone=access_zone))\
                .to_dict()
            LOG.info('Got Users from PowerScale cluster %s',
                     self.module.params['onefs_host'])
            return users_list
        except Exception as e:
            error_msg = (
                'Get Users List for PowerScale cluster: {0} and access zone: {1} '
                'failed with error: {2}' .format(
                    self.module.params['onefs_host'],
                    access_zone,
                    utils.determine_error(e)))
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def get_groups_list(self, access_zone):
        """Get the list of groups for an access zone of a given PowerScale
        Storage"""
        try:
            group_list = (
                self.auth_api.list_auth_groups(
                    zone=access_zone)).to_dict()
            LOG.info('Got Groups from PowerScale cluster %s',
                     self.module.params['onefs_host'])
            return group_list
        except Exception as e:
            error_msg = ('Get Group List for PowerScale cluster: {0} and'
                         'access zone: {1} failed with error: {2}'.format(
                             self.module.params['onefs_host'],
                             access_zone,
                             utils.determine_error(e)))
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def get_smb_shares_list(self, access_zone):
        """Get the list of smb_shares of a given PowerScale Storage"""
        try:
            smb_shares_list = []
            smb_shares_details = (self.protocol_api.list_smb_shares(zone=access_zone)).to_dict()
            smb_shares = smb_shares_details['shares']
            LOG.info('Got smb_shares from PowerScale cluster  %s',
                     self.module.params['onefs_host'])
            if smb_shares:
                for share in smb_shares:
                    smb_shares_list.append({"id": share['id'],
                                            "name": share['name']})
            return smb_shares_list
        except Exception as e:
            error_msg = (
                'Get smb_shares list for PowerScale cluster: {0} failed with'
                'error: {1}'.format(
                    self.module.params['onefs_host'],
                    utils.determine_error(e)))
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def get_clients_list(self):
        """Get the list of active clients of a given PowerScale Storage"""
        try:
            clients_list = []
            clients_details = (self.statistics_api.get_summary_client()).to_dict()
            LOG.info('Got active clients from PowerScale cluster  %s',
                     self.module.params['onefs_host'])
            clients = clients_details['client']
            if clients:
                for client in clients:
                    clients_list.append({"local_address": client['local_addr'],
                                         "local_name": client['local_name'],
                                         "remote_address": client['remote_addr'],
                                         "remote_name": client['remote_name'],
                                         "node": client['node'],
                                         "protocol": client['protocol']})
            return clients_list
        except Exception as e:
            error_msg = (
                'Get active clients list for PowerScale cluster: {0} failed with'
                'error: {1}'.format(
                    self.module.params['onefs_host'],
                    utils.determine_error(e)))
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def get_nfs_exports_list(self, access_zone):
        """Get the list of nfs_exports of a given PowerScale Storage"""
        try:
            nfs_exports_list = []
            nfs_exports_details = (self.protocol_api.list_nfs_exports(zone=access_zone))\
                .to_dict()
            nfs_exports = nfs_exports_details["exports"]
            if nfs_exports:
                for nfs_export in nfs_exports:
                    nfs_exports_list.append({"id": nfs_export['id'], "paths": nfs_export['paths']})
            LOG.info('Got nfs_exports from PowerScale cluster  %s',
                     self.module.params['onefs_host'])
            return nfs_exports_list
        except Exception as e:
            error_msg = (
                'Get nfs_exports list for PowerScale cluster: {0} failed with'
                'error: {1}'.format(
                    self.module.params['onefs_host'],
                    utils.determine_error(e)))
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def perform_module_operation(self):
        """Perform different actions on Gatherfacts based on user parameter
        chosen in playbook
        """
        access_zone = self.module.params['access_zone']
        subset = self.module.params['gather_subset']
        if not subset:
            self.module.fail_json(msg="Please specify gather_subset")

        attributes = []
        access_zones = []
        nodes = []
        providers = []
        users = []
        groups = []
        smb_shares = []
        clients = []
        nfs_exports = []
        if 'attributes' in str(subset):
            attributes = self.get_attributes_list()
        if 'access_zones' in str(subset):
            access_zones = self.get_access_zones_list()
        if 'nodes' in str(subset):
            nodes = self.get_nodes_list()
        if 'providers' in str(subset):
            providers = self.get_providers_list(access_zone)
        if 'users' in str(subset):
            users = self.get_users_list(access_zone)
        if 'groups' in str(subset):
            groups = self.get_groups_list(access_zone)
        if 'smb_shares' in str(subset):
            smb_shares = self.get_smb_shares_list(access_zone)
        if 'clients' in str(subset):
            clients = self.get_clients_list()
        if 'nfs_exports' in str(subset):
            nfs_exports = self.get_nfs_exports_list(access_zone)
        self.module.exit_json(
            Attributes=attributes,
            AccessZones=access_zones,
            Nodes=nodes,
            Providers=providers,
            Users=users,
            Groups=groups,
            SmbShares=smb_shares,
            Clients=clients,
            NfsExports=nfs_exports)


def get_powerscale_gatherfacts_parameters():
    """This method provide parameter required for the ansible gatherfacts
        modules on PowerScale"""
    return dict(
        access_zone=dict(required=False, type='str',
                         default='System'),
        gather_subset=dict(type='list', required=True, elements='str',
                           choices=['attributes',
                                    'access_zones',
                                    'nodes',
                                    'providers',
                                    'users',
                                    'groups',
                                    'smb_shares',
                                    'nfs_exports',
                                    'clients'
                                    ]),
    )


def main():
    """Create PowerScale GatherFacts object and perform action on it
        based on user input from playbook"""
    obj = PowerScaleGatherFacts()
    obj.perform_module_operation()


if __name__ == '__main__':
    main()
