.. _node_module:


node -- Get node info of PowerScale Storage System
==================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Get information of a node belonging to the PowerScale cluster.



Requirements
------------
The below requirements are needed on the host that executes this module.

- A Dell PowerScale Storage system.
- Ansible-core 2.13 or later.
- Python 3.9, 3.10 or 3.11.



Parameters
----------

  node_id (True, int, None)
    The Logical node Number of a PowerScale cluster node.


  state (True, str, None)
    Defines whether the node should exist or not.


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
   - The modules present in this collection named as 'dellemc.powerscale' are built to support the Dell PowerScale storage platform.




Examples
--------

.. code-block:: yaml+jinja

    
    - name: Get node info of the PowerScale cluster node
      dellemc.powerscale.node:
        onefs_host: "{{onefs_host}}"
        verify_ssl: "{{verify_ssl}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        node_id: "{{cluster_node_id}}"
        state: "present"



Return Values
-------------

changed (always, bool, )
  Whether or not the resource has changed.


cluster_node_details (When cluster node exists, complex, )
  The cluster node details.


  id (, int, )
    Node id (device number) of a node.


  lnn (, int, )
    Logical Node Number (LNN) of a node.


  partitions (, complex, )
    Node partition information.


    count (, int, )
      Count of how many partitions are included.







Status
------





Authors
~~~~~~~

- Ganesh Prabhu(@prabhg5) <ansible.team@dell.com>>

