.. _groupnet_module:


groupnet -- Manages groupnet configuration on PowerScale
========================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Manages the groupnet configuration on the PowerScale storage system. This includes creating, modifying, deleting and retrieving the details of the groupnet.



Requirements
------------
The below requirements are needed on the host that executes this module.

- A Dell PowerScale Storage system.
- Ansible-core 2.15 or later.
- Python 3.10, 3.11 or 3.12.



Parameters
----------

  groupnet_name (True, str, None)
    The name of the groupnet.


  description (optional, str, None)
    A description of the groupnet.


  new_groupnet_name (optional, str, None)
    Name of the groupnet when renaming an existing groupnet.


  dns_servers (optional, list, None)
    List of Domain Name Server IP addresses.


  dns_server_state (optional, str, None)
    Specifies if the :emphasis:`dns\_servers` should be added or removed from the groupnet.


  dns_search_suffix (optional, list, None)
    List of DNS search suffixes.


  dns_search_suffix_state (optional, str, None)
    Specifies if the dns search suffix should be added or removed from the groupnet.


  state (True, str, None)
    The state of the groupnet after the task is performed.

    :literal:`present` - indicates that the groupnet should exist on the system.

    :literal:`absent` - indicates that the groupnet should not exist on the system.


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
   - The :emphasis:`check\_mode` is not supported.
   - The modules present in this collection named as 'dellemc.powerscale' are built to support the Dell PowerScale storage platform.




Examples
--------

.. code-block:: yaml+jinja

    
    - name: Create a groupnet
      dellemc.powerscale.groupnet:
        onefs_host: "{{onefs_host}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        verify_ssl: "{{verify_ssl}}"
        groupnet_name: "groupnet_test"
        description: "Test Groupnet"
        dns_servers:
          - '198.10.**.***'
        dns_server_state: 'add'
        dns_search_suffix:
          - 'samplesearch.com'
        dns_search_suffix_state: 'add'
        state: "present"

    - name: Add dns servers to a groupnet
      dellemc.powerscale.groupnet:
        onefs_host: "{{onefs_host}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        verify_ssl: "{{verify_ssl}}"
        groupnet_name: "groupnet_test"
        dns_servers:
          - '198.10.**.***'
        dns_server_state: 'add'
        state: "present"

    - name: Remove dns servers from a groupnet
      dellemc.powerscale.groupnet:
        onefs_host: "{{onefs_host}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        verify_ssl: "{{verify_ssl}}"
        groupnet_name: "groupnet_test"
        dns_servers:
          - '198.10.**.***'
        dns_server_state: 'remove'
        state: "present"

    - name: Add dns search suffix to a groupnet
      dellemc.powerscale.groupnet:
        onefs_host: "{{onefs_host}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        verify_ssl: "{{verify_ssl}}"
        groupnet_name: "groupnet_test"
        dns_search_suffix:
          - 'samplesearch.com'
        dns_search_suffix_state: 'add'
        state: "present"

    - name: Remove dns search suffix from a groupnet
      dellemc.powerscale.groupnet:
        onefs_host: "{{onefs_host}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        verify_ssl: "{{verify_ssl}}"
        groupnet_name: "groupnet_test"
        dns_search_suffix:
          - 'samplesearch.com'
        dns_search_suffix_state: 'remove'
        state: "present"

    - name: Rename a groupnet
      dellemc.powerscale.groupnet:
        onefs_host: "{{onefs_host}}"
        port_no: "{{port_no}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        verify_ssl: "{{verify_ssl}}"
        groupnet_name: "groupnet_test"
        new_groupnet_name: "groupnet_test_rename"

    - name: Get groupnet details
      dellemc.powerscale.groupnet:
        onefs_host: "{{onefs_host}}"
        port_no: "{{port_no}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        verify_ssl: "{{verify_ssl}}"
        groupnet_name: "groupnet_test"
        state: "present"

    - name: Delete a groupnet
      dellemc.powerscale.groupnet:
        onefs_host: "{{onefs_host}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        verify_ssl: "{{verify_ssl}}"
        groupnet_name: "groupnet_test"
        state: "absent"



Return Values
-------------

changed (always, bool, false)
  Whether or not the resource has changed.


groupnet_details (When a groupnet exists, complex, {'allow_wildcard_subdomains': True, 'description': 'Initial groupnet', 'dns_cache_enabled': True, 'dns_options': [], 'dns_search': ['ansible.com'], 'dns_servers': ['10.**.**.***'], 'id': 'groupnet0', 'name': 'groupnet0', 'server_side_dns_search': True, 'subnets': ['subnet0']})
  Groupnet details.


  dns_search (, list, )
    List of DNS search suffixes


  dns_servers (, list, )
    List of Domain Name Server IP addresses


  id (, str, )
    Unique Groupnet ID.


  name (, str, )
    Name of groupnet


  subnets (, list, )
    List of names of the subnets in the groupnet






Status
------





Authors
~~~~~~~

- Jennifer John (@johnj9) <ansible.team@dell.com>

