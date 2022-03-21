#!/usr/bin/python
# Copyright: (c) 2019, DellEMC

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

"""Ansible module for Gathering information about DellEMC PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: info

version_added: '1.2.0'

short_description: Gathering information about DellEMC PowerScale Storage

description:
- Gathering information about DellEMC PowerScale Storage System includes
  Get attributes of the PowerScale cluster,
  Get list of access zones in the PowerScale cluster,
  Get list of nodes in the PowerScale cluster,
  Get list of authentication providers for all access zones or a specific access zone,
  Get list of users and groups for an access zone.
  Get list of smb_shares in the PowerScale cluster,
  Get list of nfs_exports in the PowerScale cluster,
  Get list of active clients in the PowerScale cluster,
  Get list of SyncIQ reports in the PowerScale cluster,
  Get list of SyncIQ target reports in the PowerScale cluster,
  Get list of SyncIQ target cluster certificates in the PowerScale cluster,
  Get list of SyncIQ policies in the PowerScale cluster.
  Get list of SyncIQ performance rules in the PowerScale cluster.
  Get list of network groupnets of the PowerScale cluster.
  Get list of network pools for all access zones or a specific access zone of the PowerScale cluster.
  Get list of network rules of the PowerScale cluster.
  Get list of network subnets of the PowerScale cluster.
  Get list of network interfaces of the PowerScale cluster.

extends_documentation_fragment:
  - dellemc.powerscale.dellemc_powerscale.powerscale

author:
- Ambuj Dubey (@AmbujDube) <ansible.team@dell.com>
- Spandita Panigrahi(@panigs7) <ansible.team@dell.com>

options:
  include_all_access_zones:
    description:
    - Specifies if requested component details need to be fetched from all access zones.
    - It is mutually exclusive with access_zone.
    type: bool
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
    - synciq_reports
    - synciq_target_reports
    - synciq_policies
    - synciq_target_cluster_certificates
    - synciq_performance_rules
    - network_groupnets
    - network_pools
    - network_rules
    - network_interfaces
    - network_subnets
    - The list of attributes, access_zones and nodes is for the entire PowerScale
      cluster
    - The list of providers, users and groups is specific to the specified
      access zone
    - The list of syncIQ reports and syncIQ target reports for the entire PowerScale
      cluster
    - The list of syncIQ policies, syncIQ target cluster certificates and syncIQ performance rules
      for the entire PowerScale cluster
    - The list of network pools is specific to the specified access zone or for all access zones
    - The list of network groupnets, network subnets, network rules and network interfaces is for the entire PowerScale cluster
    required: True
    choices: [attributes, access_zones, nodes, providers, users, groups,
              smb_shares, nfs_exports, clients, synciq_reports, synciq_target_reports,
              synciq_policies, synciq_target_cluster_certificates, synciq_performance_rules,
              network_groupnets, network_subnets, network_pools, network_rules, network_interfaces]
    type: list
    elements: str
notes:
- The parameters access_zone and include_all_access_zones are mutually exclusive.
- Listing of SyncIQ target cluster certificates is not supported by isi_sdk_8_1_1 version.
'''

EXAMPLES = r'''
  - name: Get attributes of the PowerScale cluster
    dellemc.powerscale.info:
      onefs_host: "{{onefs_host}}"
      port_no: "{{powerscaleport}}"
      verify_ssl: "{{verify_ssl}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      gather_subset:
        - attributes

  - name: Get access_zones of the PowerScale cluster
    dellemc.powerscale.info:
      onefs_host: "{{onefs_host}}"
      port_no: "{{powerscaleport}}"
      verify_ssl: "{{verify_ssl}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      gather_subset:
        - access_zones

  - name: Get nodes of the PowerScale cluster
    dellemc.powerscale.info:
      onefs_host: "{{onefs_host}}"
      port_no: "{{powerscaleport}}"
      verify_ssl: "{{verify_ssl}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      gather_subset:
        - nodes

  - name: Get list of authentication providers for an access zone of the
          PowerScale cluster
    dellemc.powerscale.info:
      onefs_host: "{{onefs_host}}"
      port_no: "{{powerscaleport}}"
      verify_ssl: "{{verify_ssl}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      access_zone: "{{access_zone}}"
      gather_subset:
        - providers

  - name: Get list of authentication providers for all access zones of the
          PowerScale cluster
    dellemc.powerscale.info:
      onefs_host: "{{onefs_host}}"
      port_no: "{{powerscaleport}}"
      verify_ssl: "{{verify_ssl}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      include_all_access_zones: True
      gather_subset:
        - providers

  - name: Get list of users for an access zone of the PowerScale cluster
    dellemc.powerscale.info:
      onefs_host: "{{onefs_host}}"
      port_no: "{{powerscaleport}}"
      verify_ssl: "{{verify_ssl}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      access_zone: "{{access_zone}}"
      gather_subset:
        - users

  - name: Get list of groups for an access zone of the PowerScale cluster
    dellemc.powerscale.info:
      onefs_host: "{{onefs_host}}"
      port_no: "{{powerscaleport}}"
      verify_ssl: "{{verify_ssl}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      access_zone: "{{access_zone}}"
      gather_subset:
        - groups

  - name: Get list of smb shares in the PowerScale cluster
    dellemc.powerscale.info:
      onefs_host: "{{onefs_host}}"
      port_no: "{{powerscaleport}}"
      verify_ssl: "{{verify_ssl}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      access_zone: "{{access_zone}}"
      gather_subset:
        - smb_shares

  - name: Get list of nfs exports in the PowerScale cluster
    dellemc.powerscale.info:
      onefs_host: "{{onefs_host}}"
      port_no: "{{powerscaleport}}"
      verify_ssl: "{{verify_ssl}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      access_zone: "{{access_zone}}"
      gather_subset:
        - nfs_exports

  - name: Get list of clients in the PowerScale cluster
    dellemc.powerscale.info:
      onefs_host: "{{onefs_host}}"
      port_no: "{{powerscaleport}}"
      verify_ssl: "{{verify_ssl}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      gather_subset:
        - clients

  - name: Get list of SyncIQ reports and SyncIQ target Reports in the PowerScale cluster
    dellemc.powerscale.info:
      onefs_host: "{{onefs_host}}"
      port_no: "{{powerscaleport}}"
      verify_ssl: "{{verify_ssl}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      gather_subset:
        - synciq_reports
        - synciq_target_reports

  - name: Get list of SyncIQ policies in the PowerScale cluster
    dellemc.powerscale.info:
      onefs_host: "{{onefs_host}}"
      port_no: "{{powerscaleport}}"
      verify_ssl: "{{verify_ssl}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      gather_subset:
        - synciq_policies

  - name: Get list of SyncIQ target cluster certificates in the PowerScale cluster
    dellemc.powerscale.info:
      onefs_host: "{{onefs_host}}"
      port_no: "{{powerscaleport}}"
      verify_ssl: "{{verify_ssl}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      gather_subset:
        - synciq_target_cluster_certificates

  - name: Get list of SyncIQ performance rules in the PowerScale cluster
    dellemc.powerscale.info:
      onefs_host: "{{onefs_host}}"
      port_no: "{{powerscaleport}}"
      verify_ssl: "{{verify_ssl}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      gather_subset:
        - synciq_performance_rules

  - name: Get list of network groupnets of the PowerScale cluster
    dellemc.powerscale.info:
      onefs_host: "{{onefs_host}}"
      verify_ssl: "{{verify_ssl}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      gather_subset:
        - network_groupnets

  - name: Get list of network pools of the PowerScale cluster
    dellemc.powerscale.info:
      onefs_host: "{{onefs_host}}"
      verify_ssl: "{{verify_ssl}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      gather_subset:
        - network_pools

  - name: Get list of network pools for all access zones of the PowerScale cluster
    dellemc.powerscale.info:
      onefs_host: "{{onefs_host}}"
      verify_ssl: "{{verify_ssl}}"
      api_user: "{{api_user}}"
      include_all_access_zones: True
      gather_subset:
        - network_pools

  - name: Get list of network rules of the PowerScale cluster
    dellemc.powerscale.info:
      onefs_host: "{{onefs_host}}"
      verify_ssl: "{{verify_ssl}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      gather_subset:
        - network_rules

  - name: Get list of network interfaces of the PowerScale cluster
    dellemc.powerscale.info:
      onefs_host: "{{onefs_host}}"
      verify_ssl: "{{verify_ssl}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      gather_subset:
        - network_interfaces

  - name: Get list of network subnets of the PowerScale cluster
    dellemc.powerscale.info:
      onefs_host: "{{onefs_host}}"
      verify_ssl: "{{verify_ssl}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      gather_subset:
        - network_subnets
'''

RETURN = r''' '''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import dellemc_ansible_powerscale_utils as utils

LOG = utils.get_logger('info')


class Info(object):
    """Class with Gathering information operations"""

    def __init__(self):
        """Define all the parameters required by this module"""

        self.module_params = utils \
            .get_powerscale_management_host_parameters()
        self.module_params.update(get_info_parameters())
        mutually_exclusive_args = [['access_zone', 'include_all_access_zones']]

        # initialize the Ansible module
        self.module = AnsibleModule(argument_spec=self.module_params,
                                    supports_check_mode=False,
                                    mutually_exclusive=mutually_exclusive_args
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
        self.synciq_api = self.isi_sdk.SyncApi(self.api_client)
        self.network_api = self.isi_sdk.NetworkApi(self.api_client)

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

    def get_providers_list(self, access_zone, include_all_access_zones):
        """Get the list of authentication providers for an access zone of a
        given PowerScale Storage"""
        try:
            if include_all_access_zones:
                providers_list = (self.auth_api
                                  .get_providers_summary())\
                    .to_dict()
            else:
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

    def get_synciq_reports(self):
        """Get the list of SyncIQ Reports of a given PowerScale Storage"""
        try:
            synciq_reports_list = []
            synciq_reports_details = (self.synciq_api.get_sync_reports()).to_dict()
            for i in range(synciq_reports_details['total']):
                synciq_reports_dict = {"id": synciq_reports_details['reports'][i]['id'],
                                       "name": synciq_reports_details['reports'][i]['policy_name']}
                synciq_reports_list.append(synciq_reports_dict)
            return synciq_reports_list
        except Exception as e:
            error_msg = (
                'Get SyncIQ Report list for PowerScale cluster: {0} failed with'
                'error: {1}'.format(
                    self.module.params['onefs_host'],
                    utils.determine_error(e)))
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def get_syniq_policies_list(self):
        """Get the list of SyncIQ policies of a given PowerScale Storage"""
        try:
            policies_list = []
            policies_details = (self.synciq_api.list_sync_policies()).to_dict()
            policies = policies_details['policies']
            if policies:
                for policy in policies:
                    policies_list.append({"name": policy['name'],
                                          "id": policy['id'],
                                          "source_root_path": policy['source_root_path'],
                                          "target_path": policy['target_path'],
                                          "action": policy['action'],
                                          "schedule": policy['schedule'],
                                          "enabled": policy['enabled']})
            return policies_list
        except Exception as e:
            error_msg = (
                'Get list of SyncIQ Policies for PowerScale: %s failed with'
                'error: %s' % (self.module.params['onefs_host'],
                               utils.determine_error(e)))
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def get_synciq_target_reports(self):
        """Get the list of SyncIQ Target Reports of a given PowerScale Storage"""
        try:
            synciq_target_reports_list = []
            synciq_target_reports_details = (self.synciq_api.get_target_reports()).to_dict()
            for i in range(synciq_target_reports_details['total']):
                synciq_target_reports_dict = {"id": synciq_target_reports_details['reports'][i]['id'],
                                              "name": synciq_target_reports_details['reports'][i]['policy_name']}
                synciq_target_reports_list.append(synciq_target_reports_dict)
            return synciq_target_reports_list
        except Exception as e:
            error_msg = ('Get SyncIQ Target Report list for PowerScale cluster: {0} failed with'
                         'error: {1}'.format(self.module.params['onefs_host'], utils.determine_error(e)))
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def get_synciq_target_cluster_certificates_list(self):
        """Get the list of SyncIQ target cluster certificates of a given PowerScale Storage"""
        try:
            cert_list = []
            cert_details = (self.synciq_api.list_certificates_peer()).to_dict()
            certs = cert_details['certificates']
            if certs:
                for certificate in certs:
                    cert_list.append({"name": certificate['name'],
                                      "id": certificate['id']})
            return cert_list
        except Exception as e:
            error_msg = (
                'Get list of SyncIQ target cluster certificates for PowerScale: %s failed with'
                'error: %s' % (
                    self.module.params['onefs_host'],
                    utils.determine_error(e)))
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def get_synciq_performance_rules(self):
        """Get the list of SyncIQ performance rules of a given PowerScale Storage"""
        try:
            synciq_performance_rule_list = []
            synciq_performance_rule_details = (self.synciq_api.list_sync_rules()).to_dict()
            for rule in synciq_performance_rule_details['rules']:
                synciq_performance_rule_dict = {"id": rule['id'],
                                                "schedule": rule['schedule'],
                                                "enabled": rule['enabled'],
                                                "type": rule['type'],
                                                "limit": get_sync_rule_limit_unit(rule['limit'], rule['type'])}
                synciq_performance_rule_list.append(synciq_performance_rule_dict)
            return synciq_performance_rule_list
        except Exception as e:
            error_msg = ('Get SyncIQ performance rules list for PowerScale cluster: %s failed with'
                         'error: %s' % (self.module.params['onefs_host'], utils.determine_error(e)))
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def get_network_groupnets(self):
        """Get the list of network groupnets of a given PowerScale Storage"""
        try:
            network_groupnet_list = []
            network_groupnet_details = (self.network_api.list_network_groupnets()).to_dict()
            groupnets = network_groupnet_details['groupnets']
            if groupnets:
                for groupnet in groupnets:
                    network_groupnet_list.append({
                        "id": groupnet["id"],
                        "name": groupnet["name"]
                    })
            return network_groupnet_list
        except Exception as e:
            error_msg = (
                'Getting list of network groupnets for PowerScale: %s failed with '
                'error: %s' % (
                    self.module.params['onefs_host'],
                    utils.determine_error(e)))
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def get_network_pools(self, access_zone, include_all_access_zones):
        """Get the list of network pools of a given PowerScale Storage"""
        try:
            network_pool_list = []
            if include_all_access_zones:
                network_pool_details = (self.network_api.get_network_pools()).to_dict()
            else:
                network_pool_details = (self.network_api.get_network_pools(access_zone=access_zone)).to_dict()
            pools = network_pool_details['pools']
            if pools:
                for pool in pools:
                    network_pool_list.append({
                        "id": pool["id"],
                        "name": pool["name"]
                    })
            return network_pool_list
        except Exception as e:
            error_msg = (
                'Getting list of network pools for PowerScale: %s failed with '
                'error: %s' % (
                    self.module.params['onefs_host'],
                    utils.determine_error(e)))
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def get_network_rules(self):
        """Get the list of network rules of a given PowerScale Storage"""
        try:
            network_rule_list = []
            network_rule_details = (self.network_api.get_network_rules()).to_dict()
            rules = network_rule_details['rules']
            if rules:
                for rule in rules:
                    network_rule_list.append({
                        "id": rule["id"],
                        "name": rule["name"]
                    })
            return network_rule_list
        except Exception as e:
            error_msg = (
                'Getting list of network rules for PowerScale: %s failed with '
                'error: %s' % (
                    self.module.params['onefs_host'],
                    utils.determine_error(e)))
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def get_network_interfaces(self):
        """Get the list of network interfaces of a given PowerScale Storage"""
        try:
            network_interfaces_list = []
            network_interfaces_details = (self.network_api.get_network_interfaces()).to_dict()
            interfaces = network_interfaces_details['interfaces']
            if interfaces:
                for interface in interfaces:
                    network_interfaces_list.append({
                        "id": interface["id"],
                        "name": interface["name"],
                        "lnn": interface["lnn"]
                    })
            return network_interfaces_list
        except Exception as e:
            error_msg = (
                'Getting list of network interfaces for PowerScale: %s failed with '
                'error: %s' % (
                    self.module.params['onefs_host'],
                    utils.determine_error(e)))
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def get_network_subnets(self):
        """Getting list of network subnets of a given PowerScale Storage"""
        try:
            network_subnet_list = []
            network_subnets_details = (self.network_api.get_network_subnets()).to_dict()
            subnets = network_subnets_details['subnets']
            if subnets:
                for subnet in subnets:
                    network_subnet_list.append({
                        "id": subnet["id"],
                        "name": subnet["name"]
                    })
            return network_subnet_list
        except Exception as e:
            error_msg = (
                'Getting list of network subnets for PowerScale: %s failed with '
                'error: %s' % (
                    self.module.params['onefs_host'],
                    utils.determine_error(e)))
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def perform_module_operation(self):
        """Perform different actions on Gatherfacts based on user parameter
        chosen in playbook
        """
        include_all_access_zones = self.module.params['include_all_access_zones']
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
        synciq_reports = []
        synciq_target_reports = []
        synciq_policies = []
        synciq_target_cluster_certificates = []
        synciq_performance_rules = []
        network_pools = []
        network_groupnets = []
        network_rules = []
        network_interfaces = []
        network_subnets = []

        if 'attributes' in str(subset):
            attributes = self.get_attributes_list()
        if 'access_zones' in str(subset):
            access_zones = self.get_access_zones_list()
        if 'nodes' in str(subset):
            nodes = self.get_nodes_list()
        if 'providers' in str(subset):
            providers = self.get_providers_list(access_zone, include_all_access_zones)
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
        if 'synciq_reports' in str(subset):
            synciq_reports = self.get_synciq_reports()
        if 'synciq_target_reports' in str(subset):
            synciq_target_reports = self.get_synciq_target_reports()
        if 'synciq_policies' in str(subset):
            synciq_policies = self.get_syniq_policies_list()
        if 'synciq_target_cluster_certificates' in str(subset) and utils.ISI_SDK_VERSION_9:
            synciq_target_cluster_certificates = self.get_synciq_target_cluster_certificates_list()
        elif 'synciq_target_cluster_certificates' in str(subset) and not utils.ISI_SDK_VERSION_9:
            self.module.fail_json("Listing of SyncIQ target cluster certificates is not supported by "
                                  "isi_sdk_8_1_1 version.")
        if 'synciq_performance_rules' in str(subset):
            synciq_performance_rules = self.get_synciq_performance_rules()
        if 'network_groupnets' in str(subset):
            network_groupnets = self.get_network_groupnets()
        if 'network_pools' in str(subset):
            network_pools = self.get_network_pools(access_zone, include_all_access_zones)
        if 'network_rules' in str(subset):
            network_rules = self.get_network_rules()
        if 'network_interfaces' in str(subset):
            network_interfaces = self.get_network_interfaces()
        if 'network_subnets' in str(subset):
            network_subnets = self.get_network_subnets()

        result = dict(
            Attributes=attributes,
            AccessZones=access_zones,
            Nodes=nodes,
            Providers=providers,
            Users=users,
            Groups=groups,
            SmbShares=smb_shares,
            Clients=clients,
            NfsExports=nfs_exports,
            SynciqReports=synciq_reports,
            SynciqTargetReports=synciq_target_reports,
            SynciqPolicies=synciq_policies,
            SynciqPerformanceRules=synciq_performance_rules,
            NetworkGroupnets=network_groupnets,
            NetworkPools=network_pools,
            NetworkRules=network_rules,
            NetworkInterfaces=network_interfaces,
            NetworkSubnets=network_subnets
        )

        if utils.ISI_SDK_VERSION_9:
            result.update(SynciqTargetClusterCertificate=synciq_target_cluster_certificates)

        self.module.exit_json(**result)


def get_sync_rule_limit_unit(limit, type):
    """Get performance rule limit with unit"""
    if type == 'bandwidth':
        unit = 'kb/s'
    elif type == 'cpu':
        unit = '%'
    elif type == 'file_count':
        unit = 'files/sec'
    elif type == 'worker':
        unit = '%'

    return str(limit) + unit


def get_info_parameters():
    """This method provide parameter required for the ansible gatherfacts
        modules on PowerScale"""
    return dict(
        include_all_access_zones=dict(required=False, type='bool'),
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
                                    'clients',
                                    'synciq_reports',
                                    'synciq_target_reports',
                                    'synciq_policies',
                                    'synciq_target_cluster_certificates',
                                    'synciq_performance_rules',
                                    'network_groupnets',
                                    'network_pools',
                                    'network_rules',
                                    'network_interfaces',
                                    'network_subnets'
                                    ]),
    )


def main():
    """Create PowerScale GatherFacts object and perform action on it
       based on user input from playbook"""
    obj = Info()
    obj.perform_module_operation()


if __name__ == '__main__':
    main()
