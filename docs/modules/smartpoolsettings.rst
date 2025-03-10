.. _smartpoolsettings_module:


smartpoolsettings -- Manages Smartpool Settings on PowerScale Storage System
============================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Managing Smartpool Settings on the PowerScale Storage System includes modifying and retrieving details of Smartpool settings.



Requirements
------------
The below requirements are needed on the host that executes this module.

- A Dell PowerScale Storage system.
- Ansible-core 2.15 or later.
- Python 3.10, 3.11 or 3.12.



Parameters
----------

  virtual_hot_spare_hide_spare (optional, bool, None)
    Hide reserved virtual hot spare space from free space counts.


  virtual_hot_spare_limit_percent (optional, int, None)
    The percent space to reserve for the virtual hot spare, from 0-20.


  state (True, str, None)
    State of smartpool settings.


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

    
    - name: Get SmartPool settings
      dellemc.powerscale.smartpoolsettings:
        onefs_host: "{{onefs_host}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        verify_ssl: "{{verify_ssl}}"
        state: "{{state_present}}"

    - name: Modify SmartPool setting
      dellemc.powerscale.smartpoolsettings:
        onefs_host: "{{onefs_host}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        verify_ssl: "{{verify_ssl}}"
        virtual_hot_spare_limit_percent: 10
        virtual_hot_spare_hide_spare: true
        state: "present"



Return Values
-------------

changed (always, bool, false)
  Whether or not the resource has changed.


smartpool_settings (always, dict, {'settings': {'automatically_manage_io_optimization': 'files_at_default', 'automatically_manage_protection': 'files_at_default', 'global_namespace_acceleration_enabled': False, 'global_namespace_acceleration_state': 'inactive', 'protect_directories_one_level_higher': True, 'spillover_enabled': True, 'spillover_target': {'id': None, 'name': None, 'type': 'anywhere'}, 'ssd_l3_cache_default_enabled': True, 'ssd_qab_mirrors': 'one', 'ssd_system_btree_mirrors': 'one', 'ssd_system_delta_mirrors': 'one', 'virtual_hot_spare_deny_writes': False, 'virtual_hot_spare_hide_spare': True, 'virtual_hot_spare_limit_drives': 0, 'virtual_hot_spare_limit_percent': 20}})
  Details of the smartpool settings.


  settings (Always, dict, )
    Details of the settings.


    automatically_manage_io_optimization (, str, )
      Automatically manage IO optimization settings on files.


    automatically_manage_protection (, str, )
      Automatically manage protection settings on files.


    global_namespace_acceleration_enabled (, bool, )
      Optimize namespace operations by storing metadata on SSDs.


    global_namespace_acceleration_state (, str, )
      Whether or not namespace operation optimizations are currently in effect.


    protect_directories_one_level_higher (, bool, )
      Automatically add additional protection level to all directories.


    spillover_enabled (, bool, )
      Spill writes into other pools as needed.


    spillover_target (, dict, )
      Target pool for spilled writes.


    ssd_l3_cache_default_enabled (, bool, )
      The L3 Cache default enabled state. This specifies whether L3 Cache should be enabled on new node pools.


    ssd_qab_mirrors (, str, )
      Controls number of mirrors of QAB blocks to place on SSDs.


    ssd_system_btree_mirrors (, str, )
      Controls number of mirrors of system B-tree blocks to place on SSDs.


    ssd_system_delta_mirrors (, str, )
      Controls number of mirrors of system delta blocks to place on SSDs.


    virtual_hot_spare_deny_writes (, bool, )
      Deny writes into reserved virtual hot spare space.


    virtual_hot_spare_hide_spare (, bool, )
      Hide reserved virtual hot spare space from free space counts.


    virtual_hot_spare_limit_drives (, int, )
      The number of drives to reserve for the virtual hot spare, from 0-4.


    virtual_hot_spare_limit_percent (, int, )
      The percent space to reserve for the virtual hot spare, from 0-20.







Status
------





Authors
~~~~~~~

- Meenakshi Dembi (@dembim) <ansible.team@dell.com>

