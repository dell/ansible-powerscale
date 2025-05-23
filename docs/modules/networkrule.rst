.. _networkrule_module:


networkrule -- Manages Network provisioning rules for PowerScale Storage System
===============================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Modify an existing network provisioning rule.

Create a new network provisioning rule.

Delete a network provisioning rule.

View the details of a network provisioning rule.



Requirements
------------
The below requirements are needed on the host that executes this module.

- A Dell PowerScale Storage system.
- Ansible-core 2.16 or later.
- Python 3.10, 3.11 or 3.12.



Parameters
----------

  description (optional, str, None)
    Description for rule.

    It can be no more than 128 bytes in length.


  groupnet_name (True, str, None)
    Groupnet name to which this provisioning rule applies.


  iface (optional, str, None)
    Interface to which the rule applies.


  node_type (optional, str, None)
    Node types to which the provisioning rule applies.


  pool_name (True, str, None)
    Pool to which this provisioning rule applies.


  rule_name (True, str, None)
    Name of provisioning rule.


  new_rule_name (optional, str, None)
    Name of provisioning rule when renaming an existing rule.


  subnet_name (True, str, None)
    Name of the subnet to which this provisioning rule applies.


  state (True, str, None)
    State of provisioning rule.


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

    

    - name: Get the details of a network rule
      dellemc.powerscale.networkrule:
        onefs_host: "{{onefs_host}}"
        port_no: "{{port_no}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        verify_ssl: "{{verify_ssl}}"
        groupnet_name: "groupnet1"
        subnet_name: "subnet1"
        pool_name: "pool1"
        rule_name: "rule1"
        state: "present"

    - name: Create a new network provisioning rule
      dellemc.powerscale.networkrule:
        onefs_host: "{{onefs_host}}"
        port_no: "{{port_no}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        verify_ssl: "{{verify_ssl}}"
        groupnet_name: "groupnet1"
        subnet_name: "subnet1"
        pool_name: "pool1"
        rule_name: "new_rule"
        description: "Rename existing rule"
        iface: "ext1"
        node_type: "storage"
        state: "present"

    - name: Modifying an existing network provisioning rule
      dellemc.powerscale.networkrule:
        onefs_host: "{{onefs_host}}"
        port_no: "{{port_no}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        verify_ssl: "{{verify_ssl}}"
        groupnet_name: "groupnet1"
        subnet_name: "subnet1"
        pool_name: "pool1"
        rule_name: "rule_name"
        description: "Modify rule"
        iface: "ext1"
        node_type: "storage"
        state: "present"

    - name: Delete a network provisioning rule
      dellemc.powerscale.networkrule:
        onefs_host: "{{onefs_host}}"
        port_no: "{{port_no}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        verify_ssl: "{{verify_ssl}}"
        groupnet_name: "groupnet1"
        subnet_name: "subnet1"
        pool_name: "pool1"
        rule_name: "rule"
        state: absent



Return Values
-------------

changed (Always, bool, false)
  Whether or not the resource has changed.


network_rule_details (When a network provisioning rule exists, complex, {'description': 'description', 'groupnet': 'groupnet0', 'id': 'groupnet0.subnet0.pool0.test_rule', 'iface': '10gige-1', 'name': 'test_rule', 'node_type': 'any', 'pool': 'pool0', 'subnet': 'subnet0'})
  Network provisioning rule details.


  description (, str, )
    Description of network provisioning rule


  groupnet (, str, )
    Name of groupnet to which this rule belongs


  id (, str, )
    Unique ID for network provisioning rule


  iface (, str, )
    Interface name to which this rule belongs

    For example, ext-1


  name (, str, )
    Name of network provisioning rule


  node_type (, str, )
    Node type to which the provisioning rule applies


  pool (, str, )
    Name of pool to which this rule belongs


  subnet (, str, )
    Name of subnet to which this rule belongs






Status
------





Authors
~~~~~~~

- Spandita Panigrahi (@panigs7) <ansible.team@dell.com>

