.. _info_module:


info -- Gathering information about PowerScale Storage
======================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Gathering information about Specified PowerScale Storage entities, includes attributes, access zones, nodes, authentication providers for all access zones, users and groups for an access zone.

Get list of smb\_shares, nfs\_exports, nfs\_aliases, active clients, SyncIQ reports, SyncIQ target reports, SyncIQ target cluster certificates, SyncIQ policies, SyncIQ performance rules.

Get list of network groupnets, network pools for all access zones or a specific access zone, network rules, network subnets, network interfaces.

Get list of node pools, storage pool tiers, smb open files, s3 buckets, ntp\_servers.

Get list of user mapping rules, ldap providers of the PowerScale cluster.

Get NFS zone settings details of the PowerScale cluster.

Get NFS default settings details of the PowerScale cluster.

Get NFS global settings details of the PowerScale cluster.

Get SyncIQ global settings details of the PowerScale cluster.

Get SMB Global Settings details of the PowerScale cluster.

Get cluster owner, cluster identity and email settings details of the PowerScale cluster.

Get SNMP settings details of the PowerScale cluster.

Retrieve a list of server certificate details.

Get support assist settings details of the PowerScale cluster.

Get list of alert rules, alert channels, alert categories, event groups and alert settings.



Requirements
------------
The below requirements are needed on the host that executes this module.

- A Dell PowerScale Storage system.
- Ansible-core 2.17 or later.
- Python 3.10, 3.11 or 3.12.



Parameters
----------

  access_zone (optional, str, System)
    The access zone. If no Access Zone is specified, the 'System' access zone would be taken by default.


  filters (False, list, None)
    List of filters to support filtered output for storage entities.

    Each filter is a tuple of {filter\_key, filter\_operator, filter\_value}.

    Supports passing of multiple filters.


    filter_key (True, str, None)
      Name identifier of the filter.


    filter_operator (True, str, None)
      Operation to be performed on filter key.


    filter_value (True, raw, None)
      Value of the filter key.



  gather_subset (True, list, None)
    List of string variables to specify the PowerScale Storage System entities for which information is required.

    List of all PowerScale Storage System entities supported by the module.

    Attributes - :literal:`attributes`.

    Access zones - :literal:`access\_zones`.

    Nodes - :literal:`nodes`.

    Providers - :literal:`providers`.

    Users - :literal:`users`.

    Groups - :literal:`groups`.

    Smb shares - :literal:`smb\_shares`.

    Nfs exports - :literal:`nfs\_exports`.

    Nfs aliases - :literal:`nfs\_aliases`.

    Clients - :literal:`clients`.

    Synciq reports - :literal:`synciq\_reports`.

    Synciq target reports - :literal:`synciq\_target\_reports`.

    Synciq policies - :literal:`synciq\_policies`.

    Synciq target cluster certificates - :literal:`synciq\_target\_cluster\_certificates`.

    Synciq performance rules - :literal:`synciq\_performance\_rules`.

    Network groupnets - :literal:`network\_groupnets`.

    Network pools - :literal:`network\_pools`.

    Network rules - :literal:`network\_rules`.

    Network interfaces - :literal:`network\_interfaces`.

    Network subnets - :literal:`network\_subnets`.

    Node pools - :literal:`node\_pools`.

    Storagepool tiers - :literal:`storagepool\_tiers`.

    SMB files - :literal:`smb\_files`.

    User mapping rules - :literal:`user\_mapping\_rules`.

    LDAPs - :literal:`ldap`.

    NFS zone settings - :literal:`nfs\_zone\_settings`.

    NFS default settings - :literal:`nfs\_default\_settings`.

    SyncIQ global settings - :literal:`synciq\_global\_settings`.

    S3 buckets - :literal:`s3\_buckets`.

    The list of :emphasis:`attributes`\ , :emphasis:`access\_zones` and :emphasis:`nodes` is for the entire PowerScale cluster.

    The list of providers for the entire PowerScale cluster.

    The list of users and groups is specific to the specified access zone.

    The list of syncIQ reports and syncIQ target reports for the entire PowerScale cluster.

    The list of syncIQ policies, syncIQ target cluster certificates and syncIQ performance rules for the entire PowerScale cluster.

    The list of network pools is specific to the specified access zone or for all access zones.

    The list of network groupnets, network subnets, network rules and network interfaces is for the entire PowerScale cluster.

    The list of smb open files for the entire PowerScale cluster.

    The list of user mapping rules of PowerScale cluster.

    The list of ldap providers of PowerScale cluster.

    SMB global settings - :literal:`smb\_global\_settings`.

    NTP servers :literal:`ntp\_servers`.

    Email settings :literal:`email\_settings`.

    Cluster identity :literal:`cluster\_identity`.

    Cluster owner :literal:`cluster\_owner`.

    SNMP settings - :literal:`snmp\_settings`.

    Server certificate - :literal:`server\_certificate`.

    Roles - :literal:`roles`.

    Support assist settings- :literal:`support\_assist\_settings`.

    Smartquota- :literal:`smartquota`.

    Filesystem - :literal:`filesystem`.

    Alert settings - :literal:`alert\_settings`.

    Alert rules - :literal:`alert\_rules`.

    Alert channels - :literal:`alert\_channels`.

    Alert categories - :literal:`alert\_categories`.

    Event groups - :literal:`event\_group`.

    Writable snapshots - :literal:`writable\_snapshots`.


  include_all_access_zones (optional, bool, None)
    Specifies if requested component details need to be fetched from all access zones.

    It is mutually exclusive with :emphasis:`access\_zone`.


  scope (optional, str, effective)
    The scope of ldap. If no scope is specified, the :literal:`effective` scope would be taken by default.

    If specified as :literal:`effective` or not specified, all fields are returned.

    If specified as :literal:`user`\ , only fields with non-default values are shown.

    If specified as :literal:`default`\ , the original values are returned.


  query_parameters (optional, dict, None)
    Contains dictionary of query parameters for specific :emphasis:`gather\_subset`.

    Applicable to :literal:`alert\_rules`\ , :literal:`event\_group`\ , :literal:`event\_channels`\ , :literal:`filesystem` and :literal:`writable\_snapshots`.

    If :literal:`writable\_snapshots` is passed as :emphasis:`gather\_subset`\ , if :emphasis:`wspath` is given, all other query parameters inside :emphasis:`writable\_snapshots` will be ignored.

    To view the list of supported query parameters for :literal:`writable\_snapshots`.

    Refer Query Parameters section from \ `https://developer.dell.com/apis/4088/versions/9.5.0/9.5.0.0\_ISLANDER\_OAS2.json/ paths/~1platform~114~1snapshot~1writable/get <https://developer.dell.com/apis/4088/versions/9.5.0/9.5.0.0_ISLANDER_OAS2.json/%20paths/~1platform~114~1snapshot~1writable/get>`__.


  onefs_host (True, str, None)
    IP address or FQDN of the PowerScale cluster.


  port_no (False, str, 8080)
    Port number of the PowerScale cluster.It defaults to 8080 if not specified.


  verify_ssl (True, bool, None)
    boolean variable to specify whether to validate SSL certificate or not.

    :literal:`true` - indicates that the SSL certificate should be verified.

    :literal:`false` - indicates that the SSL certificate should not be verified.


  api_user (True, str, None)
    username of the PowerScale cluster.


  api_password (True, str, None)
    the password of the PowerScale cluster.





Notes
-----

.. note::
   - The parameters :emphasis:`access\_zone` and :emphasis:`include\_all\_access\_zones` are mutually exclusive.
   - The :emphasis:`check\_mode` is supported.
   - Filter functionality is supported only for the following 'gather\_subset'- 'nfs', 'smartquota', 'filesystem' 'writable\_snapshots', 'smb\_files'.
   - The parameter :emphasis:`smb\_files` would return for all the clusters.
   - When :emphasis:`gather\_subset` is :literal:`smb\_files`\ , it is assumed that the credentials of all node is same as the :emphasis:`hostname`.
   - :literal:`support\_assist\_settings` is supported for One FS version 9.5.0 and above.
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

    - name: Get filesystem (/ifs) from PowerScale cluster
      dellemc.powerscale.info:
        onefs_host: "{{ onefs_host }}"
        verify_ssl: "{{ verify_ssl }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"
        gather_subset:
          - filesystem

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
            path: "<path>" # If specified, return filesystem details under the specified path

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
            path: "<path>" # If specified, return filesystem details under the specified path
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



NetworkInterfaces (When C(network_interfaces) is in a given I(gather_subset), list, [{'flags': [], 'id': '3:ext-agg', 'ip_addrs': [], 'ipv4_gateway': None, 'ipv6_gateway': None, 'lnn': 3, 'mtu': 0, 'name': 'ext-agg', 'nic_name': 'lagg0', 'owners': [], 'speed': None, 'status': 'inactive', 'type': 'aggregated', 'vlans': []}])
  List of Network interfaces.


  flags (, list, )
    List of interface flags.


  id (, str, )
    ID of the interface.


  ip_addrs (, list, )
    List of IP addresses.


  ipv4_gateway (, str, )
    Address of the default IPv4 gateway.


  ipv6_gateway (, str, )
    Address of the default IPv6 gateway.


  lnn (, int, )
    Interface's lnn.


  mtu (, int, )
    The mtu the interface.


  name (, str, )
    Name of the interface.


  nic_name (, str, )
    NIC name.


  owners (, list, )
    List of owners.


  speed (, int, )
    Interface's speed.


  status (, str, )
    Status of the interface.


  type (, str, )
    Type of the interface.


  vlans (, list, )
    List of VLANs.



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



NfsExports (When C(nfs_exports) is in a given I(gather_subset), list, [{'all_dir': 'false'}, {'block_size': 8192}, {'clients': 'None'}, {'id': 9324}, {'read_only_client': ['x.x.x.x']}, {'security_flavors': ['unix', 'krb5']}, {'zone': 'System'}, {'map_root': {'enabled': True, 'primary_group': {'id': 'GROUP:group1', 'name': None, 'type': None}, 'secondary_groups': [], 'user': {'id': 'USER:user', 'name': None, 'type': None}}}, {'map_non_root': {'enabled': False, 'primary_group': {'id': None, 'name': None, 'type': None}, 'secondary_groups': [], 'user': {'id': 'USER:nobody', 'name': None, 'type': None}}}])
  List of NFS exports.


  all_dirs (, bool, )
    :emphasis:`sub\_directories\_mountable` flag value.


  id (, int, 12)
    The ID of the NFS Export, generated by the array.


  paths (, list, ['/ifs/dir/filepath'])
    The filesystem path.


  zone (, str, System)
    Specifies the zone in which the export is valid.


  read_only (, bool, )
    Specifies whether the export is read-only or read-write.


  read_only_clients (, list, ['client_ip', 'client_ip'])
    The list of read only clients for the NFS Export.


  read_write_clients (, list, ['client_ip', 'client_ip'])
    The list of read write clients for the NFS Export.


  root_clients (, list, ['client_ip', 'client_ip'])
    The list of root clients for the NFS Export.


  clients (, list, ['client_ip', 'client_ip'])
    The list of clients for the NFS Export.


  description (, str, )
    Description for the export.


  map_root (, complex, )
    Specifies the users and groups to which non-root and root clients are mapped.


    enabled (, bool, )
      True if the user mapping is applied.


    user (, complex, )
      Specifies the persona name.


      id (, str, )
        Specifies the persona name.



    primary_group (, complex, )
      Specifies the primary group.


      id (, str, )
        Specifies the primary group name.



    secondary_groups (, list, )
      Specifies the secondary groups.



  map_non_root (, complex, )
    Specifies the users and groups to which non-root and root clients are mapped.


    enabled (, bool, )
      True if the user mapping is applied.


    user (, complex, )
      Specifies the persona details.


      id (, str, )
        Specifies the persona name.



    primary_group (, complex, )
      Specifies the primary group details.


      id (, str, )
        Specifies the primary group name.



    secondary_groups (, list, )
      Specifies the secondary groups details.




NfsZoneSettings (When C(nfs_zone_settings) is in a given I(gather_subset), dict, {'nfsv4_allow_numeric_ids': True, 'nfsv4_domain': 'sample.com', 'nfsv4_no_domain': True, 'nfsv4_no_domain_uids': True, 'nfsv4_no_names': True, 'nfsv4_replace_domain': True, 'zone': 'System'})
  Details of NFS zone settings.


  nfsv4_allow_numeric_ids (, bool, )
    If :literal:`true`\ , sends owners and groups as UIDs and GIDs when look up fails or if the :emphasis:`nfsv4\_no\_names` property is set to 1.


  nfsv4_domain (, str, )
    Specifies the domain through which users and groups are associated.


  nfsv4_no_domain (, bool, )
    If :literal:`true`\ , sends owners and groups without a domain name.


  nfsv4_no_domain_uids (, bool, )
    If :literal:`true`\ , sends UIDs and GIDs without a domain name.


  nfsv4_no_names (, bool, )
    If :literal:`true`\ , sends owners and groups as UIDs and GIDs.


  nfsv4_replace_domain (, bool, )
    If :literal:`true`\ , replaces the owner or group domain with an NFS domain name.


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




SmbOpenFiles (When C(smb_files) is in a given I(gather_subset), list, [{'file': 'C:\\ifs', 'id': 1370, 'locks': 0, 'node': 'xx.xx.xx.xx', 'permissions': ['read'], 'user': 'admin'}])
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


  node (, str, )
    The node on which the file is open.



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
    Path of S3 bucket with in :literal:`'/ifs'`.


  zid (, int, )
    Zone id.


  zone (, str, )
    Access zone name.



SmbGlobalSettings (always, dict, {'access_based_share_enum': False, 'audit_fileshare': None, 'audit_logon': None, 'dot_snap_accessible_child': True, 'dot_snap_accessible_root': True, 'dot_snap_visible_child': False, 'dot_snap_visible_root': True, 'enable_security_signatures': False, 'guest_user': 'nobody', 'ignore_eas': False, 'onefs_cpu_multiplier': 4, 'onefs_num_workers': 0, 'reject_unencrypted_access': False, 'require_security_signatures': False, 'server_side_copy': False, 'server_string': 'PowerScale Server', 'service': True, 'srv_cpu_multiplier': None, 'srv_num_workers': None, 'support_multichannel': True, 'support_netbios': False, 'support_smb2': True, 'support_smb3_encryption': True})
  The updated SMB global settings details.


  access_based_share_enum (, bool, )
    Only enumerate files and folders the requesting user has access to.


  audit_fileshare (, str, )
    Specify level of file share audit events to log.


  audit_logon (, str, )
    Specify the level of logon audit events to log.


  dot_snap_accessible_child (, bool, )
    Allow access to .snapshot directories in share subdirectories.


  dot_snap_accessible_root (, bool, )
    Allow access to the .snapshot directory in the root of the share.


  dot_snap_visible_child (, bool, )
    Show .snapshot directories in share subdirectories.


  dot_snap_visible_root (, bool, )
    Show the .snapshot directory in the root of a share.


  enable_security_signatures (, bool, )
    Indicates whether the server supports signed SMB packets.


  guest_user (, str, )
    Specifies the fully-qualified user to use for guest access.


  ignore_eas (, bool, )
    Specify whether to ignore EAs on files.


  onefs_cpu_multiplier (, int, )
    Specify the number of OneFS driver worker threads per CPU.


  onefs_num_workers (, int, )
    Set the maximum number of OneFS driver worker threads.


  reject_unencrypted_access (, bool, )
    If SMB3 encryption is enabled, reject unencrypted access from clients.


  require_security_signatures (, bool, )
    Indicates whether the server requires signed SMB packets.


  server_side_copy (, bool, )
    Enable Server Side Copy.


  server_string (, str, )
    Provides a description of the server.


  service (, bool, )
    Specify whether service is enabled.


  srv_cpu_multiplier (, int, )
    Specify the number of SRV service worker threads per CPU.


  srv_num_workers (, int, )
    Set the maximum number of SRV service worker threads.


  support_multichannel (, bool, )
    Support multichannel.


  support_netbios (, bool, )
    Support NetBIOS.


  support_smb2 (, bool, )
    The support SMB2 attribute.


  support_smb3_encryption (, bool, )
    Support the SMB3 encryption on the server.



email_settings (Always, dict, {'settings': {'batch_mode': 'none', 'mail_relay': '10.**.**.**', 'mail_sender': 'powerscale@dell.com', 'mail_subject': 'Powerscale Cluster notifications', 'smtp_auth_passwd_set': False, 'smtp_auth_security': 'none', 'smtp_auth_username': '', 'smtp_port': 25, 'use_smtp_auth': False, 'user_template': ''}})
  Details of the email settings.


  settings (Always, dict, )
    Details of the settings.


    batch_mode (, str, )
      This setting determines how notifications will be batched together to be sent by email.


    mail_relay (, str, )
      The address of the SMTP server to be used for relaying the notification messages.


    mail_sender (, str, )
      The full email address that will appear as the sender of notification messages.


    mail_subject (, str, )
      The subject line for notification messages from this cluster.


    smtp_auth_passwd_set (, bool, )
      Indicates if an SMTP authentication password is set.


    smtp_auth_security (, str, )
      The type of secure communication protocol to use if SMTP is being used.


    smtp_auth_username (, str, )
      Username to authenticate with if SMTP authentication is being used.


    smtp_port (, int, )
      The port on the SMTP server to be used for relaying the notification messages.


    use_smtp_auth (, bool, )
      If true, this cluster will send SMTP authentication credentials to the SMTP relay server in order to send its notification emails.


    user_template (, str, )
      Location of a custom template file that can be used to specify the layout of the notification emails.




ntp_servers (Always, dict, {'servers': [{'id': '10.**.**.**', 'key': None, 'name': '10.**.**.**'}]})
  List of NTP servers.


  servers (, list, )
    List of servers.


    id (, str, )
      Field id.


    key (, str, )
      Key value from :emphasis:`key\_file` that maps to this server.


    name (, str, )
      NTP server name.




cluster_identity (Always, dict, {'cluster_identity': {'description': 'asdadasdasdasdadadadds', 'logon': {'motd': 'This is new description', 'motd_header': 'This is the new title'}, 'mttdl_level_msg': 'none', 'name': 'PIE-IsilonS-24241-Clusterwrerwerwrewr'}})
  Details related to cluster identity.


  description (, str, )
    Description of PowerScale cluster.


  logon (, dict, )
    Details of logon message shown on Powerscale login screen.


    motd (, str, )
      Details of logon message.


    motd_header (, str, )
      Details of logon message title.



  mttdl_level_msg (, str, )
    mttdl\_level\_msg.


  name (, str, )
    Name of PowerScale cluster.



cluster_owner (Always, dict, {'cluster_owner': {'company': 'Test company', 'location': 'Test location', 'primary_email': 'primary_email@email.com', 'primary_name': 'primary_name', 'primary_phone1': 'primary_phone1', 'primary_phone2': 'primary_phone2', 'secondary_email': 'secondary_email@email.com', 'secondary_name': 'secondary_name', 'secondary_phone1': 'secondary_phone1', 'secondary_phone2': 'secondary_phone2'}})
  Details related to cluster identity.


  company (, str, )
    Name of the company.


  location (, str, )
    Location of the company.


  primary_email (, str, )
    Email of primary system admin.


  primary_name (, str, )
    Name of primary system admin.


  primary_phone1 (, str, )
    Phone1 of primary system admin.


  primary_phone2 (, str, )
    Phone2 of primary system admin.


  secondary_email (, str, )
    Email of secondary system admin.


  secondary_name (, str, )
    Name of secondary system admin.


  secondary_phone1 (, str, )
    Phone1 of secondary system admin.


  secondary_phone2 (, str, )
    Phone2 of secondary system admin.



SnmpSettings (When C(snmp_settings) is in a given I(gather_subset), dict, {'read_only_community': 'public', 'service': True, 'snmp_v1_v2c_access': True, 'snmp_v3_access': True, 'snmp_v3_auth_protocol': 'MD5', 'snmp_v3_priv_protocol': 'DES', 'snmp_v3_security_level': 'authPriv', 'snmp_v3_read_only_user': 'general', 'system_contact': 'system', 'system_location': 'cluster'})
  The SNMP settings details.


  read_only_community (, str, )
    SNMP Read-only community name.


  service (, bool, )
    Whether the SNMP Service is enabled.


  snmp_v1_v2c_access (, bool, )
    Whether the SNMP v2c access is enabled.


  snmp_v3_access (, bool, )
    Whether the SNMP v3 access is enabled.


  snmp_v3_auth_protocol (, str, )
    SNMP v3 authentication protocol.


  snmp_v3_priv_protocol (, str, )
    SNMP v3 privacy protocol.


  snmp_v3_security_level (, str, )
    SNMP v3 security level.


  snmp_v3_read_only_user (, str, )
    SNMP v3 read-only user.


  system_contact (, str, )
    SNMP system owner contact information.


  system_location (, str, )
    The cluster description of the SNMP system.



ServerCertificate (When C(server_certificate) is in a given I(gather_subset), list, [{'certificate_monitor_enabled': True, 'certificate_pre_expiration_threshold': 4294, 'description': 'This the example test description', 'dnsnames': ['powerscale'], 'fingerprints': [{'type': 'SHA1', 'value': '68:b2:d5:5d:cc:b0:70:f1:f0:39:3a:bb:e0:44:49:70:6e:05:c3:ed'}, {'type': 'SHA256', 'value': '69:99:b9:c0:29:49:c9:62:e8:4b:60:05:60:a8:fa:f0:01:ab:24:43:8a:47:4c:2f:66:2c:95:a1:7c:d8:10:34'}], 'id': '6999b9c02949c962e84b600560a8faf001ab24438a474c2f662c95a17cd81034', 'issuer': 'C=IN, ST=Karnataka, L=Bangalore, O=Dell, OU=ISG, CN=powerscale, emailAddress=contact@dell.com', 'name': 'test', 'not_after': 1769586969, 'not_before': 1706514969, 'status': 'valid', 'subject': 'C=IN, ST=Karnataka, L=Bangalore, O=Dell, OU=ISG, CN=powerscale, emailAddress=contact@dell.com'}])
  The Server certificate details.


  description (, str, )
    Description of the certificate.


  id (, str, )
    System assigned certificate id.


  issuer (, str, )
    Name of the certificate issuer.


  name (, str, )
    Name for the certificate.


  not_after (, str, )
    The date and time from which the certificate becomes valid and can be used for authentication and encryption.


  not_before (, str, )
    The date and time until which the certificate is valid and can be used for authentication and encryption.


  status (, str, )
    Status of the certificate.


  fingerprints (, str, )
    Fingerprint details of the certificate.


  dnsnames (, list, )
    Subject alternative names of the certificate.


  subject (, str, )
    Subject of the certificate.


  certificate_monitor_enabled (, bool, )
    Boolean value indicating whether certificate expiration monitoring is enabled.


  certificate_pre_expiration_threshold (, int, )
    The number of seconds before certificate expiration that the certificate expiration monitor will start raising alerts.



roles (When C(roles) is in a given I(gather_subset), dict, {'roles': [{'description': 'Test_Description', 'id': 'Test_Role', 'members': [{'id': 'UID:2008', 'name': 'esa', 'type': 'user'}], 'name': 'Test_Role', 'privileges': [{'id': 'ISI_PRIV_LOGIN_PAPI', 'name': 'Platform API', 'permission': 'r'}]}]})
  List of auth roles.


  description (, str, )
    Description of the auth role.


  id (, str, )
    id of the auth role.


  name (, str, )
    Name of the auth role.


  members (, list, )
    Specifies the members of auth role.


    id (, str, )
      ID of the member.


    name (, str, )
      Name of the member.


    type (, str, )
      Specifies the type of the member.



  privileges (, list, )
    Specifies the privileges of auth role.


    id (, str, )
      ID of the privilege.


    name (, str, )
      Name of the privilege.


    permission (, str, )
      Specifies the permission of the privilege.




smart_quota (always, list, [{'container': True, 'description': '', 'efficiency_ratio': None, 'enforced': False, 'id': 'iddd', 'include_snapshots': False, 'labels': '', 'linked': False, 'notifications': 'default', 'path': 'VALUE_SPECIFIED_IN_NO_LOG_PARAMETER', 'persona': {'id': 'UID:9355', 'name': 'test_user_12', 'type': 'user'}, 'ready': True, 'reduction_ratio': None, 'thresholds': {'advisory': None, 'advisory_exceeded': False, 'advisory_last_exceeded': None, 'hard': None, 'hard_exceeded': False, 'hard_last_exceeded': None, 'percent_advisory': None, 'percent_soft': None, 'soft': None, 'soft_exceeded': False, 'soft_grace': None, 'soft_last_exceeded': None}, 'thresholds_on': 'applogicalsize', 'type': 'user', 'usage': {'applogical': 0, 'applogical_ready': True, 'fslogical': 0, 'fslogical_ready': True, 'fsphysical': 0, 'fsphysical_ready': False, 'inodes': 0, 'inodes_ready': True, 'physical': 0, 'physical_data': 0, 'physical_data_ready': True, 'physical_protection': 0, 'physical_protection_ready': True, 'physical_ready': True, 'shadow_refs': 0, 'shadow_refs_ready': True}}])
  The smart quota details.


  id (, str, 2nQKAAEAAAAAAAAAAAAAQIMCAAAAAAAA)
    The ID of the Quota.


  enforced (, bool, True)
    Whether the limits are enforced on Quota or not.


  container (, bool, True)
    If :literal:`true`\ , SMB shares using the quota directory see the quota thresholds as share size.


  thresholds (, dict, {'advisory': 3221225472, 'advisory(GB)': '3.0', 'advisory_exceeded': False, 'advisory_last_exceeded': 0, 'hard': 6442450944, 'hard(GB)': '6.0', 'hard_exceeded': False, 'hard_last_exceeded': 0, 'soft': 5368709120, 'soft(GB)': '5.0', 'soft_exceeded': False, 'soft_grace': 3024000, 'soft_last_exceeded': 0})
    Includes information about all the limits imposed on quota. The limits are mentioned in bytes and :emphasis:`soft\_grace` is in seconds.


  type (, str, directory)
    The type of Quota.


  usage (, dict, {'inodes': 1, 'logical': 0, 'physical': 2048})
    The Quota usage.



file_system (always, list, [{'name': 'home'}, {'name': 'smb11'}])
  The filesystem details.

  If path is not specified in query\_parameters, the filesystem /ifs details are returned.

  If path is specified in query\_parameters, the filesystem details under the specified path are returned.


  name (, str, home)
    The name of the filesystem.



support_assist_settings (When C(support_assist_settings) is in a given I(gather_subset), dict, {'automatic_case_creation': False, 'connection': {'gateway_endpoints': [{'enabled': True, 'host': 'XX.XX.XX.XX', 'port': 9443, 'priority': 1, 'use_proxy': False, 'validate_ssl': False}, {'enabled': True, 'host': 'XX.XX.XX.XY', 'port': 9443, 'priority': 2, 'use_proxy': False, 'validate_ssl': False}], 'mode': 'gateway', 'network_pools': [{'pool': 'pool1', 'subnet': 'subnet0'}]}, 'connection_state': 'disabled', 'contact': {'primary': {'email': 'p7VYg@example.com', 'first_name': 'Eric', 'last_name': 'Nam', 'phone': '1234567890'}, 'secondary': {'email': 'kangD@example.com', 'first_name': 'Daniel', 'last_name': 'Kang', 'phone': '1234567891'}}, 'enable_download': False, 'enable_remote_support': False, 'onefs_software_id': 'ELMISL1019H4GY', 'supportassist_enabled': True, 'telemetry': {'offline_collection_period': 60, 'telemetry_enabled': True, 'telemetry_persist': True, 'telemetry_threads': 10}})
  The support assist settings details.


  automatic_case_creation (, bool, )
    :literal:`True` indicates automatic case creation is enabled.


  connection (, dict, )
    Support assist connection details.


    gateway_endpoints (, list, )
      List of gateway endpoints.


      gateway_host (, str, )
        Hostname or IP address of the gateway endpoint.


      gateway_port (, int, )
        Port number of the gateway endpoint.


      priority (, int, )
        Priority of the gateway endpoint.


      use_proxy (, bool, )
        Use proxy.


      validate_ssl (, bool, )
        Validate SSL.


      enabled (, bool, )
        Enable the gateway endpoint.



    mode (, str, )
      Connection mode.


    network_pools (, list, )
      List of network pools.


      pool (, str, )
        Name of the network pool.


      subnet (, str, )
        Name of the subnet of the network pool.




  connection_state (, str, )
    Set connectivity state.


  contact (, dict, )
    Information on the remote support contact.


    primary (, dict, )
      Primary contact details.


      first_name (, str, )
        First name of the primary contact.


      last_name (, str, )
        Last name of the primary contact.


      email (, str, )
        Email address of the primary contact.


      phone (, str, )
        Phone number of the primary contact.



    secondary (, dict, )
      Secondary contact details.


      first_name (, str, )
        First name of the secondary contact.


      last_name (, str, )
        Last name of the secondary contact.


      email (, str, )
        Email address of the secondary contact.


      phone (, str, )
        Phone number of the secondary contact.




  telemetry (, dict, )
    Enable telemetry.


    offline_collection_period (, int, )
      Change the offline collection period for when the connection to gateway is down.

      The range is 0 to 86400.


    telemetry_enabled (, bool, )
      Change the status of telemetry.


    telemetry_persist (, bool, )
      Change if files are kept after upload.


    telemetry_threads (, int, )
      Change the number of threads for telemetry gathers.

      The range is 1 to 64.



  enable_download (, bool, )
    :literal:`True` indicates downloads are enabled.


  enable_remote_support (, bool, )
    Allow remote support.


  enable_service (, bool, )
    Enable/disable Support Assist service.


  accepted_terms (, bool, )
    Whether to accept or reject the terms and conditions for remote support.



alert_settings (When C(alert_settings) is in a given I(gather_subset)., dict, {'history': [{'end': 0, 'start': 1719822336}], 'maintenance': 'false'})
  The alert settings details.


  history (, list, )
    History list of CELOG maintenance mode windows.


    end (, int, )
      End time of CELOG maintenance mode, as a UNIX timestamp in seconds.

      Value 0 indicates that maintenance mode is still enabled.


    start (, int, )
      Start time of CELOG maintenance mode, as a UNIX timestamp in seconds.



  maintenance (, bool, )
    Indicates if maintenance mode is enabled.



alert_categories (When C(alert_categories) is in a given I(gather_subset)., list, {'categories': [{'id': '200000000', 'id_name': 'NODE_STATUS_EVENTS', 'name': 'Node status events'}], 'resume': None, 'total': 1})
  The alert categories details.


  categories (, list, )
    High level categorisation of eventgroups.


    id (, str, )
      Numeric identifier of eventgroup category.


    id_name (, str, )
      Name of category.


    name (, str, )
      Description of category.



  resume (, str, )
    Provide this token as the 'resume' query argument to continue listing results.


  total (, int, )
    Total number of items available.



alert_channels (When C(alert_channels) is in a given I(gather_subset)., list, {'channels': [{'allowed_nodes': [], 'enabled': 'true', 'excluded_nodes': [], 'id': 2, 'name': 'Heartbeat Self-Test', 'parameters': {'address': [], 'batch': '', 'batch_period': '', 'custom_template': '', 'send_as': '', 'smtp_host': '', 'smtp_password': '', 'smtp_port': '', 'smtp_security': '', 'smtp_use_auth': '', 'smtp_username': '', 'subject': ''}, 'rules': ['Heatrbeat'], 'system': 'true', 'type': 'heartbreak'}], 'resume': None, 'total': 1})
  The alert channels details.


  channels (, list, )
    Named channel through which alerts can be delivered.


    allowed_nodes (, list, )
      Nodes (LNNs) that can be masters for this channel.


    enabled (, bool, )
      Channel is to be used or not.


    excluded_nodes (, list, )
      Nodes (LNNs) that cannot be masters for this channel.


    parameters (, dict, )
      Parameters to be used for an smtp channel.


      address (, list, )
        Email addresses to send to.


      batch (, str, )
        Batching criterion.


      batch_period (, int, )
        Period over which batching is to be performed.


      custom_template (, str, )
        Path to custom notification template.


      send_as (, str, )
        Email address to use as from.


      smtp_host (, str, )
        SMTP host.


      smtp_password (, str, )
        Password for SMTP authentication, only if smtp\_use\_auth true.


      smtp_port (, int, )
        SMTP relay port. It defaults to 25.


      smtp_security (, str, )
        Encryption protocol to use for SMTP.


      smtp_use_auth (, bool, )
        Use SMTP authentication. It defaults to false.


      smtp_username (, str, )
        Username for SMTP authentication, only if smtp\_use\_auth true.


      subject (, str, )
        Subject for emails.



    system (, bool, )
      Channel is a pre-defined system channel.


    type (, str, )
      The mechanism used by the channel.


    id (, int, )
      Unique identifier.


    name (, str, )
      Channel name, may not contain /.


    rules (, str, )
      Alert rules involving this eventgroup type.



  resume (, str, )
    Provide this token as the 'resume' query argument to continue listing results.


  total (, int, )
    Total number of items available.



alert_rules (When C(alert_rules) is in a given I(gather_subset)., list, {'alert_conditions': [{'categories': [], 'channels': [], 'condition': 'ONGOING', 'eventgroup_ids': ['400050004'], 'exclude_eventgroup_ids': [], 'id': 1, 'interval': 0, 'limit': 0, 'name': 'Heartbeat Self-Test', 'severities': [], 'transient': 0}], 'resume': None, 'total': 1})
  The alert rules details.


  alert_conditions (, list, )
    Specifies under what conditions and over which channel an alert should be sent.


    categories (, list, )
      Event Group categories to be alerted.


    channels (, list, )
      Channels for alert.


    condition (, str, )
      Trigger condition for alert.


    eventgroup_ids (, list, )
      Event Group IDs to be alerted.


    exclude_eventgroup_ids (, list, )
      Event Group categories to be excluded from alerts.


    id (, int, )
      Unique identifier.


    interval (, int, )
      Required with ONGOING condition only, period in seconds between alerts of ongoing conditions.


    limit (, int, )
      Required with NEW EVENTS condition only, limits the number of alerts sent as events are added.


    name (, str, )
      Unique identifier.


    severities (, list, )
      Severities to be alerted.


    transient (, int, )
      Any eventgroup lasting less than this many seconds is deemed transient and will not generate alerts under this condition.



  resume (, str, )
    Provide this token as the 'resume' query argument to continue listing results.


  total (, int, )
    Total number of items available.



event_groups (When C(event_group) is in a given I(gather_subset)., list, {'eventgroup_definitions': [{'category': '400000000', 'channels': [], 'description': 'ONGOING', 'id': 1, 'name': 'Heartbeat Self-Test', 'no_ignore': True, 'node': True, 'rules': [], 'suppressed': False}], 'resume': None, 'total': 1})
  The event group details.


  eventgroup_definitions (, list, )
    Description of an eventgroup that can occur and be detected.


    category (, list, )
      ID of eventgroup category.


    channels (, list, )
      Channels by which this eventgroup type can be alerted.


    description (, str, )
      Human readable description, may contain value placeholders.


    id (, int, )
      Unique identifier.


    name (, str, )
      Name for eventgroup.


    no_ignore (, bool, )
      True if event should not be ignored.


    node (, bool, )
      True if this eventgroup type is node specific, false cluster wide.


    rules (, list, )
      Alert rules involving this eventgroup type.


    suppressed (, bool, )
      True if alerting is suppressed for this eventgroup type.



  resume (, str, )
    Provide this token as the 'resume' query argument to continue listing results.


  total (, int, )
    Total number of items available.






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
- Sachin Apagundi(@sachin-apa) <ansible.team.dell.com>
- Kritika Bhateja(@Kritika-Bhateja-03) <ansible.team.dell.com>

