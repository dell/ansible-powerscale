.. _networkpool_module:


networkpool -- Manages Network Pools on PowerScale Storage System
=================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Managing Network Pools on the PowerScale Storage System includes creating, modifying, deleting and reterving details of network pool.



Requirements
------------
The below requirements are needed on the host that executes this module.

- A Dell PowerScale Storage system.
- Ansible-core 2.13 or later.
- Python 3.9, 3.10 or 3.11.



Parameters
----------

  pool_name (True, str, None)
    The Name of the pool.


  new_pool_name (optional, str, None)
    Name of the pool when renaming an existing pool.


  groupnet_name (True, str, None)
    The name of the groupnet.


  subnet_name (True, str, None)
    The name of the subnet.


  description (optional, str, None)
    Description of the pool.


  access_zone (optional, str, None)
    Name of access zone to be associated with pool.


  state (True, str, None)
    The state option is used to mention the existence of pool.


  additional_pool_params (optional, dict, None)
    Define additional parameters for pool.


    ranges (optional, list, None)
      List of IP address ranges in this pool.


      low (optional, str, None)
        Lower limit.


      high (optional, str, None)
        Upper limit.



    range_state (optional, str, None)
      This signifies if range needs to be added or removed.


    ifaces (optional, list, None)
      List of Pool interface members.


      iface (optional, str, None)
        Pool interface members


      lnn (optional, int, None)
        Logical Node Number



    iface_state (optional, str, None)
      This signifies if interface needs to be added or removed.



  sc_params (optional, dict, None)
    SmartConnect Parameters.


    static_routes (optional, list, None)
      List of static routes in the pool.


      gateway (True, str, None)
        Address of the gateway in the format yyy.yyy.yyy.yyy.


      prefix_len (True, int, None)
        The subnet mask length.


      subnet (True, str, None)
        Network address in the format xxx.xxx.xxx.xxx.



    sc_dns_zone (optional, str, None)
      SmartConnect zone name for the pool.


    sc_dns_zone_aliases (optional, list, None)
      List of SmartConnect zone aliases (DNS names) to the pool.


    sc_subnet (optional, str, None)
      Name of SmartConnect service subnet for this pool.


    sc_connect_policy (optional, str, None)
      SmartConnect client connection balancing policy.


    sc_failover_policy (optional, str, None)
      SmartConnect IP failover policy.


    rebalance_policy (optional, str, None)
      Rebalance policy.


    alloc_method (optional, str, None)
      Specifies how IP address allocation is done among pool members.


    sc_auto_unsuspend_delay (optional, int, None)
      Time delay in seconds before a node which has been automatically unsuspended becomes usable in SmartConnect responses for pool zones.


    sc_ttl (optional, int, None)
      Time to live value for SmartConnect DNS query responses in seconds.


    aggregation_mode (optional, str, None)
      OneFS supports the following ``NIC`` aggregation modes.



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
   - The *check_mode* is not supported.
   - Removal of static routes and *sc_dns_zone_aliases* is not supported.
   - The modules present in this collection named as 'dellemc.powerscale' are built to support the Dell PowerScale storage platform.




Examples
--------

.. code-block:: yaml+jinja

    
      - name: Create Network Pool
        dellemc.powerscale.networkpool:
          onefs_host: "{{onefs_host}}"
          api_user: "{{api_user}}"
          api_password: "{{api_password}}"
          verify_ssl: "{{verify_ssl}}"
          groupnet: "groupnet0"
          subnet: "subnet0"
          additional_pool_params:
            ranges:
            - low: "10.230.**.***"
              high: "10.230.**.***"
            range_state: "add"
            ifaces:
            - iface: "ext-1"
              lnn: 1
            iface_state: "add"
          sc_params:
            sc_dns_zone: "10.230.**.***"
            sc_connect_policy: "throughput"
            sc_failover_policy: "throughput"
            rebalance_policy: "auto"
            alloc_method: "static"
            sc_auto_unsuspend_delay: 200
            sc_ttl: 200
            sc_dns_zone_aliases:
            - "Test"
            static_routes:
            - gateway: "10.**.**.**"
              prefix_len: 21
              subnet: "10.**.**.**"
          pool: "Test_Pool_2"
          access_zone: "system"
          state: "present"

      - name: Get Network Pool
        dellemc.powerscale.networkpool:
          onefs_host: "{{onefs_host}}"
          api_user: "{{api_user}}"
          api_password: "{{api_password}}"
          verify_ssl: "{{verify_ssl}}"
          groupnet: "groupnet0"
          subnet: "subnet0"
          pool: "Test_Pool_2"
          state: "present"

      - name: Modify Network Pool
        dellemc.powerscale.networkpool:
          onefs_host: "{{onefs_host}}"
          api_user: "{{api_user}}"
          api_password: "{{api_password}}"
          verify_ssl: "{{verify_ssl}}"
          groupnet: "groupnet0"
          subnet: "subnet0"
          pool: "Test_Pool_2"
          additional_pool_params:
            ranges:
            - low: "10.230.**.***"
              high: "10.230.**.***"
            range_state: "add"
            ifaces:
            - iface: "ext-1"
              lnn: 1
            iface_state: "add"
          sc_params:
            sc_dns_zone: "10.230.**.***"
            sc_connect_policy: "throughput"
            sc_failover_policy: "throughput"
            rebalance_policy: "auto"
            alloc_method: "static"
            sc_auto_unsuspend_delay: 200
            sc_ttl: 200
            sc_dns_zone_aliases:
            - "Test"
            static_routes:
            - gateway: "10.**.**.**"
              prefix_len: 21
              subnet: "10.**.**.**"
          aggregation_mode: "fec"
          description: "Pool Created by Ansible Modify"
          state: "present"

      - name: Delete Network Pool
        dellemc.powerscale.networkpool:
          onefs_host: "{{onefs_host}}"
          api_user: "{{api_user}}"
          api_password: "{{api_password}}"
          verify_ssl: "{{verify_ssl}}"
          groupnet: "groupnet0"
          subnet: "subnet0"
          pool: "Test_Pool_2"
          state: "absent"

      - name: Rename a network Pool
        dellemc.powerscale.networkpool:
          onefs_host: "{{onefs_host}}"
          api_user: "{{api_user}}"
          api_password: "{{api_password}}"
          verify_ssl: "{{verify_ssl}}"
          groupnet_name: "groupnet0"
          subnet_name: "subnet0"
          pool_name: "Test_Pool"
          new_pool_name: "Test_Pool_Rename"
          state: "present"



Return Values
-------------

changed (always, bool, false)
  Whether or not the resource has changed.


pools (always, complex, {'pools': [{'access_zone': 'System', 'addr_family': 'ipv4', 'aggregation_mode': 'roundrobin', 'alloc_method': 'static', 'description': '', 'groupnet': 'groupnet0', 'id': 'groupnet0.subnet0.Test_10', 'ifaces': [], 'name': 'Test_10', 'nfsv3_rroce_only': False, 'ranges': [], 'rebalance_policy': 'auto', 'rules': [], 'sc_auto_unsuspend_delay': 0, 'sc_connect_policy': 'round_robin', 'sc_dns_zone': '10.**.**.**', 'sc_dns_zone_aliases': ['Testststst', 'tesrtdsb1'], 'sc_failover_policy': 'round_robin', 'sc_subnet': '', 'sc_suspended_nodes': [], 'sc_ttl': 0, 'static_routes': [{'gateway': '10.**.**.**', 'prefixlen': 21, 'subnet': '10.**.**.**'}], 'subnet': 'subnet0'}]})
  Details of the network pool.


  access_zone (, str, )
    Name of a valid access zone to map IP address pool to the zone.


  addr_family (, str, )
    IP address format.


  aggregation_mode (, str, )
    OneFS supports the following NIC aggregation modes.


  alloc_method (, str, )
    Specifies how IP address allocation is done among pool members.


  description (, str, )
    A description of the pool.


  groupnet (, str, )
    Name of the groupnet this pool belongs to.


  id (, str, )
    Unique Pool ID.


  ifaces (, str, )
    List of interface members in this pool.


  name (, str, )
    The name of the pool. It must be unique throughout the given subnet. It's a required field with POST method.


  ranges (, str, )
    List of IP address ranges in this pool.


  rebalance_policy (, str, )
    Rebalance policy.


  sc_auto_unsuspend_delay (, int, )
    Time delay in seconds before a node which has been automatically unsuspended becomes usable in SmartConnect responses for pool zones.


  sc_connect_policy (, str, )
    SmartConnect client connection balancing policy.


  sc_dns_zone (, str, )
    SmartConnect zone name for the pool.


  sc_dns_zone_aliases (, list, )
    List of SmartConnect zone aliases (DNS names) to the pool.


  sc_failover_policy (, str, )
    SmartConnect IP failover policy.


  sc_subnet (, str, )
    Name of SmartConnect service subnet for this pool.


  sc_suspended_nodes (, list, )
    List of LNNs showing currently suspended nodes in SmartConnect.


  sc_ttl (, int, )
    Time to live value for SmartConnect DNS query responses in seconds.


  static_routes (, list, )
    List of static routes in the pool.


  subnet (, str, )
    The name of the subnet.






Status
------





Authors
~~~~~~~

- Meenakshi Dembi (@dembim) <ansible.team@dell.com>
- Pavan Mudunuri(@Pavan-Mudunuri) <ansible.team@dell.com>

