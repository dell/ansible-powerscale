.. _subnet_module:


subnet -- Manages subnet configuration on PowerScale
====================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Manages the subnet configuration on the PowerScale storage system. This includes creating, modifying, deleting and retrieving the details of the subnet.



Requirements
------------
The below requirements are needed on the host that executes this module.

- A Dell PowerScale Storage system. Ansible 2.12, 2.13 or 2.14.



Parameters
----------

  subnet_name (True, str, None)
    Name of the subnet.


  groupnet_name (True, str, None)
    Name of the groupnet.


  description (optional, str, None)
    A description of the subnet.


  netmask (optional, str, None)
    Netmask of the subnet.


  gateway_priority (optional, int, None)
    Gateway priority.


  new_subnet_name (optional, str, None)
    Name of the subnet when renaming an existing subnet.


  subnet_params (optional, dict, None)
    Specify additional parameters to configure the subnet.


    gateway (optional, str, None)
      Gateway IP address.


    sc_service_addrs (optional, list, None)
      List of IP addresses that SmartConnect listens for DNS requests.


      start_range (True, str, None)
        Specifies the start range for sc_service_addrs.


      end_range (True, str, None)
        Specifies the end range for sc_service_addrs.



    sc_service_addrs_state (optional, str, None)
      Specifies if the sc_service_addrs range need to be added or removed from the subnet.


    mtu (optional, int, None)
      MTU of the subnet.


    vlan_enabled (optional, bool, None)
      VLAN tagging enabled or disabled


    vlan_id (optional, int, None)
      VLAN ID for all interfaces in the subnet.



  state (True, str, None)
    The state of the subnet after the task is performed.

    present - indicates that the subnet should exist on the system.

    absent - indicates that the subnet should not exist on the system.


  onefs_host (True, str, None)
    IP address or FQDN of the PowerScale cluster.


  port_no (False, str, 8080)
    Port number of the PowerScale cluster.It defaults to 8080 if not specified.


  verify_ssl (True, bool, None)
    boolean variable to specify whether to validate SSL certificate or not.

    True - indicates that the SSL certificate should be verified.

    False - indicates that the SSL certificate should not be verified.


  api_user (True, str, None)
    username of the PowerScale cluster.


  api_password (True, str, None)
    the password of the PowerScale cluster.





Notes
-----

.. note::
   - The modules present in this collection named as 'dellemc.powerscale' are built to support the Dell PowerScale storage platform.




Examples
--------

.. code-block:: yaml+jinja

    
    - name: Create a subnet
      dellemc.powerscale.subnet:
          onefs_host: "{{onefs_host}}"
          port_no: "{{port_no}}"
          api_user: "{{api_user}}"
          api_password: "{{api_password}}"
          verify_ssl: "{{verify_ssl}}"
          groupnet_name: "groupnet_test"
          subnet_name: "subnet_test"
          description: "Test subnet"
          netmask: '198.10.**.***'
          gateway_priority: 1
          subnet_params:
            gateway: '198.10.**.***'
            sc_service_addrs:
              - start_range : '198.10.**.***'
                end_range: '198.10.**.***'
            sc_service_addrs_state: "add"
            mtu: 1500
            vlan_enabled: true
            vlan_id: 22
          state: 'present'

    - name: Modify a subnet
      dellemc.powerscale.subnet:
          onefs_host: "{{onefs_host}}"
          port_no: "{{port_no}}"
          api_user: "{{api_user}}"
          api_password: "{{api_password}}"
          verify_ssl: "{{verify_ssl}}"
          groupnet_name: "groupnet_test"
          subnet_name: "subnet_test"
          description: "Test subnet"
          netmask: '198.10.**.***'
          gateway_priority: 2
          subnet_params:
            gateway: '198.10.**.***'
            mtu: 1500
            vlan_enabled: true
            vlan_id: 22
          state: 'present'

    - name: Rename a subnet
      dellemc.powerscale.subnet:
          onefs_host: "{{onefs_host}}"
          port_no: "{{port_no}}"
          api_user: "{{api_user}}"
          api_password: "{{api_password}}"
          verify_ssl: "{{verify_ssl}}"
          groupnet_name: "groupnet_test"
          subnet_name: "subnet_test"
          new_subnet_name: "subnet_test_rename"

    - name: Add smart connect service ip range to subnet
      dellemc.powerscale.subnet:
          onefs_host: "{{onefs_host}}"
          port_no: "{{port_no}}"
          api_user: "{{api_user}}"
          api_password: "{{api_password}}"
          verify_ssl: "{{verify_ssl}}"
          groupnet_name: "groupnet_test"
          subnet_name: "subnet_test"
          subnet_params:
            sc_service_addrs:
              - start_range : '198.10.**.***'
                end_range: '198.10.**.***'
            sc_service_addrs_state: "add"
          state: 'present'

    - name: Remove smart connect service ip range from subnet
      dellemc.powerscale.subnet:
          onefs_host: "{{onefs_host}}"
          port_no: "{{port_no}}"
          api_user: "{{api_user}}"
          api_password: "{{api_password}}"
          verify_ssl: "{{verify_ssl}}"
          groupnet_name: "groupnet_test"
          subnet_name: "subnet_test"
          subnet_params:
            sc_service_addrs:
              - start_range : '198.10.**.***'
                end_range: '198.10.**.***'
            sc_service_addrs_state: "remove"
          state: 'present'

    - name: Delete a subnet
      dellemc.powerscale.subnet:
          onefs_host: "{{onefs_host}}"
          port_no: "{{port_no}}"
          api_user: "{{api_user}}"
          api_password: "{{api_password}}"
          verify_ssl: "{{verify_ssl}}"
          groupnet_name: "groupnet_test"
          subnet_name: "subnet_test"
          state: 'absent'



Return Values
-------------

changed (always, bool, )
  Whether or not the resource has changed.


subnet_details (When a subnet exists, complex, )
  Subnet details.


  id (, str, )
    Unique subnet id.


  name (, str, )
    The name of the subnet.


  mtu (, int, )
    MTU of the subnet.


  prefixlen (, int, )
    Subnet prefix length.


  sc_service_addr (, list, )
    The address that SmartConnect listens for DNS requests.


  addr_family (, str, )
    IP address format.


  groupnet (, str, )
    Name of the groupnet this subnet belongs to.


  pools (, list, )
    List of names of pools in the subnet.






Status
------





Authors
~~~~~~~

- Jennifer John (@johnj9) <ansible.team@dell.com>

