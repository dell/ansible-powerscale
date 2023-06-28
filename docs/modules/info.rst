.. _info_module:


info -- Gathering information about PowerScale Storage
======================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Gathering information about PowerScale Storage System includes Get attributes of the PowerScale cluster, Get list of access zones in the PowerScale cluster, Get list of nodes in the PowerScale cluster, Get list of authentication providers for all access zones or a specific access zone, Get list of users and groups for an access zone. Get list of smb_shares in the PowerScale cluster, Get list of nfs_exports in the PowerScale cluster, Get list of nfs_aliases in the PowerScale cluster, Get list of active clients in the PowerScale cluster, Get list of SyncIQ reports in the PowerScale cluster, Get list of SyncIQ target reports in the PowerScale cluster, Get list of SyncIQ target cluster certificates in the PowerScale cluster, Get list of SyncIQ policies in the PowerScale cluster. Get list of SyncIQ performance rules in the PowerScale cluster. Get list of network groupnets of the PowerScale cluster. Get list of network pools for all access zones or a specific access zone of the PowerScale cluster. Get list of network rules of the PowerScale cluster. Get list of network subnets of the PowerScale cluster. Get list of network interfaces of the PowerScale cluster. Get list of node pools of PowerScale cluster. Get list of storage pool tiers of PowerScale cluster. Get list of smb open files of PowerScale cluster. Get list of user mapping rules of PowerScale cluster. Get list of ldap providers of the PowerScale cluster



Requirements
------------
The below requirements are needed on the host that executes this module.

- A Dell PowerScale Storage system.
- Ansible-core 2.13 or later.
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

    List of all PowerScale Storage System entities supported by the module -

    attributes

    access_zones

    nodes

    providers

    users

    groups

    smb_shares

    nfs_exports

    nfs_aliases

    clients

    synciq_reports

    synciq_target_reports

    synciq_policies

    synciq_target_cluster_certificates

    synciq_performance_rules

    network_groupnets

    network_pools

    network_rules

    network_interfaces

    network_subnets

    node_pools

    storagepool_tiers

    smb_files

    user_mapping_rules

    ldap

    The list of *attributes*, *access_zones* and *nodes* is for the entire PowerScale cluster

    The list of providers for the entire PowerScale cluster

    The list of users and groups is specific to the specified access zone

    The list of syncIQ reports and syncIQ target reports for the entire PowerScale cluster

    The list of syncIQ policies, syncIQ target cluster certificates and syncIQ performance rules for the entire PowerScale cluster

    The list of network pools is specific to the specified access zone or for all access zones

    The list of network groupnets, network subnets, network rules and network interfaces is for the entire PowerScale cluster

    The list of smb open files for the entire PowerScale cluster

    The list of user mapping rules of PowerScale cluster

    The list of ldap providers of PowerScale cluster


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

      - name: Get list of authentication providers for all access zones of the
              PowerScale cluster
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





Status
------





Authors
~~~~~~~

- Ambuj Dubey (@AmbujDube) <ansible.team@dell.com>
- Spandita Panigrahi(@panigs7) <ansible.team@dell.com>
- Pavan Mudunuri(@Pavan-Mudunuri) <ansible.team@dell.com>
- Ananthu S Kuttattu(@kuttattz) <ansible.team@dell.com>

