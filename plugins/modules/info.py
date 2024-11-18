#!/usr/bin/python
# Copyright: (c) 2019-2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for Gathering information about PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: info

version_added: '1.2.0'

short_description: Gathering information about PowerScale Storage

description:
- Gathering information about Specified PowerScale Storage entities, includes
  attributes, access zones, nodes, authentication providers for all access
  zones, users and groups for an access zone.
- Get list of smb_shares, nfs_exports, nfs_aliases, active clients,
  SyncIQ reports, SyncIQ target reports, SyncIQ target cluster certificates,
  SyncIQ policies, SyncIQ performance rules.
- Get list of network groupnets, network pools for all access zones or a
  specific access zone, network rules, network subnets, network interfaces.
- Get list of node pools, storage pool tiers, smb open files, s3 buckets, ntp_servers.
- Get list of user mapping rules, ldap providers of the PowerScale cluster.
- Get NFS zone settings details of the PowerScale cluster.
- Get NFS default settings details of the PowerScale cluster.
- Get NFS global settings details of the PowerScale cluster.
- Get SyncIQ global settings details of the PowerScale cluster.
- Get SMB Global Settings details of the PowerScale cluster.
- Get cluster owner, cluster identity and email settings details of the PowerScale cluster.
- Get SNMP settings details of the PowerScale cluster.
- Retrieve a list of server certificate details.
- Get support assist settings details of the PowerScale cluster.
- Get list of alert rules, alert channels, alert categories, event groups and alert settings.

extends_documentation_fragment:
  - dellemc.powerscale.powerscale

author:
- Ambuj Dubey (@AmbujDube) <ansible.team@dell.com>
- Spandita Panigrahi(@panigs7) <ansible.team@dell.com>
- Pavan Mudunuri(@Pavan-Mudunuri) <ansible.team@dell.com>
- Ananthu S Kuttattu(@kuttattz) <ansible.team@dell.com>
- Bhavneet Sharma(@Bhavneet-Sharma) <ansible.team@dell.com>
- Trisha Datta(@trisha-dell) <ansible.team@dell.com>
- Meenakshi Dembi(@dembim) <ansible.team.dell.com>
- Sachin Apagundi(@sachin-apa) <ansible.team.dell.com>
- Kritika Bhateja(@Kritika-Bhateja-03) <ansible.team.dell.com>

options:
  access_zone:
    description:
    - The access zone. If no Access Zone is specified, the 'System' access
      zone would be taken by default.
    default: 'System'
    type: str
  filters:
    description:
    - List of filters to support filtered output for storage entities.
    - Each filter is a tuple of {filter_key, filter_operator, filter_value}.
    - Supports passing of multiple filters.
    required: False
    type: list
    elements: dict
    suboptions:
      filter_key:
        description:
        - Name identifier of the filter.
        type: str
        required: True
      filter_operator:
        description:
        - Operation to be performed on filter key.
        type: str
        choices: [equal]
        required: True
      filter_value:
        description:
        - Value of the filter key.
        type: raw
        required: True
    version_added: '3.2.0'
  gather_subset:
    description:
    - List of string variables to specify the PowerScale Storage System
      entities for which information is required.
    - List of all PowerScale Storage System entities supported by the module.
    - Attributes - C(attributes).
    - Access zones - C(access_zones).
    - Nodes - C(nodes).
    - Providers - C(providers).
    - Users - C(users).
    - Groups - C(groups).
    - Smb shares - C(smb_shares).
    - Nfs exports - C(nfs_exports).
    - Nfs aliases - C(nfs_aliases).
    - Clients - C(clients).
    - Synciq reports - C(synciq_reports).
    - Synciq target reports - C(synciq_target_reports).
    - Synciq policies - C(synciq_policies).
    - Synciq target cluster certificates - C(synciq_target_cluster_certificates).
    - Synciq performance rules - C(synciq_performance_rules).
    - Network groupnets - C(network_groupnets).
    - Network pools - C(network_pools).
    - Network rules - C(network_rules).
    - Network interfaces - C(network_interfaces).
    - Network subnets - C(network_subnets).
    - Node pools - C(node_pools).
    - Storagepool tiers - C(storagepool_tiers).
    - SMB files - C(smb_files).
    - User mapping rules - C(user_mapping_rules).
    - LDAPs - C(ldap).
    - NFS zone settings - C(nfs_zone_settings).
    - NFS default settings - C(nfs_default_settings).
    - SyncIQ global settings - C(synciq_global_settings).
    - S3 buckets - C(s3_buckets).
    - The list of I(attributes), I(access_zones) and I(nodes) is for the entire
      PowerScale cluster.
    - The list of providers for the entire PowerScale cluster.
    - The list of users and groups is specific to the specified
      access zone.
    - The list of syncIQ reports and syncIQ target reports for the entire
      PowerScale cluster.
    - The list of syncIQ policies, syncIQ target cluster certificates and
      syncIQ performance rules for the entire PowerScale cluster.
    - The list of network pools is specific to the specified access zone or for
      all access zones.
    - The list of network groupnets, network subnets, network rules and network
      interfaces is for the entire PowerScale cluster.
    - The list of smb open files for the entire PowerScale cluster.
    - The list of user mapping rules of PowerScale cluster.
    - The list of ldap providers of PowerScale cluster.
    - SMB global settings - C(smb_global_settings).
    - NTP servers C(ntp_servers).
    - Email settings C(email_settings).
    - Cluster identity C(cluster_identity).
    - Cluster owner C(cluster_owner).
    - SNMP settings - C(snmp_settings).
    - Server certificate - C(server_certificate).
    - Roles - C(roles).
    - Support assist settings- C(support_assist_settings).
    - Smartquota- C(smartquota).
    - Filesystem - C(filesystem).
    - Alert settings - C(alert_settings).
    - Alert rules - C(alert_rules).
    - Alert channels - C(alert_channels).
    - Alert categories - C(alert_categories).
    - Event groups - C(event_group).
    - Writable snapshots - C(writable_snapshots).
    required: true
    choices: [attributes, access_zones, nodes, providers, users, groups,
              smb_shares, nfs_exports, nfs_aliases, clients, synciq_reports, synciq_target_reports,
              synciq_policies, synciq_target_cluster_certificates, synciq_performance_rules,
              network_groupnets, network_subnets, network_pools, network_rules, network_interfaces,
              node_pools, storagepool_tiers, smb_files, user_mapping_rules, ldap,
              nfs_zone_settings, nfs_default_settings, nfs_global_settings, synciq_global_settings, s3_buckets,
              smb_global_settings, ntp_servers, email_settings, cluster_identity, cluster_owner, snmp_settings,
              server_certificate, roles, support_assist_settings, smartquota, filesystem, alert_settings,
              alert_rules, alert_channels, alert_categories, event_group, writable_snapshots]
    type: list
    elements: str
  include_all_access_zones:
    description:
    - Specifies if requested component details need to be fetched from all
      access zones.
    - It is mutually exclusive with I(access_zone).
    type: bool
  scope:
    description:
    - The scope of ldap. If no scope is specified, the C(effective) scope
      would be taken by default.
    - If specified as C(effective) or not specified, all fields are returned.
    - If specified as C(user), only fields with non-default values are shown.
    - If specified as C(default), the original values are returned.
    choices: ['effective', 'user', 'default']
    default: 'effective'
    type: str
  query_parameters:
    description:
    - Contains dictionary of query parameters for specific I(gather_subset).
    - Applicable to C(alert_rules), C(event_group), C(event_channels), C(filesystem)
      and C(writable_snapshots).
    - If C(writable_snapshots) is passed as I(gather_subset), if I(wspath) is given,
      all other query parameters inside I(writable_snapshots) will be ignored.
    - To view the list of supported query parameters for C(writable_snapshots).
    - Refer Query Parameters section from
      U(https://developer.dell.com/apis/4088/versions/9.5.0/9.5.0.0_ISLANDER_OAS2.json/
        paths/~1platform~114~1snapshot~1writable/get).
    type: dict
    version_added: '3.2.0'
notes:
- The parameters I(access_zone) and I(include_all_access_zones) are mutually exclusive.
- The I(check_mode) is supported.
- Filter functionality is supported only for the following 'gather_subset'- 'nfs', 'smartquota', 'filesystem'
  'writable_snapshots', 'smb_files'.
- The parameter I(smb_files) would return for all the clusters.
- When I(gather_subset) is C(smb_files), it is assumed that the credentials of all node is same as the I(hostname).
- C(support_assist_settings) is supported for One FS version 9.5.0 and above.
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

- name: Get list of authentication providers for all access zones of the PowerScale cluster
  dellemc.powerscale.info:
    onefs_host: "{{onefs_host}}"
    port_no: "{{powerscaleport}}"
    verify_ssl: "{{verify_ssl}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
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
    query_parameters:
      users:
        - filter: 'sample_user'

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

- name: Get list of nfs exports in the PowerScale cluster using filter
  dellemc.powerscale.info:
    onefs_host: "{{onefs_host}}"
    port_no: "{{powerscaleport}}"
    verify_ssl: "{{verify_ssl}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    access_zone: "{{access_zone}}"
    gather_subset:
      - nfs_exports
    filters:
      - filter_key: "id"
        filter_operator: "equal"
        filter_value: 7075

- name: Get list of nfs exports in the PowerScale cluster using multiple filter
  dellemc.powerscale.info:
    onefs_host: "{{onefs_host}}"
    port_no: "{{powerscaleport}}"
    verify_ssl: "{{verify_ssl}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    access_zone: "{{access_zone}}"
    gather_subset:
      - nfs_exports
    filters:
      - filter_key: "id"
        filter_operator: "equal"
        filter_value: 7075
      - filter_key: description
        filter_operator: "equal"
        filter_value: test-filter export

- name: Get list of nfs aliases in the PowerScale cluster
  dellemc.powerscale.info:
    onefs_host: "{{onefs_host}}"
    port_no: "{{powerscaleport}}"
    verify_ssl: "{{verify_ssl}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    access_zone: "{{access_zone}}"
    gather_subset:
      - nfs_aliases

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
    include_all_access_zones: true
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

- name: Get list of node pools of the PowerScale cluster
  dellemc.powerscale.info:
    onefs_host: "{{onefs_host}}"
    verify_ssl: "{{verify_ssl}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    gather_subset:
      - node_pools
  register: subset_result

- name: Get list of storage pool tiers of the PowerScale cluster
  dellemc.powerscale.info:
    onefs_host: "{{onefs_host}}"
    verify_ssl: "{{verify_ssl}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    gather_subset:
      - storagepool_tiers
  register: subset_result

- name: Get list of smb open files of the PowerScale cluster
  dellemc.powerscale.info:
    onefs_host: "{{onefs_host}}"
    verify_ssl: "{{verify_ssl}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    gather_subset:
      - smb_files

- name: Get smb open files of the PowerScale
    cluster of the PowerScale cluster using filter
  dellemc.powerscale.info:
    onefs_host: "{{onefs_host}}"
    verify_ssl: "{{verify_ssl}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    gather_subset:
      - smb_files
    filters:
      - filter_key: "id"
        filter_operator: "equal"
        filter_value: "xxx"

- name: Get list of user mapping rule of the PowerScale cluster
  dellemc.powerscale.info:
    onefs_host: "{{onefs_host}}"
    verify_ssl: "{{verify_ssl}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    gather_subset:
      - user_mapping_rules

- name: Get list of ldap providers of the PowerScale cluster
  dellemc.powerscale.info:
    onefs_host: "{{onefs_host}}"
    verify_ssl: "{{verify_ssl}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    gather_subset:
      - ldap
    scope: "effective"

- name: Get the NFS zone settings of the PowerScale cluster
  dellemc.powerscale.info:
    onefs_host: "{{onefs_host}}"
    verify_ssl: "{{verify_ssl}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    gather_subset:
      - nfs_zone_settings

- name: Get the NFS default settings of the PowerScale cluster
  dellemc.powerscale.info:
    onefs_host: "{{onefs_host}}"
    verify_ssl: "{{verify_ssl}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    gather_subset:
      - nfs_default_settings

- name: Get the NFS global settings of the PowerScale cluster
  dellemc.powerscale.info:
    onefs_host: "{{onefs_host}}"
    verify_ssl: "{{verify_ssl}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    gather_subset:
      - nfs_global_settings

- name: Get SyncIQ global settings details of the PowerScale cluster
  dellemc.powerscale.info:
    onefs_host: "{{ onefs_host }}"
    verify_ssl: "{{ verify_ssl }}"
    api_user: "{{ api_user }}"
    api_password: "{{ api_password }}"
    gather_subset:
      - synciq_global_settings

- name: Get S3 bucket list for the PowerScale cluster
  dellemc.powerscale.info:
    onefs_host: "{{ onefs_host }}"
    verify_ssl: "{{ verify_ssl }}"
    api_user: "{{ api_user }}"
    api_password: "{{ api_password }}"
    gather_subset:
      - s3_buckets

- name: Get SMB global settings from PowerScale cluster
  dellemc.powerscale.info:
    onefs_host: "{{ onefs_host }}"
    verify_ssl: "{{ verify_ssl }}"
    api_user: "{{ api_user }}"
    api_password: "{{ api_password }}"
    gather_subset:
      - smb_global_settings

- name: Get the list of server certificate
  dellemc.powerscale.info:
    onefs_host: "{{ onefs_host }}"
    verify_ssl: "{{ verify_ssl }}"
    api_user: "{{ api_user }}"
    api_password: "{{ api_password }}"
    gather_subset:
      - server_certificate

- name: Get NTP servers from PowerScale cluster
  dellemc.powerscale.info:
    onefs_host: "{{ onefs_host }}"
    verify_ssl: "{{ verify_ssl }}"
    api_user: "{{ api_user }}"
    api_password: "{{ api_password }}"
    gather_subset:
      - ntp_servers

- name: Get SNMP settings from PowerScale cluster
  dellemc.powerscale.info:
    onefs_host: "{{ onefs_host }}"
    verify_ssl: "{{ verify_ssl }}"
    api_user: "{{ api_user }}"
    api_password: "{{ api_password }}"
    gather_subset:
      - snmp_settings

- name: Get email settings details from PowerScale cluster
  dellemc.powerscale.info:
    onefs_host: "{{ onefs_host }}"
    verify_ssl: "{{ verify_ssl }}"
    api_user: "{{ api_user }}"
    api_password: "{{ api_password }}"
    gather_subset:
      - email_settings

- name: Get cluster identity details from PowerScale cluster
  dellemc.powerscale.info:
    onefs_host: "{{ onefs_host }}"
    verify_ssl: "{{ verify_ssl }}"
    api_user: "{{ api_user }}"
    api_password: "{{ api_password }}"
    gather_subset:
      - cluster_identity

- name: Get cluster owner details from PowerScale cluster
  dellemc.powerscale.info:
    onefs_host: "{{ onefs_host }}"
    verify_ssl: "{{ verify_ssl }}"
    api_user: "{{ api_user }}"
    api_password: "{{ api_password }}"
    gather_subset:
      - cluster_owner

- name: Get support assist settings from PowerScale cluster
  dellemc.powerscale.info:
    onefs_host: "{{ onefs_host }}"
    verify_ssl: "{{ verify_ssl }}"
    api_user: "{{ api_user }}"
    api_password: "{{ api_password }}"
    gather_subset:
      - support_assist_settings

- name: Get alert categories and alert settings from PowerScale cluster
  dellemc.powerscale.info:
    onefs_host: "{{ onefs_host }}"
    verify_ssl: "{{ verify_ssl }}"
    api_user: "{{ api_user }}"
    api_password: "{{ api_password }}"
    gather_subset:
      - alert_categories
      - alert_settings

- name: Get list of alert rules in descending order from PowerScale cluster
  dellemc.powerscale.info:
    onefs_host: "{{ onefs_host }}"
    verify_ssl: "{{ verify_ssl }}"
    api_user: "{{ api_user }}"
    api_password: "{{ api_password }}"
    gather_subset:
      - alert_rules
    query_parameters:
      alert_rules:
        - sort_dir: "desc"
        - sort: "condition"
        - channels: "SupportAssist"

- name: Get list of event groups with alert info from PowerScale cluster
  dellemc.powerscale.info:
    onefs_host: "{{ onefs_host }}"
    verify_ssl: "{{ verify_ssl }}"
    api_user: "{{ api_user }}"
    api_password: "{{ api_password }}"
    gather_subset:
      - event_group
    query_parameters:
      event_group:
        - alert_info: true
        - category: '100000000'

- name: Get sorted list of alert channel based on name key from PowerScale cluster
  dellemc.powerscale.info:
    onefs_host: "{{ onefs_host }}"
    verify_ssl: "{{ verify_ssl }}"
    api_user: "{{ api_user }}"
    api_password: "{{ api_password }}"
    gather_subset:
      - alert_channels
    query_parameters:
      alert_channels:
        - sort: "enabled"
        - sort_dir: "asc"

- name: Get smartquota from PowerScale cluster
  dellemc.powerscale.info:
    onefs_host: "{{ onefs_host }}"
    verify_ssl: "{{ verify_ssl }}"
    api_user: "{{ api_user }}"
    api_password: "{{ api_password }}"
    gather_subset:
      - smartquota

- name: Get smartquota from PowerScale cluster using filter
  dellemc.powerscale.info:
    onefs_host: "{{ onefs_host }}"
    verify_ssl: "{{ verify_ssl }}"
    api_user: "{{ api_user }}"
    api_password: "{{ api_password }}"
    gather_subset:
      - smartquota
    filters:
      - filter_key: "id"
        filter_operator: "equal"
        filter_value: "xxx"

- name: Get filesystem from PowerScale cluster
  dellemc.powerscale.info:
    onefs_host: "{{ onefs_host }}"
    verify_ssl: "{{ verify_ssl }}"
    api_user: "{{ api_user }}"
    api_password: "{{ api_password }}"
    gather_subset:
      - filesystem
    path: "<path>"

- name: Get filesystem from PowerScale cluster with query parameters
  dellemc.powerscale.info:
    onefs_host: "{{ onefs_host }}"
    verify_ssl: "{{ verify_ssl }}"
    api_user: "{{ api_user }}"
    api_password: "{{ api_password }}"
    gather_subset:
      - filesystem
    query_parameters:
      filesystem:
        metadata: true
        quota: true
        acl: true
        snapshot: true
        path: "<path>"

- name: Get filesystem from PowerScale cluster with query parameters along with filters
  dellemc.powerscale.info:
    onefs_host: "{{ onefs_host }}"
    verify_ssl: "{{ verify_ssl }}"
    api_user: "{{ api_user }}"
    api_password: "{{ api_password }}"
    gather_subset:
      - filesystem
    query_parameters:
      filesystem:
        metadata: true
        quota: true
        acl: true
        snapshot: true
        path: "<path>"
    filters:
      - filter_key: "name"
        filter_operator: "equal"
        filter_value: "xxx"

- name: Get all writable snapshots from PowerScale cluster
  dellemc.powerscale.info:
    onefs_host: "{{ onefs_host }}"
    verify_ssl: "{{ verify_ssl }}"
    api_user: "{{ api_user }}"
    api_password: "{{ api_password }}"
    gather_subset:
      - writable_snapshots

- name: To get the specific writable snapshot
  dellemc.powerscale.info:
    onefs_host: "{{ onefs_host }}"
    verify_ssl: "{{ verify_ssl }}"
    api_user: "{{ api_user }}"
    api_password: "{{ api_password }}"
    gather_subset:
      - writable_snapshots
    query_parameters:
      writable_snapshots:
        wspath: "/ifs/test_mkdir"

- name: To filter the writable snapshot in ascending order
  dellemc.powerscale.info:
    onefs_host: "{{ onefs_host }}"
    verify_ssl: "{{ verify_ssl }}"
    api_user: "{{ api_user }}"
    api_password: "{{ api_password }}"
    gather_subset:
      - writable_snapshots
    query_parameters:
      writable_snapshots:
        dir: ASC
        limit: 1

- name: To filter the writable snapshot using sort
  dellemc.powerscale.info:
    onefs_host: "{{ onefs_host }}"
    verify_ssl: "{{ verify_ssl }}"
    api_user: "{{ api_user }}"
    api_password: "{{ api_password }}"
    gather_subset:
      - writable_snapshots
    query_parameters:
      writable_snapshots:
        sort: src_snap
        state: active
'''

RETURN = r'''
changed:
    description: Shows Whether or not the resource has changed.
    returned: always
    type: bool
    sample: "false"
AccessZones:
    description: Access zones of  the PowerScale storage system.
    type: dict
    returned: When C(access_zones) is in a given I(gather_subset)
    contains:
        zones:
            description: List of different access zone.
            type: list
    sample: [
        "zones": [
            {
                "alternate_system_provider": "lsa-file-provider:MinimumRequired",
                "auth_providers": [
                    "lsa-local-provider:sampe-az"
                ],
                "cache_entry_expiry": 14400,
                "groupnet": "groupnet0",
                "home_directory_umask": 63,
                "id": "Bhavneet-SS",
                "ifs_restricted": [],
                "name": "Bhavneet-SS",
                "negative_cache_entry_expiry": 60,
                "netbios_name": "",
                "path": "/ifs",
                "skeleton_directory": "/usr/share/skel",
                "system": false,
                "system_provider": "lsa-file-provider:System",
                "user_mapping_rules": [],
                "zone_id": 18
            }
        ]
    ]
Attributes:
    description: Different Attributes of the PowerScale storage system.
    type: dict
    returned: When C(attributes) is in a given I(gather_subset)
    contains:
        Cluster_Version:
            description: Cluster version of the PowerScale storage system.
            type: dict
        Config:
            description: Config details of the PowerScale storage system.
            type: dict
        Contact_Info:
            description: Contact details of the PowerScale storage system.
            type: dict
        External_IP:
            description: External IPs of the PowerScale storage system.
            type: dict
        Logon_msg:
            description: Log-on messages of the PowerScale storage system.
            type: dict
    sample: {
        "Cluster_Version": {
            "errors": [],
            "nodes": [
                {
                    "build": "B_9_5_0_005(RELEASE)",
                    "id": 1,
                    "release": "x.x.0.0",
                    "revision": "124",
                    "type": "Isilon OneFS",
                    "version": "Isilon OneFS x.x.0.0"
                }
            ],
            "total": 3
        },
        "Config": {
            "description": "",
            "devices": [
                {
                    "devid": 1,
                    "guid": "000e1e84be90ac5e7d62df0dfc180d3d0ccb",
                    "is_up": true,
                    "lnn": 1
                }
            ],
            "encoding": "utf-8",
            "guid": "000e1e84be902f5f7d62ef254853667f0792",
            "has_quorum": true,
            "is_compliance": false,
            "is_virtual": false,
            "is_vonefs": false,
            "join_mode": "Manual",
            "local_devid": 1,
            "local_lnn": 1,
            "local_serial": "xxxx-xxxx-xxxxx",
            "name": "LAB-IsilonS-xxxxx",
            "onefs_version": {
                "build": "B_x_x_0_005(RELEASE)",
                "copyright": "Copyright (c) 2001-2022 Dell Inc. All Rights Reserved.",
                "reldate": xxxx,
                "release": "x.x.0.0",
                "revision": "649926064822288389",
                "type": "Isilon OneFS",
                "version": "Isilon OneFS x.x.0.0"
            },
            "timezone": {
                "abbreviation": "GMT",
                "custom": "",
                "name": "Greenwich Mean Time",
                "path": "GMT"
            },
            "upgrade_type": null
        },
        "Contact_Info": {},
        "External_IP": {},
        "Logon_msg": {}
    }
Clients:
    description: List all clients present in the PowerScale system.
    type: list
    returned: When C(clients) is in a given I(gather_subset)
    contains:
        local_address:
            description: Local address of the client.
            type: str
        local_name:
            description: Local name of the client.
            type: str
        node:
            description: Node on which client exists.
            type: int
        protocol:
            description: Protocol that client uses.
            type: str
        remote_address:
            description: Remote address of the client.
            type: str
        remote_name:
            description: Remote address of the client.
            type: str
    sample: [
        {
            "local_address": "x.x.x.x",
            "local_name": "x.x.x.x",
            "node": 1,
            "protocol": "nfs4",
            "remote_address": "x.x.x.x",
            "remote_name": "x.x.x.x"
        }
    ]
Groups:
    description: List of all groups.
    type: list
    returned: When C(groups) is in a given I(gather_subset)
    contains:
        groups:
            description: List of groups details.
            type: list
            contains:
                id:
                    description: ID of the groups.
                    type: str
                name:
                    description: Name of the groups.
                    type: str
                provider:
                    description: The provider of the groups.
                    type: str
    sample: [
        "groups": [
            {
                "dn": "CN=Administrators,CN=Builtin,DC=PIE-ISILONS-xxx",
                "dns_domain": null,
                "domain": "BUILTIN",
                "generated_gid": false,
                "gid": {
                    "id": "GID:1544",
                    "name": null,
                    "type": null
                },
                "id": "Administrators",
                "member_of": null,
                "name": "Administrators",
                "object_history": [],
                "provider": "lsa-local-provider:System",
                "sam_account_name": "Administrators",
                "sid": {
                    "id": "SID:S-1-5-32-544",
                    "name": null,
                    "type": null
                },
                "type": "group"
            }
        ]
    ]
LdapProviders:
    description: Provide details of LDAP providers.
    type: list
    returned: When C(ldap) is in a given I(gather_subset)
    contains:
        linked_access_zones:
            description: List of access zones linked to the authentication
                         provider.
            type: list
        base_dn:
            description: Specifies the root of the tree in which to search
                         identities.
            type: str
        bind_dn:
            description: Specifies the distinguished name for binding to the
                         LDAP server.
            type: str
        groupnet:
            description: Groupnet identifier.
            type: str
        name:
            description: Specifies the name of the LDAP provider.
            type: str
        server_uris:
            description: Specifies the server URIs.
            type: str
        status:
            description: Specifies the status of the provider.
            type: str
    sample: [
        {
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
NetworkGroupnets:
    description: List of Network Groupnets.
    type: list
    returned: When C(network_groupnets) is in a given I(gather_subset)
    contains:
        id:
            description: ID of the groupnet.
            type: str
        name:
            description: Name of the groupnet.
            type: str
    sample: [
        {
            "id": "sample",
            "name": "groupnet0"
        }
    ]
NetworkInterfaces:
    description: List of Network interfaces.
    type: list
    returned: When C(network_interfaces) is in a given I(gather_subset)
    contains:
        flags:
            description: List of interface flags.
            type: list
        id:
            description: ID of the interface.
            type: str
        ip_addrs:
            description: List of IP addresses.
            type: list
        ipv4_gateway:
            description: Address of the default IPv4 gateway.
            type: str
        ipv6_gateway:
            description: Address of the default IPv6 gateway.
            type: str
        lnn:
            description: Interface's lnn.
            type: int
        mtu:
            description: The mtu the interface.
            type: int
        name:
            description: Name of the interface.
            type: str
        nic_name:
            description: NIC name.
            type: str
        owners:
            description: List of owners.
            type: list
        speed:
            description: Interface's speed.
            type: int
        status:
            description: Status of the interface.
            type: str
        type:
            description: Type of the interface.
            type: str
        vlans:
            description: List of VLANs.
            type: list
    sample: [
            {
                "flags": [],
                "id": "3:ext-agg",
                "ip_addrs": [],
                "ipv4_gateway": null,
                "ipv6_gateway": null,
                "lnn": 3,
                "mtu": 0,
                "name": "ext-agg",
                "nic_name": "lagg0",
                "owners": [],
                "speed": null,
                "status": "inactive",
                "type": "aggregated",
                "vlans": []
        }
    ]
NetworkPools:
    description: List of Network Pools.
    type: list
    returned: When C(network_pools) is in a given I(gather_subset)
    contains:
        id:
            description: ID of the Network Pool.
            type: str
        name:
            description: Name of the Network Pool.
            type: str
    sample: [
        {
            "id": "groupnet0.subnet0.pool0",
            "name": "pool0"
        }
    ]
NetworkRules:
    description: List of the Network rules.
    type: list
    returned: When C(network_rules) is in a given I(gather_subset)
    contains:
        id:
            description: Name of the Network Pool.
            type: str
        name:
            description: Name of the Network Pool.
            type: str
    sample: [
        {
            "id": "groupnet0.subnet0.pool0.test_rule",
            "name": "test_rule"
        }
    ]
NetworkSubnets:
    description: List of the Network subnets.
    type: list
    returned: When C(network_subnets) is in a given I(gather_subset)
    contains:
        id:
            description: Name of the Network Pool.
            type: str
        name:
            description: Name of the Network Pool.
            type: str
    sample: [
        {
            "id": "groupnet0.subnet0.pool0.test_rule",
            "name": "test_rule"
        }
    ]
NfsAliases:
    description: List of NFS Aliases.
    type: list
    returned: When C(nfs_aliases) is in a given I(gather_subset)
    contains:
        health:
            description: Specifies the health of the NFS alias.
            type: str
        id:
            description: ID of the NFS alias.
            type: str
        name:
            description: Name of the NFS alias.
            type: str
        path:
            description: Path of the NFS alias.
            type: str
        zone:
            description: Access zone of the NFS alias.
            type: str
    sample: [
        {
            "health": "path not found",
            "id": "/ifs_#$%^&*()",
            "name": "/ifs_#$%^&*()",
            "path": "/ifs/sample_alias_1",
            "zone": "System"
        }
    ]
NfsExports:
    description: List of NFS exports.
    type: list
    returned: When C(nfs_exports) is in a given I(gather_subset)
    contains:
        all_dirs:
            description: I(sub_directories_mountable) flag value.
            type: bool
        id:
            description: The ID of the NFS Export, generated by the array.
            type: int
            sample: 12
        paths:
            description: The filesystem path.
            type: list
            sample:  ['/ifs/dir/filepath']
        zone:
            description: Specifies the zone in which the export is valid.
            type: str
            sample: 'System'
        read_only:
            description: Specifies whether the export is read-only or read-write.
            type: bool
        read_only_clients:
            description: The list of read only clients for the NFS Export.
            type: list
            sample:  ['client_ip', 'client_ip']
        read_write_clients:
            description: The list of read write clients for the NFS Export.
            type: list
            sample:  ['client_ip', 'client_ip']
        root_clients:
            description: The list of root clients for the NFS Export.
            type: list
            sample:  ['client_ip', 'client_ip']
        clients:
            description: The list of clients for the NFS Export.
            type: list
            sample:  ['client_ip', 'client_ip']
        description:
            description: Description for the export.
            type: str
        map_root:
            description: Specifies the users and groups to which non-root and root clients are mapped.
            type: complex
            contains:
                enabled:
                    description: True if the user mapping is applied.
                    type: bool
                user:
                    description: Specifies the persona name.
                    type: complex
                    contains:
                        id:
                            description: Specifies the persona name.
                            type: str
                primary_group:
                    description: Specifies the primary group.
                    type: complex
                    contains:
                        id:
                            description: Specifies the primary group name.
                            type: str
                secondary_groups:
                    description: Specifies the secondary groups.
                    type: list
        map_non_root:
            description: Specifies the users and groups to which non-root and root clients are mapped.
            type: complex
            contains:
                enabled:
                    description: True if the user mapping is applied.
                    type: bool
                user:
                    description: Specifies the persona details.
                    type: complex
                    contains:
                        id:
                            description: Specifies the persona name.
                            type: str
                primary_group:
                    description: Specifies the primary group details.
                    type: complex
                    contains:
                        id:
                            description: Specifies the primary group name.
                            type: str
                secondary_groups:
                    description: Specifies the secondary groups details.
                    type: list

    sample: [
        "all_dir": "false",
        "block_size": 8192,
        "clients": None,
        "id": 9324,
        "read_only_client": ["x.x.x.x"],
        "security_flavors": ["unix", "krb5"],
        "zone": "System",
        "map_root": {
            "enabled": true,
            "primary_group": {
                "id": GROUP:group1,
                "name": null,
                "type": null
            },
            "secondary_groups": [],
            "user": {
                "id": "USER:user",
                "name": null,
                "type": null
            }
        },
        "map_non_root": {
            "enabled": false,
            "primary_group": {
                "id": null,
                "name": null,
                "type": null
            },
            "secondary_groups": [],
            "user": {
                "id": "USER:nobody",
                "name": null,
                "type": null
            }
        }
    ]
NfsZoneSettings:
    description: Details of NFS zone settings.
    type: dict
    returned: When C(nfs_zone_settings) is in a given I(gather_subset)
    contains:
        nfsv4_allow_numeric_ids:
            description: If C(true), sends owners and groups as UIDs and GIDs
                         when look up fails or if the I(nfsv4_no_names)
                         property is set to 1.
            type: bool
        nfsv4_domain:
            description: Specifies the domain through which users and groups
                         are associated.
            type: str
        nfsv4_no_domain:
            description: If C(true), sends owners and groups without a domain
                         name.
            type: bool
        nfsv4_no_domain_uids:
            description: If C(true), sends UIDs and GIDs without a domain name.
            type: bool
        nfsv4_no_names:
            description: If C(true), sends owners and groups as UIDs and GIDs.
            type: bool
        nfsv4_replace_domain:
            description: If C(true), replaces the owner or group domain with an
                         NFS domain name.
            type: bool
        zone:
            description: Specifies the access zone in which the NFS zone
                         settings apply.
            type: str
    sample: {
        "nfsv4_allow_numeric_ids": true,
        "nfsv4_domain": "sample.com",
        "nfsv4_no_domain": true,
        "nfsv4_no_domain_uids": true,
        "nfsv4_no_names": true,
        "nfsv4_replace_domain": true,
        "zone": "System"
    }
NfsGlobalSettings:
    description: Details of NFS global settings.
    type: dict
    returned: When C(nfs_global_settings) is in a given I(gather_subset)
    contains:
        nfsv3_enabled:
            description: Whether NFSv3 protocol is enabled/disabled.
            type: bool
        nfsv3_rdma_enabled:
            description: Whether rdma is enabled for NFSv3 protocol.
            type: bool
        nfsv40_enabled:
            description: Whether version 0 of NFSv4 protocol is enabled/disabled.
            type: bool
        nfsv41_enabled:
            description: Whether version 1 of NFSv4 protocol is enabled/disabled.
            type: bool
        nfsv42_enabled:
            description: Whether version 2 of NFSv4 protocol is enabled/disabled.
            type: bool
        nfsv4_enabled:
            description: Whether NFSv4 protocol is enabled/disabled.
            type: bool
        rpc_maxthreads:
            description: Specifies the maximum number of threads in the nfsd thread pool.
            type: int
        rpc_minhreads:
            description: Specifies the minimum number of threads in the nfsd thread pool.
            type: int
        rquota_enabled:
            description: Whether the rquota protocol is enabled/disabled.
            type: bool
        service:
            description: Whether the NFS service is enabled/disabled.
            type: bool
    sample: {
        "nfsv3_enabled": false,
        "nfsv3_rdma_enabled": true,
        "nfsv40_enabled": true,
        "nfsv41_enabled": true,
        "nfsv42_enabled": false,
        "nfsv4_enabled": true,
        "rpc_maxthreads": 20,
        "rpc_minthreads": 17,
        "rquota_enabled": true,
        "service": true
    }
NodePools:
    description: List of the Node pools.
    type: list
    returned: When C(node_pools) is in a given I(gather_subset)
    contains:
        id:
            description: ID of the node pool.
            type: str
        lnns:
            description: Node pool's lnns.
            type: list
        name:
            description: Name of the node pool.
            type: str
        protection_policy:
            description: Protection policy of the node pool.
            type: str
        usage:
            description: Usage of the node pool.
            type: dict
    sample: [
        {
            "can_disable_l3": true,
            "can_enable_l3": true,
            "health_flags": [
                "missing_drives"
            ],
            "id": 1,
            "l3": true,
            "l3_status": "l3",
            "lnns": [
                1
            ],
            "manual": false,
            "name": "s210_6.9tb_1.6tb-ssd_64gb",
            "node_type_ids": [
                1
            ],
            "protection_policy": "+2d:1n",
            "tier": null,
            "transfer_limit_pct": 90,
            "transfer_limit_state": "default",
            "usage": {}
        }
    ]
Nodes:
    description: Contain the list of Nodes in the PowerScale cluster.
    type: dict
    returned: When C(nodes) is in a given I(gather_subset)
    contains:
        nodes:
            description: Specifies the deatils of the node.
            type: list
        total:
            description: Total number of nodes.
            type: int
    sample: {
        "nodes": [],
        "total": 1
    }
Providers:
    description: Contains different type of providers in the PowerScale system.
    type: list
    returned: When C(providers) is in a given I(gather_subset)
    contains:
        provider_instances:
            description: List of providers.
            type: list
            contains:
                active_server:
                    description: Active server of the provider.
                    type: str
                connections:
                    description: Different connections of provider.
                    type: str
                groupnet:
                    description: Groupnet of the provider.
                    type: str
                id:
                    description: ID of the provider.
                    type: str
                name:
                    description: Name of the provider.
                    type: str
                status:
                    description: Status of the provider.
                    type: str
                type:
                    description: Type of the provider
                    type: str
                zone_name:
                    description: Access zone of the provider.
                    type: str
    sample: {
        "provider_instances": [
            {
                "active_server": null,
                "connections": [],
                "groupnet": null,
                "id": "lsa-local-provider:System",
                "name": "System",
                "status": "active",
                "type": "local",
                "zone_name": "System"
            }
        ]
    }
SmbOpenFiles:
    description: List of SMB open files.
    type: list
    returned: When C(smb_files) is in a given I(gather_subset)
    contains:
        file:
            description: Path of file within /ifs.
            type: str
        id:
            description: The ID of the SMB open file.
            type: int
        locks:
            description: The number of locks user holds on file.
            type: int
        permission:
            description: The user's permissions on file.
            type: list
        user:
            description: User holding file open.
            type: str
        node:
            description: The node on which the file is open.
            type: str
    sample: [
        {
            "file": "C:\\ifs",
            "id": 1370,
            "locks": 0,
            "node": xx.xx.xx.xx,
            "permissions": [
                "read"
            ],
            "user": "admin"
        }
    ]
SmbShares:
    description: List of the SMB Shares.
    type: list
    returned: When C(smb_shares) is in a given I(gather_subset)
    contains:
        id:
            description: ID of the SMB Share.
            type: str
        name:
            description: Name of the SMB Share.
            type: str
    sample: [
        {
            "id": "Atest",
            "name": "Atest"
        }
    ]
StoragePoolTiers:
    description: List of the storage pool tiers.
    type: list
    returned: When C(storagepool_tiers) is in a given I(gather_subset)
    contains:
        children:
            description: Children in the storage pool tiers.
            type: list
        id:
            description: ID of the storage pool tier.
            type: str
        lnns:
            description: Storage pool tier's lnn.
            type: list
        name:
            description: Name of the storage pool tier.
            type: str
        usage:
            description: Usage of the storage pool tiers.
            type: list
    sample: [
        {
            "children": [],
            "id": 984,
            "lnns": [],
            "name": "Ansible_Tier_1",
            "usage": {}
        }
    ]
SynciqPerformanceRules:
    description: List of SyncIQ performance rules.
    type: list
    returned: When C(synciq_performance_rules) is in a given I(gather_subset)
    contains:
        enabled:
            description: Whether SyncIQ performance rule enabled.
            type: bool
        id:
            description: ID of the SyncIQ performance rule.
            type: str
        limit:
            description: Limits of the SyncIQ performance rule.
            type: str
        schedule:
            description: Schedule of the SyncIQ performance rule.
            type: dict
        type:
            description: The type of the SyncIQ performance rule.
            type: str
    sample: [
        {
            "enabled": true,
            "id": "fc-0",
            "limit": "1files/sec",
            "schedule": {},
            "type": "file_count"
        }
    ]
SynciqPolicies:
    description: List of the SyncIQ policies.
    type: list
    returned: When C(synciq_policies) is in a given I(gather_subset)
    contains:
        enabled:
            description: Whether SyncIQ policies enabled.
            type: bool
        id:
            description: ID of the SyncIQ policies.
            type: str
        name:
            description: Name of the SyncIQ policies.
            type: str
        schedule:
            description: Schedule of the SyncIQ policies.
            type: str
        source_root_path:
            description: Source path of the SyncIQ policies.
            type: str
        target_path:
            description: Target path of the SyncIQ policies.
            type: str
    sample: [
        {
            "enabled": true,
            "id": "1ee8ad74f6f147894d21e339d57c3d1b",
            "name": "dk2-nginx-10-230-24-249-Five_Minutes",
            "schedule": "when-source-modified",
            "source_root_path": "/ifs/data/sample-x.x.x.x-Five_Minutes",
            "target_path": "/ifs/data/dk2-nginx-x.x.x.x-Five_Minutes"
        }
    ]
SynciqReports:
    description: List of the SyncIQ reports.
    type: list
    returned: When C(synciq_reports) is in a given I(gather_subset)
    contains:
        id:
            description: ID of the SyncIQ reports.
            type: str
        name:
            description: Name of the SyncIQ reports.
            type: str
    sample: [
        {
            "id": "1ee8ad74f6f147894d21e339d57c3d1b",
            "name": "dk2-nginx-10-230-24-249-Five_Minutes"
        }
    ]
SynciqTargetClusterCertificate:
    description: List of the SyncIQ Target cluster certificates.
    type: list
    returned: When C(synciq_target_cluster_certificates) is in a given I(gather_subset)
    contains:
        id:
            description: ID of the SyncIQ Target cluster certificates.
            type: str
        name:
            description: Name of the SyncIQ Target cluster certificates.
            type: str
    sample: [
        {
            "id": "077f119e54ec2c12c74f011433cd33ac5c",
            "name": "sample"
        }
    ]
SynciqTargetReports:
    description: List of the SyncIQ Target reports.
    type: list
    returned: When C(synciq_target_reports) is in a given I(gather_subset)
    contains:
        id:
            description: ID of the SyncIQ Target reports.
            type: str
        name:
            description: Name of the SyncIQ Target reports.
            type: str
    sample: [
        {
            "id": "cicd-repctl-0419-t151741-10-247-100-10-Five_Minutes",
            "name": "cicd-repctl-0419-t1741-10-247-100-10-Five_Minutes"
        }
    ]
UserMappingRules:
    description: List of the User mapping rules.
    type: list
    returned: When C(user_mapping_rules) is in a given I(gather_subset)
    contains:
        apply_order:
            description: Current order of the rule.
            type: int
        operator:
            description: The operation that a rule carries out.
            type: str
        options:
            description: The operation that a rule carries out.
            type: dict
        user1:
            description: A UNIX user or an Active Directory user.
            type: dict
        user2:
            description: A UNIX user or an Active Directory user.
            type: dict
    sample: [
        {
            "apply_order": 1,
            "operator": "append",
            "options": {
                "_break": false,
                "default_user": null,
                "group": true,
                "groups": true,
                "user": true
            },
            "user1": {
                "domain": null,
                "user": "test_user_2"
            },
            "user2": {
                "domain": null,
                "user": "test_user_1"
            }
        }
    ]
Users:
    description: List of all Users.
    type: list
    returned: When C(users) is in a given I(gather_subset)
    contains:
        users:
            description: List of users details.
            type: list
            contains:
                id:
                    description: ID of the user.
                    type: str
                name:
                    description: Name of the user.
                    type: str
                provider:
                    description: The provider of the user.
                    type: str
    sample: [
        "users": [
            {
                "dn": "CN=test_ans_user,CN=Users,DC=X-ISILON-X",
                "dns_domain": null,
                "domain": "x-ISILON-X",
                "email": "testuser_ans@dell.com",
                "gid": {
                    "id": "GID:1800",
                    "name": null,
                    "type": null
                },
                "home_directory": "/ifs/home/test_ans_user",
                "id": "test_ans_user",
                "name": "test_ans_user",
                "on_disk_user_identity": {
                    "id": "UID:2016",
                    "name": null,
                    "type": null
                },
                "password_expired": false,
                "primary_group_sid": {
                    "id": "SID:S-1-5-21-2193650305-1279797252-961391754-800",
                    "name": null,
                    "type": null
                },
                "prompt_password_change": false,
                "provider": "lsa-local-provider:System",
                "sam_account_name": "test_ans_user",
                "shell": "/bin/zsh",
                "sid": {
                    "id": "SID:S-1-5-21-2193650305-1279797252-961391754-1025",
                    "name": null,
                    "type": null
                },
                "ssh_public_keys": [],
                "type": "user",
                "uid": {
                    "id": "UID:2016",
                    "name": null,
                    "type": null
                },
                "upn": "test_ans_user@x-ISILON-X",
                "user_can_change_password": true
            }
        ]
    ]
nfs_default_settings:
    description: The NFS default settings.
    type: dict
    returned: always
    contains:
        map_root:
            description: Mapping of incoming root users to a specific user and/or group ID.
            type: dict
        map_non_root:
            description: Mapping of non-root users to a specific user and/or group ID.
            type: dict
        map_failure:
            description: Mapping of users to a specific user and/or group ID after a failed auth attempt.
            type: dict
        name_max_size:
            description: Specifies the reported maximum length of a file name. This parameter does
                not affect server behavior, but is included to accommodate legacy client
                requirements.
            type: dict
        block_size:
            description: Specifies the block size returned by the NFS statfs procedure.
            type: dict
        directory_transfer_size:
            description: Specifies the preferred size for directory read operations. This value is
                used to advise the client of optimal settings for the server, but is not
                enforced.
            type: dict
        read_transfer_max_size:
            description: Specifies the maximum buffer size that clients should use on NFS read
                requests. This value is used to advise the client of optimal settings for
                the server, but is not enforced.
            type: dict
        read_transfer_multiple:
            description: Specifies the preferred multiple size for NFS read requests. This value is
                used to advise the client of optimal settings for the server, but is not
                enforced.
            type: dict
        read_transfer_size:
            description: Specifies the preferred size for NFS read requests. This value is used to
                advise the client of optimal settings for the server, but is not enforced.
            type: dict
        write_transfer_max_size:
            description: Specifies the maximum buffer size that clients should use on NFS write
                requests. This value is used to advise the client of optimal settings for
                the server, but is not enforced.
            type: dict
        write_transfer_multiple:
            description: Specifies the preferred multiple size for NFS write requests. This value is
                used to advise the client of optimal settings for the server, but is not
                enforced.
            type: dict
        write_transfer_size:
            description: Specifies the preferred multiple size for NFS write requests. This value is
                used to advise the client of optimal settings for the server, but is not
                enforced.
            type: dict
        max_file_size:
            description: Specifies the maximum file size for any file accessed from the export. This
                parameter does not affect server behavior, but is included to accommodate
                legacy client requirements.
            type: dict
        security_flavors:
            description: Specifies the authentication types that are supported for this export.
            type: list
        commit_asynchronous:
            description: True if NFS commit requests execute asynchronously.
            type: bool
        setattr_asynchronous:
            description: True if set attribute operations execute asynchronously.
            type: bool
        readdirplus:
            description: True if 'readdirplus' requests are enabled. Enabling this property might
                improve network performance and is only available for NFSv3.
            type: bool
        return_32bit_file_ids:
            description: Limits the size of file identifiers returned by NFSv3+ to 32-bit values (may
                require remount).
            type: bool
        can_set_time:
            description: True if the client can set file times through the NFS set attribute
                request. This parameter does not affect server behavior, but is included to
                accommodate legacy client requirements.
            type: bool
        map_lookup_uid:
            description: True if incoming user IDs (UIDs) are mapped to users in the OneFS user
                database. When set to False, incoming UIDs are applied directly to file
                operations.
            type: bool
        symlinks:
            description: True if symlinks are supported. This value is used to advise the client of
                optimal settings for the server, but is not enforced.
            type: bool
        write_datasync_action:
            description: Specifies the synchronization type for data sync action.
            type: str
        write_datasync_reply:
            description: Specifies the synchronization type for data sync reply.
            type: str
        write_filesync_action:
            description: Specifies the synchronization type for file sync action.
            type: str
        write_filesync_reply:
            description: Specifies the synchronization type for file sync reply.
            type: str
        write_unstable_action:
            description: Specifies the synchronization type for unstable action.
            type: str
        write_unstable_reply:
            description: Specifies the synchronization type for unstable reply.
            type: str
        encoding:
            description: Specifies the default character set encoding of the clients connecting to
                the export, unless otherwise specified.
            type: str
        time_delta:
            description: Specifies the resolution of all time values that are returned to the
                clients.
            type: dict
        zone:
            description: The zone to which the NFS default settings apply.
            type: str
    sample: {
                'map_root': {
                    'enabled': True,
                    'primary_group': {
                        'id': None,
                        'name': None,
                        'type': None
                    },
                    'secondary_groups': [],
                    'user': {
                        'id': 'USER:nobody',
                        'name': None,
                        'type': None
                    }
                },
                'map_non_root': {
                    'enabled': False,
                    'primary_group': {
                        'id': None,
                        'name': None,
                        'type': None
                    },
                    'secondary_groups': [],
                    'user': {
                        'id': 'USER:nobody',
                        'name': None,
                        'type': None
                    }
                },
                'map_failure': {
                    'enabled': False,
                    'primary_group': {
                        'id': None,
                        'name': None,
                        'type': None
                    },
                    'secondary_groups': [],
                    'user': {
                        'id': 'USER:nobody',
                        'name': None,
                        'type': None
                    }
                },
                'name_max_size': 255,
                'block_size': 8192,
                'commit_asynchronous': False,
                'directory_transfer_size': 131072,
                'read_transfer_max_size': 1048576,
                'read_transfer_multiple': 512,
                'read_transfer_size': 131072,
                'setattr_asynchronous': False,
                'write_datasync_action': 'DATASYNC',
                'write_datasync_reply': 'DATASYNC',
                'write_filesync_action': 'FILESYNC',
                'write_filesync_reply': 'FILESYNC',
                'write_transfer_max_size': 1048576,
                'write_transfer_multiple': 512,
                'write_transfer_size': 524288,
                'write_unstable_action': 'UNSTABLE',
                'write_unstable_reply': 'UNSTABLE',
                'max_file_size': 9223372036854775807,
                'readdirplus': True,
                'return_32bit_file_ids': False,
                'can_set_time': True,
                'encoding': 'DEFAULT',
                'map_lookup_uid': False,
                'symlinks': True,
                'time_delta': 1e-09,
                'zone': 'sample-zone'
            }
SynciqGlobalSettings:
    description: The SyncIQ global settings details.
    type: dict
    returned: always
    contains:
        bandwidth_reservation_reserve_absolute:
            description: The absolute bandwidth reservation for SyncIQ.
            type: int
        bandwidth_reservation_reserve_percentage:
            description: The percentage-based bandwidth reservation for SyncIQ.
            type: int
        cluster_certificate_id:
            description: The ID of the cluster certificate used for SyncIQ.
            type: str
        encryption_cipher_list:
            description: The list of encryption ciphers used for SyncIQ.
            type: str
        encryption_required:
            description: Whether encryption is required or not for SyncIQ.
            type: bool
        force_interface:
            description: Whether the force interface is enabled or not for SyncIQ.
            type: bool
        max_concurrent_jobs:
            description: The maximum number of concurrent jobs for SyncIQ.
            type: int
        ocsp_address:
            description: The address of the OCSP server used for SyncIQ certificate validation.
            type: str
        ocsp_issuer_certificate_id:
            description: The ID of the issuer certificate used for OCSP validation in SyncIQ.
            type: str
        preferred_rpo_alert:
            description: Whether the preferred RPO alert is enabled or not for SyncIQ.
            type: bool
        renegotiation_period:
            description: The renegotiation period in seconds for SyncIQ.
            type: int
        report_email:
            description: The email address to which SyncIQ reports are sent.
            type: str
        report_max_age:
            description: The maximum age in days of reports that are retained by SyncIQ.
            type: int
        report_max_count:
            description: The maximum number of reports that are retained by SyncIQ.
            type: int
        restrict_target_network:
            description: Whether to restrict the target network in SyncIQ.
            type: bool
        rpo_alerts:
            description: Whether RPO alerts are enabled or not in SyncIQ.
            type: bool
        service:
            description: Specifies whether the SyncIQ service is currently on, off, or paused.
            type: str
        service_history_max_age:
            description: The maximum age in days of service history that is retained by SyncIQ.
            type: int
        service_history_max_count:
            description: The maximum number of service history records that are retained by SyncIQ.
            type: int
        source_network:
            description: The source network used by SyncIQ.
            type: str
        tw_chkpt_interval:
            description: The interval between checkpoints in seconds in SyncIQ.
            type: int
        use_workers_per_node:
           description : Whether to use workers per node in SyncIQ or not.
           type : bool
    sample: {
              "bandwidth_reservation_reserve_absolute": null,
              "bandwidth_reservation_reserve_percentage": 1,
              "cluster_certificate_id": "xxxx",
              "encryption_cipher_list": "",
              "encryption_required": true,
              "force_interface": false,
              "max_concurrent_jobs": 16,
              "ocsp_address": "",
              "ocsp_issuer_certificate_id": "",
              "preferred_rpo_alert": 0,
              "renegotiation_period": 28800,
              "report_email": [],
              "report_max_age": 31536000,
              "report_max_count": 2000,
              "restrict_target_network": false,
              "rpo_alerts": true,
              "service": "off",
              "service_history_max_age": 31536000,
              "service_history_max_count": 2000,
              "source_network": null,
              "tw_chkpt_interval": null,
              "use_workers_per_node": false
            }
S3_bucket_details:
    description: The updated S3 Bucket details.
    type: dict
    returned: When C(s3_buckets) is in a given I(gather_subset)
    contains:
        acl:
            description: Specifies the properties of S3 access controls.
            type: list
            contains:
                grantee:
                    description: Specifies details of grantee.
                    type: dict
                    contains:
                        id:
                            description: ID of the grantee.
                            type: str
                        name:
                            description: Name of the grantee.
                            type: str
                        type:
                            description: Specifies the type of the grantee.
                            type: str
                permission:
                    description: Specifies the S3 permission being allowed.
                    type: str
        description:
            description: Specifies the description of the S3 bucket.
            type: str
        id:
            description: S3 bucket ID.
            type: str
        name:
            description: S3 bucket name.
            type: str
        object_acl_policy:
            description: Set behaviour of object acls for a specified S3
                         bucket.
            type: str
        owner:
            description: Specifies the owner of the S3 bucket.
            type: str
        path:
            description: Path of S3 bucket with in C('/ifs').
            type: str
        zid:
            description: Zone id.
            type: int
        zone:
            description: Access zone name.
            type: str
    sample: {
        "access_zone": "System",
        "acl": [{
            "grantee": {
                "id": "ID",
                "name": "ansible-user",
                "type": "user"
                },
            "permission": "READ"
        }],
        "description": "description",
        "id": "ansible_S3_bucket",
        "name": "ansible_S3_bucket",
        "object_acl_policy": "replace",
        "owner": "ansible-user",
        "path": "/ifs/<sample-path>",
        "zid": 1
    }
SmbGlobalSettings:
    description: The updated SMB global settings details.
    type: dict
    returned: always
    contains:
      access_based_share_enum:
        description: Only enumerate files and folders the requesting user has access to.
        type: bool
      audit_fileshare:
        description: Specify level of file share audit events to log.
        type: str
      audit_logon:
        description: Specify the level of logon audit events to log.
        type: str
      dot_snap_accessible_child:
        description: Allow access to .snapshot directories in share subdirectories.
        type: bool
      dot_snap_accessible_root:
        description: Allow access to the .snapshot directory in the root of the share.
        type: bool
      dot_snap_visible_child:
        description: Show .snapshot directories in share subdirectories.
        type: bool
      dot_snap_visible_root:
        description: Show the .snapshot directory in the root of a share.
        type: bool
      enable_security_signatures:
        description: Indicates whether the server supports signed SMB packets.
        type: bool
      guest_user:
        description: Specifies the fully-qualified user to use for guest access.
        type: str
      ignore_eas:
        description: Specify whether to ignore EAs on files.
        type: bool
      onefs_cpu_multiplier:
        description: Specify the number of OneFS driver worker threads per CPU.
        type: int
      onefs_num_workers:
        description: Set the maximum number of OneFS driver worker threads.
        type: int
      reject_unencrypted_access:
        description: If SMB3 encryption is enabled, reject unencrypted access from clients.
        type: bool
      require_security_signatures:
        description: Indicates whether the server requires signed SMB packets.
        type: bool
      server_side_copy:
        description: Enable Server Side Copy.
        type: bool
      server_string:
        description: Provides a description of the server.
        type: str
      service:
        description: Specify whether service is enabled.
        type: bool
      srv_cpu_multiplier:
        description: Specify the number of SRV service worker threads per CPU.
        type: int
      srv_num_workers:
        description: Set the maximum number of SRV service worker threads.
        type: int
      support_multichannel:
        description: Support multichannel.
        type: bool
      support_netbios:
        description: Support NetBIOS.
        type: bool
      support_smb2:
        description: The support SMB2 attribute.
        type: bool
      support_smb3_encryption:
        description: Support the SMB3 encryption on the server.
        type: bool
    sample: {
      "access_based_share_enum": false,
      "audit_fileshare": null,
      "audit_logon": null,
      "dot_snap_accessible_child": true,
      "dot_snap_accessible_root": true,
      "dot_snap_visible_child": false,
      "dot_snap_visible_root": true,
      "enable_security_signatures": false,
      "guest_user": "nobody",
      "ignore_eas": false,
      "onefs_cpu_multiplier": 4,
      "onefs_num_workers": 0,
      "reject_unencrypted_access": false,
      "require_security_signatures": false,
      "server_side_copy": false,
      "server_string": "PowerScale Server",
      "service": true,
      "srv_cpu_multiplier": null,
      "srv_num_workers": null,
      "support_multichannel": true,
      "support_netbios": false,
      "support_smb2": true,
      "support_smb3_encryption": true
    }
email_settings:
    description: Details of the email settings.
    type: dict
    returned: Always
    contains:
        settings:
            description: Details of the settings.
            returned: Always
            type: dict
            contains:
                batch_mode:
                    description: This setting determines how notifications will be batched together to be sent by email.
                    type: str
                mail_relay:
                    description: The address of the SMTP server to be used for relaying the notification messages.
                    type: str
                mail_sender:
                    description: The full email address that will appear as the sender of notification messages.
                    type: str
                mail_subject:
                    description: The subject line for notification messages from this cluster.
                    type: str
                smtp_auth_passwd_set:
                    description: Indicates if an SMTP authentication password is set.
                    type: bool
                smtp_auth_security:
                    description: The type of secure communication protocol to use if SMTP is being used.
                    type: str
                smtp_auth_username:
                    description: Username to authenticate with if SMTP authentication is being used.
                    type: str
                smtp_port:
                    description: The port on the SMTP server to be used for relaying the notification messages.
                    type: int
                use_smtp_auth:
                    description: If true, this cluster will send SMTP authentication credentials to the
                                SMTP relay server in order to send its notification emails.
                    type: bool
                user_template:
                    description: Location of a custom template file that can be used to specify the layout of the notification emails.
                    type: str
    sample:
        {
            "settings": {
                "batch_mode": "none",
                "mail_relay": "10.**.**.**",
                "mail_sender": "powerscale@dell.com",
                "mail_subject": "Powerscale Cluster notifications",
                "smtp_auth_passwd_set": false,
                "smtp_auth_security": "none",
                "smtp_auth_username": "",
                "smtp_port": 25,
                "use_smtp_auth": false,
                "user_template": ""
            }
        }

ntp_servers:
    description: List of NTP servers.
    type: dict
    returned: Always
    contains:
        servers:
            description: List of servers.
            type: list
            contains:
                id:
                    description: Field id.
                    type: str
                key:
                    description: Key value from I(key_file) that maps to this server.
                    type: str
                name:
                    description: NTP server name.
                    type: str
    sample:
        {
            "servers": [
                {
                    "id": "10.**.**.**",
                    "key": null,
                    "name": "10.**.**.**"
                }
            ]
        }
cluster_identity:
    description: Details related to cluster identity.
    type: dict
    returned: Always
    contains:
        description:
            description: Description of PowerScale cluster.
            type: str
        logon:
            description: Details of logon message shown on Powerscale login screen.
            type: dict
            contains:
                motd:
                    description: Details of logon message.
                    type: str
                motd_header:
                    description: Details of logon message title.
                    type: str
        mttdl_level_msg:
            description: mttdl_level_msg.
            type: str
        name:
            description: Name of PowerScale cluster.
            type: str
    sample:
        {
           "cluster_identity":
           {
                "description": "asdadasdasdasdadadadds",
                "logon":
                {
                    "motd": "This is new description",
                    "motd_header": "This is the new title"
                },
                "mttdl_level_msg": "none",
                "name": "PIE-IsilonS-24241-Clusterwrerwerwrewr"
            }
        }
cluster_owner:
    description: Details related to cluster identity.
    type: dict
    returned: Always
    contains:
        company:
            description: Name of the company.
            type: str
        location:
            description: Location of the company.
            type: str
        primary_email:
            description: Email of primary system admin.
            type: str
        primary_name:
            description: Name of primary system admin.
            type: str
        primary_phone1:
            description: Phone1 of primary system admin.
            type: str
        primary_phone2:
            description: Phone2 of primary system admin.
            type: str
        secondary_email:
            description: Email of secondary system admin.
            type: str
        secondary_name:
            description: Name of secondary system admin.
            type: str
        secondary_phone1:
            description: Phone1 of secondary system admin.
            type: str
        secondary_phone2:
            description: Phone2 of secondary system admin.
            type: str
    sample:
        {
           "cluster_owner":
           {
                "company": "Test company",
                "location": "Test location",
                "primary_email": "primary_email@email.com",
                "primary_name": "primary_name",
                "primary_phone1": "primary_phone1",
                "primary_phone2": "primary_phone2",
                "secondary_email": "secondary_email@email.com",
                "secondary_name": "secondary_name",
                "secondary_phone1": "secondary_phone1",
                "secondary_phone2": "secondary_phone2"
            }
        }
SnmpSettings:
    description: The SNMP settings details.
    type: dict
    returned: When C(snmp_settings) is in a given I(gather_subset)
    contains:
        read_only_community:
            description: SNMP Read-only community name.
            type: str
        service:
            description: Whether the SNMP Service is enabled.
            type: bool
        snmp_v1_v2c_access:
            description: Whether the SNMP v2c access is enabled.
            type: bool
        snmp_v3_access:
            description: Whether the SNMP v3 access is enabled.
            type: bool
        snmp_v3_auth_protocol:
            description: SNMP v3 authentication protocol.
            type: str
        snmp_v3_priv_protocol:
            description: SNMP v3 privacy protocol.
            type: str
        snmp_v3_security_level:
            description: SNMP v3 security level.
            type: str
        snmp_v3_read_only_user:
            description: SNMP v3 read-only user.
            type: str
        system_contact:
            description: SNMP system owner contact information.
            type: str
        system_location:
            description: The cluster description of the SNMP system.
            type: str
    sample: {
        "read_only_community": "public",
        "service": true,
        "snmp_v1_v2c_access": true,
        "snmp_v3_access": true,
        "snmp_v3_auth_protocol": "MD5",
        "snmp_v3_priv_protocol": "DES",
        "snmp_v3_security_level": "authPriv",
        "snmp_v3_read_only_user": "general",
        "system_contact": "system",
        "system_location": "cluster"
    }
ServerCertificate:
    description: The Server certificate details.
    type: list
    returned: When C(server_certificate) is in a given I(gather_subset)
    contains:
        description:
            description: Description of the certificate.
            type: str
        id:
            description: System assigned certificate id.
            type: str
        issuer:
            description: Name of the certificate issuer.
            type: str
        name:
            description: Name for the certificate.
            type: str
        not_after:
            description: The date and time from which the certificate becomes valid and
                can be used for authentication and encryption.
            type: str
        not_before:
            description: The date and time until which the certificate is valid and
                can be used for authentication and encryption.
            type: str
        status:
            description: Status of the certificate.
            type: str
        fingerprints:
            description: Fingerprint details of the certificate.
            type: str
        dnsnames:
            description: Subject alternative names of the certificate.
            type: list
        subject:
            description: Subject of the certificate.
            type: str
        certificate_monitor_enabled:
            description: Boolean value indicating whether certificate expiration monitoring is enabled.
            type: bool
        certificate_pre_expiration_threshold:
            description: The number of seconds before certificate expiration that the certificate expiration
                monitor will start raising alerts.
            type: int
    sample:
        [{
            "certificate_monitor_enabled": true,
            "certificate_pre_expiration_threshold": 4294,
            "description": "This the example test description",
            "dnsnames": ["powerscale"],
            "fingerprints": [
                {
                    "type": "SHA1",
                    "value": "68:b2:d5:5d:cc:b0:70:f1:f0:39:3a:bb:e0:44:49:70:6e:05:c3:ed"
                },
                {
                    "type": "SHA256",
                    "value": "69:99:b9:c0:29:49:c9:62:e8:4b:60:05:60:a8:fa:f0:01:ab:24:43:8a:47:4c:2f:66:2c:95:a1:7c:d8:10:34"
                }],
            "id": "6999b9c02949c962e84b600560a8faf001ab24438a474c2f662c95a17cd81034",
            "issuer": "C=IN, ST=Karnataka, L=Bangalore, O=Dell, OU=ISG, CN=powerscale, emailAddress=contact@dell.com",
            "name": "test",
            "not_after": 1769586969,
            "not_before": 1706514969,
            "status": "valid",
            "subject": "C=IN, ST=Karnataka, L=Bangalore, O=Dell, OU=ISG, CN=powerscale, emailAddress=contact@dell.com"
        }]
roles:
    description: List of auth roles.
    type: dict
    returned: When C(roles) is in a given I(gather_subset)
    contains:
        description:
            description: Description of the auth role.
            type: str
        id:
            description: id of the auth role.
            type: str
        name:
            description: Name of the auth role.
            type: str
        members:
            description: Specifies the members of auth role.
            type: list
            contains:
                id:
                    description: ID of the member.
                    type: str
                name:
                    description: Name of the member.
                    type: str
                type:
                    description: Specifies the type of the member.
                    type: str
        privileges:
            description: Specifies the privileges of auth role.
            type: list
            contains:
                id:
                    description: ID of the privilege.
                    type: str
                name:
                    description: Name of the privilege.
                    type: str
                permission:
                    description: Specifies the permission of the privilege.
                    type: str
    sample:
        {
           "roles":
           [{
                "description" : "Test_Description",
                "id" : "Test_Role",
                "members" : [{
                    "id" : "UID:2008",
                    "name" : "esa",
                    "type" : "user"
                }],
                "name" : "Test_Role",
                "privileges" : [{
                    "id" : "ISI_PRIV_LOGIN_PAPI",
                    "name" : "Platform API",
                    "permission" : "r"
                }]
            }]
        }
smart_quota:
  description: The smart quota details.
  type: list
  returned: always
  contains:
        id:
            description: The ID of the Quota.
            type: str
            sample: "2nQKAAEAAAAAAAAAAAAAQIMCAAAAAAAA"
        enforced:
            description: Whether the limits are enforced on Quota or not.
            type: bool
            sample: true
        container:
            description: If C(true), SMB shares using the quota directory see the quota thresholds as share size.
            type: bool
            sample: true
        thresholds:
            description: Includes information about all the limits imposed on quota.
                         The limits are mentioned in bytes and I(soft_grace) is in seconds.
            type: dict
            sample: {
                    "advisory": 3221225472,
                    "advisory(GB)": "3.0",
                    "advisory_exceeded": false,
                    "advisory_last_exceeded": 0,
                    "hard": 6442450944,
                    "hard(GB)": "6.0",
                    "hard_exceeded": false,
                    "hard_last_exceeded": 0,
                    "soft": 5368709120,
                    "soft(GB)": "5.0",
                    "soft_exceeded": false,
                    "soft_grace": 3024000,
                    "soft_last_exceeded": 0
                }
        type:
            description: The type of Quota.
            type: str
            sample: "directory"
        usage:
            description: The Quota usage.
            type: dict
            sample: {
                    "inodes": 1,
                    "logical": 0,
                    "physical": 2048
                }
  sample: [
    {
    "container": true,
    "description": "",
    "efficiency_ratio": null,
    "enforced": false,
    "id": "iddd",
    "include_snapshots": false,
    "labels": "",
    "linked": false,
    "notifications": "default",
    "path": "VALUE_SPECIFIED_IN_NO_LOG_PARAMETER",
    "persona": {
        "id": "UID:9355",
        "name": "test_user_12",
        "type": "user"
    },
    "ready": true,
    "reduction_ratio": null,
    "thresholds": {
        "advisory": null,
        "advisory_exceeded": false,
        "advisory_last_exceeded": null,
        "hard": null,
        "hard_exceeded": false,
        "hard_last_exceeded": null,
        "percent_advisory": null,
        "percent_soft": null,
        "soft": null,
        "soft_exceeded": false,
        "soft_grace": null,
        "soft_last_exceeded": null
    },
    "thresholds_on": "applogicalsize",
    "type": "user",
    "usage": {
        "applogical": 0,
        "applogical_ready": true,
        "fslogical": 0,
        "fslogical_ready": true,
        "fsphysical": 0,
        "fsphysical_ready": false,
        "inodes": 0,
        "inodes_ready": true,
        "physical": 0,
        "physical_data": 0,
        "physical_data_ready": true,
        "physical_protection": 0,
        "physical_protection_ready": true,
        "physical_ready": true,
        "shadow_refs": 0,
        "shadow_refs_ready": true
    }
    }
    ]
file_system:
  description: The filesystem details.
  type: list
  returned: always
  contains:
        name:
            description: The name of the filesystem.
            type: str
            sample: "home"
  sample: [
        {
            "name": "home"
        },
        {
            "name": "smb11"
        }
    ]
support_assist_settings:
    description: The support assist settings details.
    type: dict
    returned: When C(support_assist_settings) is in a given I(gather_subset)
    contains:
        automatic_case_creation:
            description: C(True) indicates automatic case creation is enabled.
            type: bool
        connection:
            description: Support assist connection details.
            type: dict
            contains:
                gateway_endpoints:
                    description: List of gateway endpoints.
                    type: list
                    elements: dict
                    contains:
                        gateway_host:
                            description: Hostname or IP address of the gateway endpoint.
                            type: str
                        gateway_port:
                            description: Port number of the gateway endpoint.
                            type: int
                        priority:
                            description: Priority of the gateway endpoint.
                            type: int
                        use_proxy:
                            description: Use proxy.
                            type: bool
                        validate_ssl:
                            description: Validate SSL.
                            type: bool
                        enabled:
                            description: Enable the gateway endpoint.
                            type: bool
                mode:
                    description: Connection mode.
                    type: str
                network_pools:
                    description: List of network pools.
                    type: list
                    elements: dict
                    contains:
                        pool:
                            description: Name of the network pool.
                            type: str
                        subnet:
                            description: Name of the subnet of the network pool.
                            type: str
        connection_state:
            description: Set connectivity state.
            type: str
        contact:
            description: Information on the remote support contact.
            type: dict
            contains:
                primary:
                    description: Primary contact details.
                    type: dict
                    contains:
                        first_name:
                            description: First name of the primary contact.
                            type: str
                        last_name:
                            description: Last name of the primary contact.
                            type: str
                        email:
                            description: Email address of the primary contact.
                            type: str
                        phone:
                            description: Phone number of the primary contact.
                            type: str
                secondary:
                    description: Secondary contact details.
                    type: dict
                    contains:
                        first_name:
                            description: First name of the secondary contact.
                            type: str
                        last_name:
                            description: Last name of the secondary contact.
                            type: str
                        email:
                            description: Email address of the secondary contact.
                            type: str
                        phone:
                            description: Phone number of the secondary contact.
                            type: str
        telemetry:
            description: Enable telemetry.
            type: dict
            contains:
                offline_collection_period:
                    description:
                    - Change the offline collection period for when the connection to gateway is down.
                    - The range is 0 to 86400.
                    type: int
                telemetry_enabled:
                    description: Change the status of telemetry.
                    type: bool
                telemetry_persist:
                    description: Change if files are kept after upload.
                    type: bool
                telemetry_threads:
                    description:
                    - Change the number of threads for telemetry gathers.
                    - The range is 1 to 64.
                    type: int
        enable_download:
            description: C(True) indicates downloads are enabled.
            type: bool
        enable_remote_support:
            description: Allow remote support.
            type: bool
        enable_service:
            description: Enable/disable Support Assist service.
            type: bool
        accepted_terms:
            description: Whether to accept or reject the terms and conditions for remote support.
            type: bool
    sample: {
      "automatic_case_creation": false,
      "connection": {
          "gateway_endpoints": [
                {
                    "enabled": true,
                    "host": "XX.XX.XX.XX",
                    "port": 9443,
                    "priority": 1,
                    "use_proxy": false,
                    "validate_ssl": false
                },
                {
                    "enabled": true,
                    "host": "XX.XX.XX.XY",
                    "port": 9443,
                    "priority": 2,
                    "use_proxy": false,
                    "validate_ssl": false
                }
            ],
            "mode": "gateway",
            "network_pools": [
                {
                    "pool": "pool1",
                    "subnet": "subnet0"
                }
            ]
        },
      "connection_state": "disabled",
      "contact": {
          "primary": {
              "email": "p7VYg@example.com",
              "first_name": "Eric",
              "last_name": "Nam",
              "phone": "1234567890"
           },
           "secondary": {
              "email": "kangD@example.com",
              "first_name": "Daniel",
              "last_name": "Kang",
              "phone": "1234567891"
            }
        },
      "enable_download": false,
      "enable_remote_support": false,
      "onefs_software_id": "ELMISL1019H4GY",
      "supportassist_enabled": true,
      "telemetry": {
          "offline_collection_period": 60,
          "telemetry_enabled": true,
          "telemetry_persist": true,
          "telemetry_threads": 10
        }
    }
alert_settings:
    description: The alert settings details.
    type: dict
    returned: When C(alert_settings) is in a given I(gather_subset).
    contains:
        history:
            description: History list of CELOG maintenance mode windows.
            type: list
            contains:
                end:
                    description:
                        - End time of CELOG maintenance mode, as a UNIX
                          timestamp in seconds.
                        - Value 0 indicates that maintenance mode is still
                          enabled.
                    type: int
                start:
                    description: Start time of CELOG maintenance mode, as a UNIX
                                 timestamp in seconds.
                    type: int
        maintenance:
            description: Indicates if maintenance mode is enabled.
            type: bool
    sample: {
        history: [
            {
                "end": 0,
                "start": 1719822336,
            }
        ],
        "maintenance": "false"
    }
alert_categories:
    description: The alert categories details.
    type: list
    returned: When C(alert_categories) is in a given I(gather_subset).
    contains:
        categories:
            description: High level categorisation of eventgroups.
            type: list
            contains:
                id:
                    description: Numeric identifier of eventgroup category.
                    type: str
                id_name:
                    description: Name of category.
                    type: str
                name:
                    description: Description of category.
                    type: str
        resume:
            description: Provide this token as the 'resume' query argument to continue listing results.
            type: str
        total:
            description: Total number of items available.
            type: int
    sample: {
        categories: [
            {
                "id": "200000000",
                "id_name": "NODE_STATUS_EVENTS",
                "name": "Node status events",
            }
        ],
        "resume": null,
        "total": 1
    }
alert_channels:
    description: The alert channels details.
    type: list
    returned: When C(alert_channels) is in a given I(gather_subset).
    contains:
        channels:
            description: Named channel through which alerts can be delivered.
            type: list
            contains:
                allowed_nodes:
                    description: Nodes (LNNs) that can be masters for this channel.
                    type: list
                enabled:
                    description: Channel is to be used or not.
                    type: bool
                excluded_nodes:
                    description: Nodes (LNNs) that cannot be masters for this channel.
                    type: list
                parameters:
                    description: Parameters to be used for an smtp channel.
                    type: dict
                    contains:
                        address:
                            description: Email addresses to send to.
                            type: list
                        batch:
                            description: Batching criterion.
                            type: str
                        batch_period:
                            description: Period over which batching is to be performed.
                            type: int
                        custom_template:
                            description: Path to custom notification template.
                            type: str
                        send_as:
                            description: Email address to use as from.
                            type: str
                        smtp_host:
                            description: SMTP host.
                            type: str
                        smtp_password:
                            description: Password for SMTP authentication, only if
                                         smtp_use_auth true.
                            type: str
                        smtp_port:
                            description: SMTP relay port. It defaults to 25.
                            type: int
                        smtp_security:
                            description: Encryption protocol to use for SMTP.
                            type: str
                        smtp_use_auth:
                            description: Use SMTP authentication. It defaults to false.
                            type: bool
                        smtp_username:
                            description: Username for SMTP authentication, only if smtp_use_auth true.
                            type: str
                        subject:
                            description: Subject for emails.
                            type: str
                system:
                    description: Channel is a pre-defined system channel.
                    type: bool
                type:
                    description: The mechanism used by the channel.
                    type: str
                id:
                    description: Unique identifier.
                    type: int
                name:
                    description: Channel name, may not contain /.
                    type: str
                rules:
                    description: Alert rules involving this eventgroup type.
                    type: str
        resume:
            description: Provide this token as the 'resume' query argument to continue listing results.
            type: str
        total:
            description: Total number of items available.
            type: int
    sample: {
        channels: [
            {
                "allowed_nodes": [],
                "enabled": "true",
                "excluded_nodes": [],
                "id": 2,
                "name": "Heartbeat Self-Test",
                "parameters": {
                    "address": [],
                    "batch": "",
                    "batch_period": "",
                    "custom_template": "",
                    "send_as": "",
                    "smtp_host": "",
                    "smtp_password": "",
                    "smtp_port": "",
                    "smtp_security": "",
                    "smtp_use_auth": "",
                    "smtp_username": "",
                    "subject": ""
                },
                "rules": ["Heatrbeat"],
                "system": "true",
                "type": "heartbreak"
            }
        ],
        "resume": null,
        "total": 1
    }
alert_rules:
    description: The alert rules details.
    type: list
    returned: When C(alert_rules) is in a given I(gather_subset).
    contains:
        alert_conditions:
            description: Specifies under what conditions and over which channel an alert should be sent.
            type: list
            contains:
                categories:
                    description: Event Group categories to be alerted.
                    type: list
                channels:
                    description: Channels for alert.
                    type: list
                condition:
                    description: Trigger condition for alert.
                    type: str
                eventgroup_ids:
                    description: Event Group IDs to be alerted.
                    type: list
                exclude_eventgroup_ids:
                    description: Event Group categories to be excluded from alerts.
                    type: list
                id:
                    description: Unique identifier.
                    type: int
                interval:
                    description: Required with ONGOING condition only, period
                                 in seconds between alerts of ongoing conditions.
                    type: int
                limit:
                    description: Required with NEW EVENTS condition only,
                                 limits the number of alerts sent as events are added.
                    type: int
                name:
                    description: Unique identifier.
                    type: str
                severities:
                    description: Severities to be alerted.
                    type: list
                transient:
                    description: Any eventgroup lasting less than this many
                                 seconds is deemed transient and will not
                                 generate alerts under this condition.
                    type: int
        resume:
            description: Provide this token as the 'resume' query argument to
                         continue listing results.
            type: str
        total:
            description: Total number of items available.
            type: int
    sample: {
        alert_conditions: [
            {
                "categories": [],
                "channels": [],
                "condition": "ONGOING",
                "eventgroup_ids": ["400050004"],
                "exclude_eventgroup_ids": [],
                "id": 1,
                "interval": 0,
                "limit": 0,
                "name": "Heartbeat Self-Test",
                "severities": [],
                "transient": 0
            }
        ],
        "resume": null,
        "total": 1
    }
event_groups:
    description: The event group details.
    type: list
    returned: When C(event_group) is in a given I(gather_subset).
    contains:
        eventgroup_definitions:
            description: Description of an eventgroup that can occur and be detected.
            type: list
            contains:
                category:
                    description: ID of eventgroup category.
                    type: list
                channels:
                    description: Channels by which this eventgroup type can be alerted.
                    type: list
                description:
                    description: Human readable description, may contain value placeholders.
                    type: str
                id:
                    description: Unique identifier.
                    type: int
                name:
                    description: Name for eventgroup.
                    type: str
                no_ignore:
                    description: True if event should not be ignored.
                    type: bool
                node:
                    description: True if this eventgroup type is node specific,
                                 false cluster wide.
                    type: bool
                rules:
                    description: Alert rules involving this eventgroup type.
                    type: list
                suppressed:
                    description: True if alerting is suppressed for this
                                 eventgroup type.
                    type: bool
        resume:
            description: Provide this token as the 'resume' query argument
                         to continue listing results.
            type: str
        total:
            description: Total number of items available.
            type: int
    sample: {
        eventgroup_definitions: [
            {
                "category": "400000000",
                "channels": [],
                "description": "ONGOING",
                "id": 1,
                "name": "Heartbeat Self-Test",
                "no_ignore": true,
                "node": true,
                "rules": [],
                "suppressed": false
            }
        ],
        "resume": null,
        "total": 1
    }
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell.shared_library.protocol \
    import Protocol
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell.shared_library.synciq \
    import SyncIQ
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell.shared_library.cluster \
    import Cluster
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell.shared_library.certificate \
    import Certificate
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell.shared_library.auth \
    import Auth
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell.shared_library.support_assist \
    import SupportAssist
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell.shared_library.events \
    import Events
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import utils
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell.shared_library.namespace \
    import Namespace
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell.shared_library.quota \
    import Quota
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell.shared_library.snapshot \
    import Snapshot


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
                                    supports_check_mode=True,
                                    mutually_exclusive=mutually_exclusive_args
                                    )

        PREREQS_VALIDATE = utils.validate_module_pre_reqs(self.module.params)
        if PREREQS_VALIDATE \
                and not PREREQS_VALIDATE["all_packages_found"]:
            self.module.fail_json(
                msg=PREREQS_VALIDATE["error_message"])

        self.api_client = utils.get_powerscale_connection(self.module.params)
        self.isi_sdk = utils.get_powerscale_sdk()
        self.major = int(str(self.isi_sdk)[21])
        self.minor = int(str(self.isi_sdk)[23])
        LOG.info('Got python SDK instance for provisioning on PowerScale ')

        self.cluster_api = self.isi_sdk.ClusterApi(self.api_client)
        self.zone_api = self.isi_sdk.ZonesApi(self.api_client)
        self.auth_api = self.isi_sdk.AuthApi(self.api_client)
        self.protocol_api = self.isi_sdk.ProtocolsApi(self.api_client)
        self.statistics_api = self.isi_sdk.StatisticsApi(self.api_client)
        self.synciq_api = self.isi_sdk.SyncApi(self.api_client)
        self.network_api = self.isi_sdk.NetworkApi(self.api_client)
        self.storagepool_api = self.isi_sdk.StoragepoolApi(self.api_client)
        self.certificate_api = self.isi_sdk.CertificateApi(self.api_client)
        self.smartquota_api = self.isi_sdk.QuotaApi(self.api_client)
        self.namespace_api = self.isi_sdk.NamespaceApi(self.api_client)
        self.quota_api = self.isi_sdk.QuotaApi(self.api_client)
        self.snapshot_api = self.isi_sdk.SnapshotApi(self.api_client)
        if self.major > 9 or (self.major == 9 and self.minor > 4):
            self.support_assist_api = self.isi_sdk.SupportassistApi(self.api_client)
        self.event_api = self.isi_sdk.EventApi(self.api_client)

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
            providers_list = (self.auth_api.get_providers_summary(zone=access_zone)).to_dict()
            LOG.info('Got authentication Providers from PowerScale cluster %s',
                     self.module.params['onefs_host'])
            return providers_list
        except Exception as e:
            error_msg = (
                'Get authentication Providers List for PowerScale'
                ' cluster: {0} failed with'
                ' error: {1}' .format(
                    self.module.params['onefs_host'],
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
            nfs_exports_details = (self.protocol_api.list_nfs_exports(zone=access_zone))\
                .to_dict()
            nfs_exports = nfs_exports_details["exports"]
            filters = self.module.params.get('filters')
            filters_dict = self.get_filters(filters)
            if filters_dict:
                filtered_nfs_exports = filter_dict_list(nfs_exports, filters_dict)
                return filtered_nfs_exports
            return nfs_exports
        except Exception as e:
            error_msg = (
                'Get nfs_exports list for PowerScale cluster: {0} failed with'
                'error: {1}'.format(
                    self.module.params['onefs_host'],
                    utils.determine_error(e)))
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def get_nfs_aliases_list(self, access_zone):
        """Get the list of nfs_aliases of a given PowerScale Storage"""
        try:
            nfs_aliases_details = (self.protocol_api.list_nfs_aliases(zone=access_zone, check=True))\
                .to_dict()
            LOG.info('Got nfs_aliases from PowerScale cluster  %s',
                     self.module.params['onefs_host'])
            return nfs_aliases_details["aliases"]
        except Exception as e:
            error_msg = (
                'Getting list of NFS aliases for PowerScale: {0} failed with'
                ' error: {1}'.format(
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
            network_interfaces_details = (self.network_api.get_network_interfaces()).to_dict()
            return network_interfaces_details['interfaces']
        except Exception as e:
            error_msg = (f"Getting list of network interfaces for PowerScale: "
                         f"{self.module.params['onefs_host']} failed with "
                         f"error: {utils.determine_error(e)}")
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

    def get_zone_settings(self, access_zone):
        """
        Getting the details of NFS zone settings
        :param access_zone: Access zone
        :return: NFS zone settings
        :rtype: dict
        """
        try:
            zone_settings = (self.protocol_api.get_nfs_settings_zone(
                zone=access_zone)).to_dict()
            nfs_zone_settings = zone_settings["settings"]
            nfs_zone_settings["zone"] = access_zone
            return nfs_zone_settings
        except Exception as e:
            error_msg = (f"Getting zone settings for PowerScale:"
                         f" {self.module.params['onefs_host']} failed with "
                         f"error: {utils.determine_error(e)}")
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def get_node_pools(self):
        """Getting list of all the node pools of a given PowerScale Storage"""
        try:
            node_pool_details = (self.storagepool_api.list_storagepool_nodepools()).to_dict()
            node_pools = node_pool_details['nodepools']
            return node_pools
        except Exception as e:
            error_msg = (
                'Getting list of node pools for PowerScale: %s failed with '
                'error: %s' % (
                    self.module.params['onefs_host'],
                    utils.determine_error(e)))
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def get_storagepool_tiers(self):
        """Getting list of all the storage tiers of a given PowerScale Storage"""
        try:
            storagepool_tiers_details = (self.storagepool_api.list_storagepool_tiers()).to_dict()
            storagepool_tiers = storagepool_tiers_details['tiers']
            return storagepool_tiers
        except Exception as e:
            error_msg = (
                'Getting list of storagepool tiers for PowerScale: %s failed with '
                'error: %s' % (
                    self.module.params['onefs_host'],
                    utils.determine_error(e)))
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def get_smb_file_for_each_cluster(self, host_ip):
        """Get the list of smb open files given PowerScale Storage"""
        try:
            params = self.module.params.copy()
            params["onefs_host"] = host_ip
            api_client = utils.get_powerscale_connection(params)
            api = self.isi_sdk.ProtocolsApi(api_client)
            cluster_response = api.get_smb_openfiles().to_dict()
            openfiles = cluster_response.get("openfiles", [])
            resume = cluster_response.get("resume")
            while resume:
                cluster_response = api.get_smb_openfiles(resume=resume).to_dict()
                openfiles.extend(cluster_response.get("openfiles", []))
                resume = cluster_response.get("resume")
            for file_dict in openfiles:
                file_dict["node"] = host_ip
            return openfiles
        except Exception as e:
            error_msg = (
                'Getting list of smb open files for PowerScale: {0} failed with'
                ' error: {1}'.format(
                    host_ip,
                    utils.determine_error(e)))
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def get_smb_files(self):
        """Get the list of smb open files given PowerScale Storage"""
        try:
            api_response = self.cluster_api.get_cluster_external_ips()
            smb_files_list = []
            for each_ip in api_response:
                smb_file = self.get_smb_file_for_each_cluster(each_ip)
                smb_files_list.extend(smb_file)
            filtered_smb_files_list = []
            filters = self.module.params.get('filters')
            filters_dict = self.get_filters(filters)
            if filters_dict:
                filtered_smb_files_list = filter_dict_list(smb_files_list, filters_dict)
                return filtered_smb_files_list
            return smb_files_list
        except Exception as e:
            error_msg = (
                'Getting list of cluster external ips for PowerScale: {0} failed with'
                ' error: {1}'.format(
                    self.module.params['onefs_host'],
                    utils.determine_error(e)))
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def get_ldap_providers(self, scope):
        """Get the list of ldap providers given PowerScale Storage"""
        try:
            ldap_providers_details = (self.auth_api.list_providers_ldap(scope=scope))\
                .to_dict()
            ldap_details = ldap_providers_details['ldap']
            LOG.info('Got ldap providers from PowerScale cluster  %s',
                     self.module.params['onefs_host'])
            return ldap_details
        except Exception as e:
            error_msg = (
                'Getting list of ldap providers for PowerScale: {0} failed with'
                ' error: {1}'.format(
                    self.module.params['onefs_host'],
                    utils.determine_error(e)))
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def get_user_mapping_rules(self, access_zone):
        """Get the list of user mapping rules of a given PowerScale Storage"""
        try:
            user_mapping_rules_list = []
            user_mapping_rules_details = (self.auth_api.get_mapping_users_rules(zone=access_zone)).to_dict()
            for count, rule in enumerate(user_mapping_rules_details['rules']['rules']):
                rule['apply_order'] = count + 1
                user_mapping_rules_list.append(rule)
            return user_mapping_rules_list
        except Exception as e:
            error_msg = (
                'Getting list of user mapping rules for PowerScale: %s failed with '
                'error: %s' % (
                    self.module.params['onefs_host'],
                    utils.determine_error(e)))
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def get_nfs_global_settings(self):
        """Get the NFS global setings of a given PowerScale Storage"""
        try:
            nfs_global_settings_details = self.protocol_api.get_nfs_settings_global().to_dict()
            msg = f"Got NFS global settings from PowerScale cluster {self.module.params['onefs_host']}"
            LOG.info(msg)
            return nfs_global_settings_details['settings']
        except Exception as e:
            error_msg = (
                f"Getting NFS global settings for PowerScale: {self.module.params['onefs_host']}" +
                f" failed with error: {utils.determine_error(e)}")
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def get_smartquota_list(self):
        """Get the smartquota list of a given PowerScale Storage"""
        try:
            smartquota = []
            smartquota_details = self.smartquota_api.list_quota_quotas().to_dict()
            smartquota.extend(smartquota_details['quotas'])
            resume = smartquota_details['resume']
            while resume:
                smartquota_details = self.smartquota_api.list_quota_quotas(resume=resume).to_dict()
                smartquota.extend(smartquota_details['quotas'])
                resume = smartquota_details['resume']
            msg = f"Got smartquota list from PowerScale cluster {self.module.params['onefs_host']}"
            LOG.info(msg)
            filters = self.module.params.get('filters')
            filters_dict = self.get_filters(filters)
            if filters_dict:
                filtered_smartquota = filter_dict_list(smartquota, filters_dict)
                return filtered_smartquota
            return smartquota
        except Exception as e:
            error_msg = (
                f"Getting smartquota list for PowerScale: {self.module.params['onefs_host']}" +
                f" failed with error: {utils.determine_error(e)}")
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def get_writable_snapshots(self):
        writable_snapshots = Snapshot(self.snapshot_api, self.module).list_writable_snapshots()
        filtered_writable_snapshots = []
        filters = self.module.params.get('filters')
        filters_dict = self.get_filters(filters)
        if filters_dict:
            filtered_writable_snapshots = filter_dict_list(writable_snapshots, filters_dict)
            return filtered_writable_snapshots
        return writable_snapshots

    def get_metadata(self, effective_path):
        return Namespace(self.namespace_api, self.module).get_filesystem(effective_path)

    def get_acl(self, effective_path):
        return Namespace(self.namespace_api, self.module).get_acl(effective_path)

    def get_quota(self, effective_path):
        return Quota(self.quota_api, self.module).get_quota(effective_path)

    def get_snapshots(self, effective_path):
        return Snapshot(self.snapshot_api, self.module).get_filesystem_snapshots(effective_path)

    def list_filesystems(self, path):
        """List all filesystems from the given directory path."""
        namespace = Namespace(self.namespace_api, self.module)
        filesystem_paths = namespace.list_all_filesystem_from_directory(path)
        return filesystem_paths.get("children", []) if filesystem_paths else []

    def fetch_data(self, effective_path, data_fetchers, required_params):
        """Fetch required data based on query parameters."""
        fetched_data = {}
        for param, fetcher in data_fetchers.items():
            if param in required_params:
                data = fetcher(effective_path)
                if param == "snapshot":
                    fetched_data["snapshots"] = data
                else:
                    fetched_data.update(data)
        return fetched_data

    def get_required_params(self, query_params=None):
        """Extract required parameters from query parameters."""
        if query_params:
            if "path" in query_params:
                del query_params["path"]
            return {k: v for k, v in query_params.items() if v is True}

    def get_filesystem_list(self, path, query_params=None):
        """Get the filesystem list of a given PowerScale Storage."""
        try:
            filesystem_list = [{"name": fs.get("name")} for fs in self.list_filesystems(path)]
            required_params = None
            if not filesystem_list:
                return filesystem_list

            filters = self.module.params.get('filters')
            filters_dict = self.get_filters(filters)
            if filters_dict:
                filesystem_list = filter_dict_list(filesystem_list, filters_dict)

            data_fetchers = {
                'metadata': self.get_metadata,
                'acl': self.get_acl,
                'quota': self.get_quota,
                'snapshot': self.get_snapshots
            }
            if query_params and "filesystem" in query_params:
                filesystem_query_params = query_params.get('filesystem')
                required_params = self.get_required_params(query_params=filesystem_query_params)

            if required_params:
                for each_filesystem in filesystem_list:
                    effective_path = f"{path}/{each_filesystem['name']}"
                    fetched_data = self.fetch_data(effective_path, data_fetchers, required_params)
                    each_filesystem.update(fetched_data)

            return filesystem_list
        except Exception as e:
            error_msg = (
                f"Getting filesystem for PowerScale: {self.module.params['onefs_host']}" +
                f" failed with error: {utils.determine_error(e)}"
            )
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def get_filters(self, filters=None):
        """Get the filters to be applied"""
        filters_dict = {}
        # TO DO run below line only if filters is not None
        if filters is None:
            return filters_dict
        filters_items = [item for item in filters
                         if 'filter_key' in item and 'filter_operator' in item
                         and 'filter_value' in item]
        if not filters_items:
            self.module.fail_json(msg='filter_key, filter_operator, filter_value are expected.')
        for item in filters_items:
            f_key = item.get("filter_key")
            f_val = item.get("filter_value")
            f_op = item.get("filter_operator")
            if f_op != 'equal':
                error_msg = "The filter operator is not supported -- only 'equal' is supported."
                self.module.fail_json(msg=error_msg)
            filters_dict[f_key] = f_val
        return filters_dict

    def get_support_assist_settings(self):
        """Get support assist settings based on the version."""
        if self.major > 9 or (self.major == 9 and self.minor > 4):
            return SupportAssist(self.support_assist_api, self.module).get_support_assist_settings()
        else:
            return {}

    def perform_module_operation(self):
        """Perform different actions on Gatherfacts based on user parameter chosen in playbook"""
        include_all_access_zones = self.module.params['include_all_access_zones']
        access_zone = self.module.params['access_zone']
        subset = self.module.params['gather_subset']
        scope = self.module.params['scope']
        path = "ifs"
        query_params = self.module.params.get("query_parameters")
        if query_params and "filesystem" in query_params:
            filesystem = query_params.get("filesystem")
            if filesystem and "path" in filesystem:
                path = filesystem.get("path")
        if not subset:
            self.module.fail_json(msg="Please specify gather_subset")

        # Initialize result dictionary with default values
        result = {
            'Attributes': [],
            'AccessZones': [],
            'Nodes': [],
            'Providers': [],
            'Users': [],
            'Groups': [],
            'SmbShares': [],
            'Clients': [],
            'NfsExports': [],
            'NfsAliases': [],
            'SynciqReports': [],
            'SynciqTargetReports': [],
            'SynciqPolicies': [],
            'SynciqTargetClusterCertificate': [],
            'SynciqPerformanceRules': [],
            'NetworkGroupnets': [],
            'NetworkPools': [],
            'NetworkRules': [],
            'NetworkInterfaces': [],
            'NetworkSubnets': [],
            'NodePools': [],
            'StoragePoolTiers': [],
            'SmbOpenFiles': [],
            'UserMappingRules': [],
            'LdapProviders': [],
            'NfsZoneSettings': {},
            'NfsDefaultSettings': {},
            'NfsGlobalSettings': {},
            'SynciqGlobalSettings': {},
            's3Buckets': {},
            'SmbGlobalSettings': {},
            'NTPServers': {},
            'EmailSettings': {},
            'ClusterIdentity': {},
            'ClusterOwner': {},
            'SnmpSettings': {},
            'ServerCertificate': [],
            'roles': {},
            'support_assist_settings': {},
            'alert_settings': {},
            'alert_rules': [],
            'alert_categories': [],
            'alert_channels': [],
            'event_groups': [],
            'smart_quota' : [],
            'file_system' : []
        }

        # Call the appropriate method based on the subset
        subset_mapping = {
            'attributes': self.get_attributes_list,
            'access_zones': self.get_access_zones_list,
            'nodes': self.get_nodes_list,
            'providers': lambda: self.get_providers_list(access_zone),
            'users': lambda: Auth(self.auth_api, self.module).get_auth_users(access_zone),
            'groups': lambda: self.get_groups_list(access_zone),
            'smb_shares': lambda: self.get_smb_shares_list(access_zone),
            'clients': self.get_clients_list,
            'nfs_exports': lambda: self.get_nfs_exports_list(access_zone),
            'nfs_aliases': lambda: self.get_nfs_aliases_list(access_zone),
            'synciq_reports': self.get_synciq_reports,
            'synciq_target_reports': self.get_synciq_target_reports,
            'synciq_policies': self.get_syniq_policies_list,
            'synciq_target_cluster_certificates': self.get_synciq_target_cluster_certificates_list,
            'synciq_performance_rules': self.get_synciq_performance_rules,
            'network_groupnets': self.get_network_groupnets,
            'network_pools': lambda: self.get_network_pools(access_zone, include_all_access_zones),
            'network_rules': self.get_network_rules,
            'network_interfaces': self.get_network_interfaces,
            'network_subnets': self.get_network_subnets,
            'node_pools': self.get_node_pools,
            'storagepool_tiers': self.get_storagepool_tiers,
            'smb_files': self.get_smb_files,
            'user_mapping_rules': lambda: self.get_user_mapping_rules(access_zone),
            'ldap': lambda: self.get_ldap_providers(scope),
            'nfs_zone_settings': lambda: self.get_zone_settings(access_zone),
            'nfs_default_settings': lambda: Protocol(self.protocol_api, self.module).get_nfs_default_settings(access_zone),
            'nfs_global_settings': self.get_nfs_global_settings,
            'synciq_global_settings': lambda: SyncIQ(self.synciq_api, self.module).get_synciq_global_settings(),
            's3_buckets': lambda: Protocol(self.protocol_api, self.module).get_s3_bucket_list(),
            'smb_global_settings': lambda: Protocol(self.protocol_api, self.module).get_smb_global_settings(),
            'ntp_servers': lambda: Protocol(self.protocol_api, self.module).get_ntp_server_list(),
            'email_settings': lambda: Cluster(self.cluster_api, self.module).get_email_settings(),
            'cluster_identity': lambda: Cluster(self.cluster_api, self.module).get_cluster_identity_details(),
            'cluster_owner': lambda: Cluster(self.cluster_api, self.module).get_cluster_owner_details(),
            'snmp_settings': lambda: Protocol(self.protocol_api, self.module).get_snmp_settings(),
            'server_certificate': lambda: Certificate(self.certificate_api, self.module).get_server_certificate_with_default(),
            'roles': lambda: Auth(self.auth_api, self.module).get_auth_roles(access_zone),
            'support_assist_settings': self.get_support_assist_settings,
            'alert_settings': lambda: Events(self.event_api, self.module).get_event_maintenance(),
            'alert_rules': lambda: Events(self.event_api, self.module).get_alert_rules(),
            'alert_categories': lambda: Events(self.event_api, self.module).get_alert_categories(),
            'alert_channels': lambda: Events(self.event_api, self.module).get_event_channels(),
            'event_group': lambda: Events(self.event_api, self.module).get_event_groups(),
            'smartquota': self.get_smartquota_list,
            'filesystem': lambda: self.get_filesystem_list(path, query_params),
            'writable_snapshots': self.get_writable_snapshots
        }

        key_mapping = {
            'attributes': 'Attributes',
            'access_zones': 'AccessZones',
            'nodes': 'Nodes',
            'providers': 'Providers',
            'users': 'Users',
            'groups': 'Groups',
            'smb_shares': 'SmbShares',
            'clients': 'Clients',
            'nfs_exports': 'NfsExports',
            'nfs_aliases': 'NfsAliases',
            'synciq_reports': 'SynciqReports',
            'synciq_target_reports': 'SynciqTargetReports',
            'synciq_policies': 'SynciqPolicies',
            'synciq_performance_rules': 'SynciqPerformanceRules',
            'network_groupnets': 'NetworkGroupnets',
            'network_pools': 'NetworkPools',
            'network_rules': 'NetworkRules',
            'network_interfaces': 'NetworkInterfaces',
            'network_subnets': 'NetworkSubnets',
            'node_pools': 'NodePools',
            'storagepool_tiers': 'StoragePoolTiers',
            'smb_files': 'SmbOpenFiles',
            'user_mapping_rules': 'UserMappingRules',
            'ldap': 'LdapProviders',
            'nfs_zone_settings': 'NfsZoneSettings',
            'nfs_default_settings': 'NfsDefaultSettings',
            'nfs_global_settings': 'NfsGlobalSettings',
            'synciq_global_settings': 'SynciqGlobalSettings',
            'smb_global_settings': 'SmbGlobalSettings',
            'ntp_servers': 'NtpServers',
            'email_settings': 'EmailSettings',
            'cluster_identity': 'ClusterIdentity',
            'cluster_owner': 'ClusterOwner',
            'snmp_settings': 'SnmpSettings',
            'server_certificate': 'ServerCertificate',
            's3_buckets': 's3Buckets',
            'synciq_target_cluster_certificates': 'SynciqTargetClusterCertificate',
            'event_group': 'event_groups',
            'smartquota': 'smart_quota',
            'filesystem': 'file_system',
            'writable_snapshots': 'writable_snapshots'
        }

        # Map the subset to the appropriate Key
        subset_list = ['attributes', 'access_zones', 'nodes', 'providers', 'groups', 'smb_shares', 'clients',
                       'nfs_exports', 'nfs_aliases', 'synciq_reports', 'synciq_target_reports', 'synciq_policies',
                       'synciq_target_cluster_certificates', 'synciq_performance_rules', 'network_groupnets',
                       'network_pools', 'network_rules', 'network_interfaces', 'network_subnets', 'node_pools',
                       'storagepool_tiers', 'smb_files', 'user_mapping_rules', 'ldap', 'nfs_zone_settings',
                       'nfs_default_settings', 'nfs_global_settings', 'synciq_global_settings', 's3_buckets',
                       'smb_global_settings', 'ntp_servers', 'email_settings', 'cluster_identity', 'cluster_owner',
                       'snmp_settings', 'server_certificate', 'event_group', 'smartquota', 'filesystem',
                       'writable_snapshots', 'users']
        for key in subset:
            if key not in subset_list:
                result[key] = subset_mapping[key]()
            else:
                result[key_mapping[key]] = subset_mapping[key]()

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
        scope=dict(required=False, type='str',
                   choices=['effective', 'user', 'default'],
                   default='effective'),
        gather_subset=dict(
            type='list', required=True, elements='str',
            choices=['attributes', 'access_zones', 'nodes',
                     'providers', 'users', 'groups',
                     'smb_shares', 'nfs_exports', 'nfs_aliases',
                     'clients', 'synciq_reports', 'synciq_target_reports',
                     'synciq_policies', 'synciq_target_cluster_certificates',
                     'synciq_performance_rules', 'network_groupnets',
                     'network_pools', 'network_rules', 'network_interfaces',
                     'network_subnets', 'node_pools', 'storagepool_tiers',
                     'smb_files', 'user_mapping_rules', 'ldap',
                     'nfs_zone_settings', 'nfs_default_settings',
                     'nfs_global_settings', 'synciq_global_settings',
                     's3_buckets', 'smb_global_settings', 'ntp_servers',
                     'email_settings', 'cluster_identity', 'cluster_owner',
                     'snmp_settings', 'server_certificate', 'roles',
                     'support_assist_settings', 'alert_settings', 'alert_rules',
                     'alert_channels', 'alert_categories', 'event_group',
                     'filesystem', 'smartquota', 'writable_snapshots']),
        filters=dict(type='list',
                     required=False,
                     elements='dict',
                     options=dict(
                         filter_key=dict(type='str', required=True, no_log=False),
                         filter_operator=dict(type='str',
                                              required=True,
                                              choices=['equal']),
                         filter_value=dict(type='raw', required=True))),
        query_parameters=dict(type='dict')
    )


def filter_dict_list(dict_list, filters):
    """
    Filters a list of dictionaries based on a list of filters.
    :param dict_list: List of dictionaries to filter
    :param filters: List of filters, where each filter is a tuple (key, value)
    :return: Filtered list of dictionaries
    """
    try:
        return [
            d for d in dict_list
            if all((isinstance(d[key], (list, dict)) and value in d.get(key))
                   or d.get(key) == value for key, value in filters.items())]
    except KeyError:
        return dict_list


def main():
    """Create PowerScale GatherFacts object and perform action on it
       based on user input from playbook"""
    obj = Info()
    obj.perform_module_operation()


if __name__ == '__main__':
    main()
