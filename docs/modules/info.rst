.. _info_module:


info -- Gathering information about PowerScale Storage
======================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Gathering information about Specified PowerScale Storage entities, includes attributes, access zones, nodes, authentication providers for all access zones, users and groups for an access zone.

Get list of smb_shares, nfs_exports, nfs_aliases, active clients, SyncIQ reports, SyncIQ target reports, SyncIQ target cluster certificates, SyncIQ policies, SyncIQ performance rules.

Get list of network groupnets, network pools for all access zones or a specific access zone, network rules, network subnets, network interfaces, node pools, storage pool tiers, smb open files.

Get list of user mapping rules, ldap providers of the PowerScale cluster.

Get NFS zone settings details of the PowerScale cluster.

Get NFS default settings details of the PowerScale cluster.

Get NFS global settings details of the PowerScale cluster.

Get SyncIQ global settings details of the PowerScale cluster.



Requirements
------------
The below requirements are needed on the host that executes this module.

- A Dell PowerScale Storage system.
- Ansible-core 2.14 or later.
- Python 3.9, 3.10 or 3.11.



Parameters
----------

  include_all_access_zones (optional, bool, None)
    Specifies if requested component details need to be fetched from all access zones.

    It is mutually exclusive with *access_zone*.


  access_zone (optional, str, System)
    The access zone. If no Access Zone is specified, the 'System' access zone would be taken by default.


  scope (optional, str, effective)
    The scope of ldap. If no scope is specified, the ``effective`` scope would be taken by default.

    If specified as ``effective`` or not specified, all fields are returned.

    If specified as ``user``, only fields with non-default values are shown.

    If specified as ``default``, the original values are returned.


  gather_subset (True, list, None)
    List of string variables to specify the PowerScale Storage System entities for which information is required.

    List of all PowerScale Storage System entities supported by the module.

    Attributes - ``attributes``.

    Access zones - ``access_zones``.

    Nodes - ``nodes``.

    Providers - ``providers``.

    Users - ``users``.

    Groups - ``groups``.

    Smb shares - ``smb_shares``.

    Nfs exports - ``nfs_exports``.

    Nfs aliases - ``nfs_aliases``.

    Clients - ``clients``.

    Synciq reports - ``synciq_reports``.

    Synciq target reports - ``synciq_target_reports``.

    Synciq policies - ``synciq_policies``.

    Synciq target cluster certificates - ``synciq_target_cluster_certificates``.

    Synciq performance rules - ``synciq_performance_rules``.

    Network groupnets - ``network_groupnets``.

    Network pools - ``network_pools``.

    Network rules - ``network_rules``.

    Network interfaces - ``network_interfaces``.

    Network subnets - ``network_subnets``.

    Node pools - ``node_pools``.

    Storagepool tiers - ``storagepool_tiers``.

    SMB files - ``smb_files``.

    User mapping rules - ``user_mapping_rules``.

    LDAPs - ``ldap``.

    NFS zone settings - ``nfs_zone_settings``.

    NFS default settings - ``nfs_default_settings``.

    SyncIQ global settings - ``synciq_global_settings``.

    S3 buckets - ``s3_buckets``

    The list of *attributes*, *access_zones* and *nodes* is for the entire PowerScale cluster.

    The list of providers for the entire PowerScale cluster.

    The list of users and groups is specific to the specified access zone.

    The list of syncIQ reports and syncIQ target reports for the entire PowerScale cluster.

    The list of syncIQ policies, syncIQ target cluster certificates and syncIQ performance rules for the entire PowerScale cluster.

    The list of network pools is specific to the specified access zone or for all access zones.

    The list of network groupnets, network subnets, network rules and network interfaces is for the entire PowerScale cluster.

    The list of smb open files for the entire PowerScale cluster.

    The list of user mapping rules of PowerScale cluster.

    The list of ldap providers of PowerScale cluster.

    The list of S3 bucket for the entire PowerScale cluster.


  onefs_host (True, str, None)
    IP address or FQDN of the PowerScale cluster.


  port_no (False, str, 8080)
    Port number of the PowerScale cluster.It defaults to 8080 if not specified.


  verify_ssl (True, bool, None)
    boolean variable to specify whether to validate SSL certificate or not.

    ``true`` - indicates that the SSL certificate should be verified.

    ``false`` - indicates that the SSL certificate should not be verified.


  api_user (True, str, None)
    username of the PowerScale cluster.


  api_password (True, str, None)
    the password of the PowerScale cluster.





Notes
-----

.. note::
   - The parameters *access_zone* and *include_all_access_zones* are mutually exclusive.
   - Listing of SyncIQ target cluster certificates is not supported by isi_sdk_8_1_1 version.
   - The *check_mode* is supported.
   - The modules present in this collection named as 'dellemc.powerscale' are built to support the Dell PowerScale storage platform.




Examples
--------

.. code-block:: yaml+jinja

    
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



Return Values
-------------

changed (always, bool, false)
  Shows Whether or not the resource has changed.


AccessZones (When C(access_zones) is in a given I(gather_subset), dict, [{'zones': [{'alternate_system_provider': 'lsa-file-provider:MinimumRequired', 'auth_providers': ['lsa-local-provider:sampe-az'], 'cache_entry_expiry': 14400, 'groupnet': 'groupnet0', 'home_directory_umask': 63, 'id': 'Bhavneet-SS', 'ifs_restricted': [], 'name': 'Bhavneet-SS', 'negative_cache_entry_expiry': 60, 'netbios_name': '', 'path': '/ifs', 'skeleton_directory': '/usr/share/skel', 'system': False, 'system_provider': 'lsa-file-provider:System', 'user_mapping_rules': [], 'zone_id': 18}]}])
  Access zones of  the PowerScale storage system.


  zones (, list, )
    List of different access zone.



Attributes (When C(attributes) is in a given I(gather_subset), dict, {'Cluster_Version': {'errors': [], 'nodes': [{'build': 'B_9_5_0_005(RELEASE)', 'id': 1, 'release': 'x.x.0.0', 'revision': '124', 'type': 'Isilon OneFS', 'version': 'Isilon OneFS x.x.0.0'}], 'total': 3}, 'Config': {'description': '', 'devices': [{'devid': 1, 'guid': '000e1e84be90ac5e7d62df0dfc180d3d0ccb', 'is_up': True, 'lnn': 1}], 'encoding': 'utf-8', 'guid': '000e1e84be902f5f7d62ef254853667f0792', 'has_quorum': True, 'is_compliance': False, 'is_virtual': False, 'is_vonefs': False, 'join_mode': 'Manual', 'local_devid': 1, 'local_lnn': 1, 'local_serial': 'xxxx-xxxx-xxxxx', 'name': 'LAB-IsilonS-xxxxx', 'onefs_version': {'build': 'B_x_x_0_005(RELEASE)', 'copyright': 'Copyright (c) 2001-2022 Dell Inc. All Rights Reserved.', 'reldate': 'xxxx', 'release': 'x.x.0.0', 'revision': '649926064822288389', 'type': 'Isilon OneFS', 'version': 'Isilon OneFS x.x.0.0'}, 'timezone': {'abbreviation': 'GMT', 'custom': '', 'name': 'Greenwich Mean Time', 'path': 'GMT'}, 'upgrade_type': None}, 'Contact_Info': {}, 'External_IP': {}, 'Logon_msg': {}})
  Different Attributes of the PowerScale storage system.


  Cluster_Version (, dict, )
    Cluster version of the PowerScale storage system.


  Config (, dict, )
    Config details of the PowerScale storage system.


  Contact_Info (, dict, )
    Contact details of the PowerScale storage system.


  External_IP (, dict, )
    External IPs of the PowerScale storage system.


  Logon_msg (, dict, )
    Log-on messages of the PowerScale storage system.



Clients (When C(clients) is in a given I(gather_subset), list, [{'local_address': 'x.x.x.x', 'local_name': 'x.x.x.x', 'node': 1, 'protocol': 'nfs4', 'remote_address': 'x.x.x.x', 'remote_name': 'x.x.x.x'}])
  List all clients present in the PowerScale system.


  local_address (, str, )
    Local address of the client.


  local_name (, str, )
    Local name of the client.


  node (, int, )
    Node on which client exists.


  protocol (, str, )
    Protocol that client uses.


  remote_address (, str, )
    Remote address of the client.


  remote_name (, str, )
    Remote address of the client.



Groups (When C(groups) is in a given I(gather_subset), list, [{'groups': [{'dn': 'CN=Administrators,CN=Builtin,DC=PIE-ISILONS-xxx', 'dns_domain': None, 'domain': 'BUILTIN', 'generated_gid': False, 'gid': {'id': 'GID:1544', 'name': None, 'type': None}, 'id': 'Administrators', 'member_of': None, 'name': 'Administrators', 'object_history': [], 'provider': 'lsa-local-provider:System', 'sam_account_name': 'Administrators', 'sid': {'id': 'SID:S-1-5-32-544', 'name': None, 'type': None}, 'type': 'group'}]}])
  List of all groups.


  groups (, list, )
    List of groups details.


    id (, str, )
      ID of the groups.


    name (, str, )
      Name of the groups.


    provider (, str, )
      The provider of the groups.




LdapProviders (When C(ldap) is in a given I(gather_subset), list, [{'linked_access_zones': ['System'], 'base_dn': 'dc=sample,dc=ldap,dc=domain,dc=com', 'bind_dn': 'cn=administrator,dc=sample,dc=ldap,dc=domain,dc=com', 'groupnet': 'groupnet', 'name': 'sample-ldap', 'server_uris': 'ldap://xx.xx.xx.xx', 'status': 'online'}])
  Provide details of LDAP providers.


  linked_access_zones (, list, )
    List of access zones linked to the authentication provider.


  base_dn (, str, )
    Specifies the root of the tree in which to search identities.


  bind_dn (, str, )
    Specifies the distinguished name for binding to the LDAP server.


  groupnet (, str, )
    Groupnet identifier.


  name (, str, )
    Specifies the name of the LDAP provider.


  server_uris (, str, )
    Specifies the server URIs.


  status (, str, )
    Specifies the status of the provider.



NetworkGroupnets (When C(network_groupnets) is in a given I(gather_subset), list, [{'id': 'sample', 'name': 'groupnet0'}])
  List of Network Groupnets.


  id (, str, )
    ID of the groupnet.


  name (, str, )
    Name of the groupnet.



NetworkInterfaces (When C(network_interfaces) is in a given I(gather_subset), list, [{'id': '110gig1', 'lnn': 1, 'name': '10gig1'}])
  List of Network interfaces.


  id (, str, )
    ID of the interface.


  lnn (, int, )
    Interface's lnn.


  name (, str, )
    Name of the interface.



NetworkPools (When C(network_pools) is in a given I(gather_subset), list, [{'id': 'groupnet0.subnet0.pool0', 'name': 'pool0'}])
  List of Network Pools.


  id (, str, )
    ID of the Network Pool.


  name (, str, )
    Name of the Network Pool.



NetworkRules (When C(network_rules) is in a given I(gather_subset), list, [{'id': 'groupnet0.subnet0.pool0.test_rule', 'name': 'test_rule'}])
  List of the Network rules.


  id (, str, )
    Name of the Network Pool.


  name (, str, )
    Name of the Network Pool.



NetworkSubnets (When C(network_subnets) is in a given I(gather_subset), list, [{'id': 'groupnet0.subnet0.pool0.test_rule', 'name': 'test_rule'}])
  List of the Network subnets.


  id (, str, )
    Name of the Network Pool.


  name (, str, )
    Name of the Network Pool.



NfsAliases (When C(nfs_aliases) is in a given I(gather_subset), list, [{'health': 'path not found', 'id': '/ifs_#$%^&*()', 'name': '/ifs_#$%^&*()', 'path': '/ifs/sample_alias_1', 'zone': 'System'}])
  List of NFS Aliases.


  health (, str, )
    Specifies the health of the NFS alias.


  id (, str, )
    ID of the NFS alias.


  name (, str, )
    Name of the NFS alias.


  path (, str, )
    Path of the NFS alias.


  zone (, str, )
    Access zone of the NFS alias.



NfsExports (When C(nfs_exports) is in a given I(gather_subset), list, [{'id': 205, 'paths': ['/ifs/data/sample/fs1']}])
  List of NFS exports.


  id (, str, )
    ID of the NFS exports.


  path (, list, )
    Path of the NFS exports.



NfsZoneSettings (When C(nfs_zone_settings) is in a given I(gather_subset), dict, {'nfsv4_allow_numeric_ids': True, 'nfsv4_domain': 'sample.com', 'nfsv4_no_domain': True, 'nfsv4_no_domain_uids': True, 'nfsv4_no_names': True, 'nfsv4_replace_domain': True, 'zone': 'System'})
  Details of NFS zone settings.


  nfsv4_allow_numeric_ids (, bool, )
    If ``true``, sends owners and groups as UIDs and GIDs when look up fails or if the *nfsv4_no_names* property is set to 1.


  nfsv4_domain (, str, )
    Specifies the domain through which users and groups are associated.


  nfsv4_no_domain (, bool, )
    If ``true``, sends owners and groups without a domain name.


  nfsv4_no_domain_uids (, bool, )
    If ``true``, sends UIDs and GIDs without a domain name.


  nfsv4_no_names (, bool, )
    If ``true``, sends owners and groups as UIDs and GIDs.


  nfsv4_replace_domain (, bool, )
    If ``true``, replaces the owner or group domain with an NFS domain name.


  zone (, str, )
    Specifies the access zone in which the NFS zone settings apply.



NfsGlobalSettings (When C(nfs_global_settings) is in a given I(gather_subset), dict, {'nfsv3_enabled': False, 'nfsv3_rdma_enabled': True, 'nfsv40_enabled': True, 'nfsv41_enabled': True, 'nfsv42_enabled': False, 'nfsv4_enabled': True, 'rpc_maxthreads': 20, 'rpc_minthreads': 17, 'rquota_enabled': True, 'service': True})
  Details of NFS global settings.


  nfsv3_enabled (, bool, )
    Whether NFSv3 protocol is enabled/disabled.


  nfsv3_rdma_enabled (, bool, )
    Whether rdma is enabled for NFSv3 protocol.


  nfsv40_enabled (, bool, )
    Whether version 0 of NFSv4 protocol is enabled/disabled.


  nfsv41_enabled (, bool, )
    Whether version 1 of NFSv4 protocol is enabled/disabled.


  nfsv42_enabled (, bool, )
    Whether version 2 of NFSv4 protocol is enabled/disabled.


  nfsv4_enabled (, bool, )
    Whether NFSv4 protocol is enabled/disabled.


  rpc_maxthreads (, int, )
    Specifies the maximum number of threads in the nfsd thread pool.


  rpc_minhreads (, int, )
    Specifies the minimum number of threads in the nfsd thread pool.


  rquota_enabled (, bool, )
    Whether the rquota protocol is enabled/disabled.


  service (, bool, )
    Whether the NFS service is enabled/disabled.



NodePools (When C(node_pools) is in a given I(gather_subset), list, [{'can_disable_l3': True, 'can_enable_l3': True, 'health_flags': ['missing_drives'], 'id': 1, 'l3': True, 'l3_status': 'l3', 'lnns': [1], 'manual': False, 'name': 's210_6.9tb_1.6tb-ssd_64gb', 'node_type_ids': [1], 'protection_policy': '+2d:1n', 'tier': None, 'transfer_limit_pct': 90, 'transfer_limit_state': 'default', 'usage': {}}])
  List of the Node pools.


  id (, str, )
    ID of the node pool.


  lnns (, list, )
    Node pool's lnns.


  name (, str, )
    Name of the node pool.


  protection_policy (, str, )
    Protection policy of the node pool.


  usage (, dict, )
    Usage of the node pool.



Nodes (When C(nodes) is in a given I(gather_subset), dict, {'nodes': [], 'total': 1})
  Contain the list of Nodes in the PowerScale cluster.


  nodes (, list, )
    Specifies the deatils of the node.


  total (, int, )
    Total number of nodes.



Providers (When C(providers) is in a given I(gather_subset), list, {'provider_instances': [{'active_server': None, 'connections': [], 'groupnet': None, 'id': 'lsa-local-provider:System', 'name': 'System', 'status': 'active', 'type': 'local', 'zone_name': 'System'}]})
  Contains different type of providers in the PowerScale system.


  provider_instances (, list, )
    List of providers.


    active_server (, str, )
      Active server of the provider.


    connections (, str, )
      Different connections of provider.


    groupnet (, str, )
      Groupnet of the provider.


    id (, str, )
      ID of the provider.


    name (, str, )
      Name of the provider.


    status (, str, )
      Status of the provider.


    type (, str, )
      Type of the provider


    zone_name (, str, )
      Access zone of the provider.




SmbOpenFiles (When C(smb_files) is in a given I(gather_subset), list, [{'file': 'C:\\ifs', 'id': 1370, 'locks': 0, 'permissions': ['read'], 'user': 'admin'}])
  List of SMB open files.


  file (, str, )
    Path of file within /ifs.


  id (, int, )
    The ID of the SMB open file.


  locks (, int, )
    The number of locks user holds on file.


  permission (, list, )
    The user's permissions on file.


  user (, str, )
    User holding file open.



SmbShares (When C(smb_shares) is in a given I(gather_subset), list, [{'id': 'Atest', 'name': 'Atest'}])
  List of the SMB Shares.


  id (, str, )
    ID of the SMB Share.


  name (, str, )
    Name of the SMB Share.



StoragePoolTiers (When C(storagepool_tiers) is in a given I(gather_subset), list, [{'children': [], 'id': 984, 'lnns': [], 'name': 'Ansible_Tier_1', 'usage': {}}])
  List of the storage pool tiers.


  children (, list, )
    Children in the storage pool tiers.


  id (, str, )
    ID of the storage pool tier.


  lnns (, list, )
    Storage pool tier's lnn.


  name (, str, )
    Name of the storage pool tier.


  usage (, list, )
    Usage of the storage pool tiers.



SynciqPerformanceRules (When C(synciq_performance_rules) is in a given I(gather_subset), list, [{'enabled': True, 'id': 'fc-0', 'limit': '1files/sec', 'schedule': {}, 'type': 'file_count'}])
  List of SyncIQ performance rules.


  enabled (, bool, )
    Whether SyncIQ performance rule enabled.


  id (, str, )
    ID of the SyncIQ performance rule.


  limit (, str, )
    Limits of the SyncIQ performance rule.


  schedule (, dict, )
    Schedule of the SyncIQ performance rule.


  type (, str, )
    The type of the SyncIQ performance rule.



SynciqPolicies (When C(synciq_policies) is in a given I(gather_subset), list, [{'enabled': True, 'id': '1ee8ad74f6f147894d21e339d57c3d1b', 'name': 'dk2-nginx-10-230-24-249-Five_Minutes', 'schedule': 'when-source-modified', 'source_root_path': '/ifs/data/sample-x.x.x.x-Five_Minutes', 'target_path': '/ifs/data/dk2-nginx-x.x.x.x-Five_Minutes'}])
  List of the SyncIQ policies.


  enabled (, bool, )
    Whether SyncIQ policies enabled.


  id (, str, )
    ID of the SyncIQ policies.


  name (, str, )
    Name of the SyncIQ policies.


  schedule (, str, )
    Schedule of the SyncIQ policies.


  source_root_path (, str, )
    Source path of the SyncIQ policies.


  target_path (, str, )
    Target path of the SyncIQ policies.



SynciqReports (When C(synciq_reports) is in a given I(gather_subset), list, [{'id': '1ee8ad74f6f147894d21e339d57c3d1b', 'name': 'dk2-nginx-10-230-24-249-Five_Minutes'}])
  List of the SyncIQ reports.


  id (, str, )
    ID of the SyncIQ reports.


  name (, str, )
    Name of the SyncIQ reports.



SynciqTargetClusterCertificate (When C(synciq_target_cluster_certificates) is in a given I(gather_subset), list, [{'id': '077f119e54ec2c12c74f011433cd33ac5c', 'name': 'sample'}])
  List of the SyncIQ Target cluster certificates.


  id (, str, )
    ID of the SyncIQ Target cluster certificates.


  name (, str, )
    Name of the SyncIQ Target cluster certificates.



SynciqTargetReports (When C(synciq_target_reports) is in a given I(gather_subset), list, [{'id': 'cicd-repctl-0419-t151741-10-247-100-10-Five_Minutes', 'name': 'cicd-repctl-0419-t1741-10-247-100-10-Five_Minutes'}])
  List of the SyncIQ Target reports.


  id (, str, )
    ID of the SyncIQ Target reports.


  name (, str, )
    Name of the SyncIQ Target reports.



UserMappingRules (When C(user_mapping_rules) is in a given I(gather_subset), list, [{'apply_order': 1, 'operator': 'append', 'options': {'_break': False, 'default_user': None, 'group': True, 'groups': True, 'user': True}, 'user1': {'domain': None, 'user': 'test_user_2'}, 'user2': {'domain': None, 'user': 'test_user_1'}}])
  List of the User mapping rules.


  apply_order (, int, )
    Current order of the rule.


  operator (, str, )
    The operation that a rule carries out.


  options (, dict, )
    The operation that a rule carries out.


  user1 (, dict, )
    A UNIX user or an Active Directory user.


  user2 (, dict, )
    A UNIX user or an Active Directory user.



Users (When C(users) is in a given I(gather_subset), list, [{'users': [{'dn': 'CN=test_ans_user,CN=Users,DC=X-ISILON-X', 'dns_domain': None, 'domain': 'x-ISILON-X', 'email': 'testuser_ans@dell.com', 'gid': {'id': 'GID:1800', 'name': None, 'type': None}, 'home_directory': '/ifs/home/test_ans_user', 'id': 'test_ans_user', 'name': 'test_ans_user', 'on_disk_user_identity': {'id': 'UID:2016', 'name': None, 'type': None}, 'password_expired': False, 'primary_group_sid': {'id': 'SID:S-1-5-21-2193650305-1279797252-961391754-800', 'name': None, 'type': None}, 'prompt_password_change': False, 'provider': 'lsa-local-provider:System', 'sam_account_name': 'test_ans_user', 'shell': '/bin/zsh', 'sid': {'id': 'SID:S-1-5-21-2193650305-1279797252-961391754-1025', 'name': None, 'type': None}, 'ssh_public_keys': [], 'type': 'user', 'uid': {'id': 'UID:2016', 'name': None, 'type': None}, 'upn': 'test_ans_user@x-ISILON-X', 'user_can_change_password': True}]}])
  List of all Users.


  users (, list, )
    List of users details.


    id (, str, )
      ID of the user.


    name (, str, )
      Name of the user.


    provider (, str, )
      The provider of the user.




nfs_default_settings (always, dict, {'map_root': {'enabled': True, 'primary_group': {'id': 'None', 'name': 'None', 'type': 'None'}, 'secondary_groups': [], 'user': {'id': 'USER:nobody', 'name': 'None', 'type': 'None'}}, 'map_non_root': {'enabled': False, 'primary_group': {'id': 'None', 'name': 'None', 'type': 'None'}, 'secondary_groups': [], 'user': {'id': 'USER:nobody', 'name': 'None', 'type': 'None'}}, 'map_failure': {'enabled': False, 'primary_group': {'id': 'None', 'name': 'None', 'type': 'None'}, 'secondary_groups': [], 'user': {'id': 'USER:nobody', 'name': 'None', 'type': 'None'}}, 'name_max_size': 255, 'block_size': 8192, 'commit_asynchronous': False, 'directory_transfer_size': 131072, 'read_transfer_max_size': 1048576, 'read_transfer_multiple': 512, 'read_transfer_size': 131072, 'setattr_asynchronous': False, 'write_datasync_action': 'DATASYNC', 'write_datasync_reply': 'DATASYNC', 'write_filesync_action': 'FILESYNC', 'write_filesync_reply': 'FILESYNC', 'write_transfer_max_size': 1048576, 'write_transfer_multiple': 512, 'write_transfer_size': 524288, 'write_unstable_action': 'UNSTABLE', 'write_unstable_reply': 'UNSTABLE', 'max_file_size': 9223372036854775807, 'readdirplus': True, 'return_32bit_file_ids': False, 'can_set_time': True, 'encoding': 'DEFAULT', 'map_lookup_uid': False, 'symlinks': True, 'time_delta': '1e-09', 'zone': 'sample-zone'})
  The NFS default settings.


  map_root (, dict, )
    Mapping of incoming root users to a specific user and/or group ID.


  map_non_root (, dict, )
    Mapping of non-root users to a specific user and/or group ID.


  map_failure (, dict, )
    Mapping of users to a specific user and/or group ID after a failed auth attempt.


  name_max_size (, dict, )
    Specifies the reported maximum length of a file name. This parameter does not affect server behavior, but is included to accommodate legacy client requirements.


  block_size (, dict, )
    Specifies the block size returned by the NFS statfs procedure.


  directory_transfer_size (, dict, )
    Specifies the preferred size for directory read operations. This value is used to advise the client of optimal settings for the server, but is not enforced.


  read_transfer_max_size (, dict, )
    Specifies the maximum buffer size that clients should use on NFS read requests. This value is used to advise the client of optimal settings for the server, but is not enforced.


  read_transfer_multiple (, dict, )
    Specifies the preferred multiple size for NFS read requests. This value is used to advise the client of optimal settings for the server, but is not enforced.


  read_transfer_size (, dict, )
    Specifies the preferred size for NFS read requests. This value is used to advise the client of optimal settings for the server, but is not enforced.


  write_transfer_max_size (, dict, )
    Specifies the maximum buffer size that clients should use on NFS write requests. This value is used to advise the client of optimal settings for the server, but is not enforced.


  write_transfer_multiple (, dict, )
    Specifies the preferred multiple size for NFS write requests. This value is used to advise the client of optimal settings for the server, but is not enforced.


  write_transfer_size (, dict, )
    Specifies the preferred multiple size for NFS write requests. This value is used to advise the client of optimal settings for the server, but is not enforced.


  max_file_size (, dict, )
    Specifies the maximum file size for any file accessed from the export. This parameter does not affect server behavior, but is included to accommodate legacy client requirements.


  security_flavors (, list, )
    Specifies the authentication types that are supported for this export.


  commit_asynchronous (, bool, )
    True if NFS commit requests execute asynchronously.


  setattr_asynchronous (, bool, )
    True if set attribute operations execute asynchronously.


  readdirplus (, bool, )
    True if 'readdirplus' requests are enabled. Enabling this property might improve network performance and is only available for NFSv3.


  return_32bit_file_ids (, bool, )
    Limits the size of file identifiers returned by NFSv3+ to 32-bit values (may require remount).


  can_set_time (, bool, )
    True if the client can set file times through the NFS set attribute request. This parameter does not affect server behavior, but is included to accommodate legacy client requirements.


  map_lookup_uid (, bool, )
    True if incoming user IDs (UIDs) are mapped to users in the OneFS user database. When set to False, incoming UIDs are applied directly to file operations.


  symlinks (, bool, )
    True if symlinks are supported. This value is used to advise the client of optimal settings for the server, but is not enforced.


  write_datasync_action (, str, )
    Specifies the synchronization type for data sync action.


  write_datasync_reply (, str, )
    Specifies the synchronization type for data sync reply.


  write_filesync_action (, str, )
    Specifies the synchronization type for file sync action.


  write_filesync_reply (, str, )
    Specifies the synchronization type for file sync reply.


  write_unstable_action (, str, )
    Specifies the synchronization type for unstable action.


  write_unstable_reply (, str, )
    Specifies the synchronization type for unstable reply.


  encoding (, str, )
    Specifies the default character set encoding of the clients connecting to the export, unless otherwise specified.


  time_delta (, dict, )
    Specifies the resolution of all time values that are returned to the clients.


  zone (, str, )
    The zone to which the NFS default settings apply.



SynciqGlobalSettings (always, dict, {'bandwidth_reservation_reserve_absolute': None, 'bandwidth_reservation_reserve_percentage': 1, 'cluster_certificate_id': 'xxxx', 'encryption_cipher_list': '', 'encryption_required': True, 'force_interface': False, 'max_concurrent_jobs': 16, 'ocsp_address': '', 'ocsp_issuer_certificate_id': '', 'preferred_rpo_alert': 0, 'renegotiation_period': 28800, 'report_email': [], 'report_max_age': 31536000, 'report_max_count': 2000, 'restrict_target_network': False, 'rpo_alerts': True, 'service': 'off', 'service_history_max_age': 31536000, 'service_history_max_count': 2000, 'source_network': None, 'tw_chkpt_interval': None, 'use_workers_per_node': False})
  The SyncIQ global settings details.


  bandwidth_reservation_reserve_absolute (, int, )
    The absolute bandwidth reservation for SyncIQ.


  bandwidth_reservation_reserve_percentage (, int, )
    The percentage-based bandwidth reservation for SyncIQ.


  cluster_certificate_id (, str, )
    The ID of the cluster certificate used for SyncIQ.


  encryption_cipher_list (, str, )
    The list of encryption ciphers used for SyncIQ.


  encryption_required (, bool, )
    Whether encryption is required or not for SyncIQ.


  force_interface (, bool, )
    Whether the force interface is enabled or not for SyncIQ.


  max_concurrent_jobs (, int, )
    The maximum number of concurrent jobs for SyncIQ.


  ocsp_address (, str, )
    The address of the OCSP server used for SyncIQ certificate validation.


  ocsp_issuer_certificate_id (, str, )
    The ID of the issuer certificate used for OCSP validation in SyncIQ.


  preferred_rpo_alert (, bool, )
    Whether the preferred RPO alert is enabled or not for SyncIQ.


  renegotiation_period (, int, )
    The renegotiation period in seconds for SyncIQ.


  report_email (, str, )
    The email address to which SyncIQ reports are sent.


  report_max_age (, int, )
    The maximum age in days of reports that are retained by SyncIQ.


  report_max_count (, int, )
    The maximum number of reports that are retained by SyncIQ.


  restrict_target_network (, bool, )
    Whether to restrict the target network in SyncIQ.


  rpo_alerts (, bool, )
    Whether RPO alerts are enabled or not in SyncIQ.


  service (, str, )
    Specifies whether the SyncIQ service is currently on, off, or paused.


  service_history_max_age (, int, )
    The maximum age in days of service history that is retained by SyncIQ.


  service_history_max_count (, int, )
    The maximum number of service history records that are retained by SyncIQ.


  source_network (, str, )
    The source network used by SyncIQ.


  tw_chkpt_interval (, int, )
    The interval between checkpoints in seconds in SyncIQ.


  use_workers_per_node (, bool, )
    Whether to use workers per node in SyncIQ or not.



S3_bucket_details (When C(s3_buckets) is in a given I(gather_subset), dict, {'access_zone': 'System', 'acl': [{'grantee': {'id': 'ID', 'name': 'ansible-user', 'type': 'user'}, 'permission': 'READ'}], 'description': 'description', 'id': 'ansible_S3_bucket', 'name': 'ansible_S3_bucket', 'object_acl_policy': 'replace', 'owner': 'ansible-user', 'path': '/ifs/<sample-path>', 'zid': 1})
  The updated S3 Bucket details.


  acl (, list, )
    Specifies the properties of S3 access controls.


    grantee (, dict, )
      Specifies details of grantee.


      id (, str, )
        ID of the grantee.


      name (, str, )
        Name of the grantee.


      type (, str, )
        Specifies the type of the grantee.



    permission (, str, )
      Specifies the S3 permission being allowed.



  description (, str, )
    Specifies the description of the S3 bucket.


  id (, str, )
    S3 bucket ID.


  name (, str, )
    S3 bucket name.


  object_acl_policy (, str, )
    Set behaviour of object acls for a specified S3 bucket.


  owner (, str, )
    Specifies the owner of the S3 bucket.


  path (, str, )
    Path of S3 bucket with in ``'/ifs'``.


  zid (, int, )
    Zone id.


  zone (, str, )
    Access zone name.






Status
------





Authors
~~~~~~~

- Ambuj Dubey (@AmbujDube) <ansible.team@dell.com>
- Spandita Panigrahi(@panigs7) <ansible.team@dell.com>
- Pavan Mudunuri(@Pavan-Mudunuri) <ansible.team@dell.com>
- Ananthu S Kuttattu(@kuttattz) <ansible.team@dell.com>
- Bhavneet Sharma(@Bhavneet-Sharma) <ansible.team@dell.com>
- Trisha Datta(@trisha-dell) <ansible.team@dell.com>
- Meenakshi Dembi(@dembim) <ansible.team.dell.com>

