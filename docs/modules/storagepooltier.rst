.. _storagepooltier_module:


storagepooltier -- Manages storage pool tier on PowerScale
==========================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Managing storage pool tier on PowerScale Storage System. This includes creating a new storage pool tier, deleting a storage pool tier and retrieving the details of a storage pool tier.



Requirements
------------
The below requirements are needed on the host that executes this module.

- A Dell PowerScale Storage system.
- Ansible-core 2.16 or later.
- Python 3.10, 3.11 or 3.12.



Parameters
----------

  tier_id (optional, int, None)
    Unique Id of the storage pool tier.

    It is mutually exclusive with :emphasis:`tier\_name`.


  tier_name (optional, str, None)
    Unique name of the storage pool tier.

    It is mutually exclusive with :emphasis:`tier\_id`.

    Mandatory for storage pool tier creation.


  nodepools (optional, list, None)
    List of names of the nodepool's.


  state (True, str, None)
    The state option is used to mention the existence of storage pool tier.


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
   - Modifying a storage pool tier is not supported.
   - The :emphasis:`check\_mode` is supported.
   - The modules present in this collection named as 'dellemc.powerscale' are built to support the Dell PowerScale storage platform.




Examples
--------

.. code-block:: yaml+jinja

    
    - name: Get storage pool tier details
      dellemc.powerscale.storagepooltier:
        onefs_host: "{{onefs_host}}"
        verify_ssl: "{{verify_ssl}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        tier_name: "test_tier"
        state: 'present'

    - name: Create a storage pool tier
      dellemc.powerscale.storagepooltier:
        onefs_host: "{{onefs_host}}"
        verify_ssl: "{{verify_ssl}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        tier_name: "test_tier"
        nodepools:
          - "test_nodepool"
        state: 'present'

    - name: Delete a storage pool tier
      dellemc.powerscale.storagepooltier:
        onefs_host: "{{onefs_host}}"
        verify_ssl: "{{verify_ssl}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        tier_name: "test_tier"
        state: 'absent'



Return Values
-------------

changed (always, bool, false)
  Whether or not the resource has changed.


storage_pool_tier_details (When a tier exists, complex, {'storage_pool_tier_details': {'children': ['test_nodepool'], 'id': 1, 'lnns': [1, 2, 3], 'name': 'test_tier'}})
  Storage pool tier details.


  id (, int, )
    Unique ID of the storage pool tier.


  name (, str, )
    Unique name of the storage pool tier.


  children (, list, )
    Nodepool's of the storage pool tier.


  lnns (, list, )
    The nodes that are part of this tier.






Status
------





Authors
~~~~~~~

- Ananthu S Kuttattu (@kuttattz) <ansible.team@dell.com>

