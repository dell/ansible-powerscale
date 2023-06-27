.. _smartquota_module:


smartquota -- Manage Smart Quotas on PowerScale
===============================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Manages Smart Quotas on a PowerScale storage system. This includes getting details, modifying, creating and deleting Smart Quotas.



Requirements
------------
The below requirements are needed on the host that executes this module.

- A Dell PowerScale Storage system.
- Ansible-core 2.13 or later.
- Python 3.9, 3.10 or 3.11.



Parameters
----------

  path (True, str, None)
    The path on which the quota will be imposed.

    For system access zone, the path is absolute. For all other access zones, the path is a relative path from the base of the access zone.


  quota_type (True, str, None)
    The type of quota which will be imposed on the path.


  user_name (optional, str, None)
    The name of the user account for which quota operations will be performed.


  group_name (optional, str, None)
    The name of the group for which quota operations will be performed.


  access_zone (optional, str, system)
    This option mentions the zone in which the user/group exists.

    For a non-system access zone, the path relative to the non-system Access Zone's base directory has to be given.

    For a system access zone, the absolute path has to be given.


  provider_type (optional, str, local)
    This option defines the type which is used to authenticate the user/group.

    If the *provider_type* is 'ads' then the domain name of the Active Directory Server has to be mentioned in the *user_name*. The format for the *user_name* should be 'DOMAIN_NAME\user_name' or "DOMAIN_NAME\\user_name".

    This option acts as a filter for all operations except creation.


  quota (optional, dict, None)
    Specifies Smart Quota parameters.


    include_snapshots (optional, bool, False)
      Whether to include the snapshots in the quota or not.


    include_overheads (optional, bool, None)
      Whether to include the data protection overheads in the quota or not.

      If not passed during quota creation then quota will be created excluding the overheads.

      This parameter is supported for SDK 8.1.1


    thresholds_on (optional, str, None)
      For SDK 9.0.0 the parameter *include_overheads* is deprecated and *thresholds_on* is used.


    advisory_limit_size (optional, float, None)
      The threshold value after which the advisory notification will be sent.


    soft_limit_size (optional, float, None)
      Threshold value after which the soft limit exceeded notification will be sent and the *soft_grace* period will start.

      Write access will be restricted after the grace period expires.

      Both *soft_grace_period* and *soft_limit_size* are required to modify soft threshold for the quota.


    soft_grace_period (optional, int, None)
      Grace Period after the soft limit for quota is exceeded.

      After the grace period, the write access to the quota will be restricted.

      Both *soft_grace_period* and *soft_limit_size* are required to modify soft threshold for the quota.


    period_unit (optional, str, None)
      Unit of the time period for *soft_grace_period*.

      For months the number of days is assumed to be 30 days.

      This parameter is required only if the *soft_grace_period*, is specified.


    hard_limit_size (optional, float, None)
      Threshold value after which a hard limit exceeded notification will be sent.

      Write access will be restricted after the hard limit is exceeded.


    cap_unit (optional, str, None)
      Unit of storage for the hard, soft and advisory limits.

      This parameter is required if any of the hard, soft or advisory limits is specified.


    container (optional, bool, False)
      If ``true``, SMB shares using the quota directory see the quota thresholds as share size.



  state (True, str, None)
    Define whether the Smart Quota should exist or not.

    ``present`` - indicates that the Smart Quota should exist on the system.

    ``absent`` - indicates that the Smart Quota should not exist on the system.


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
   - To perform any operation, path, quota_type and state are mandatory parameters.
   - There can be two quotas for each type per directory, one with snapshots included and one without snapshots included.
   - Once the limits are assigned, then the quota cannot be converted to accounting. Only modification to the threshold limits is permitted.
   - The *check_mode* is not supported.
   - The modules present in this collection named as 'dellemc.powerscale' are built to support the Dell PowerScale storage platform.




Examples
--------

.. code-block:: yaml+jinja

    
      - name: Create a Quota for a User excluding snapshot
        dellemc.powerscale.smartquota:
          onefs_host: "{{onefs_host}}"
          verify_ssl: "{{verify_ssl}}"
          api_user: "{{api_user}}"
          api_password: "{{api_password}}"
          path: "<path>"
          quota_type: "user"
          user_name: "{{user_name}}"
          access_zone: "sample-zone"
          provider_type: "local"
          quota:
            include_overheads: false
            advisory_limit_size: "{{advisory_limit_size}}"
            soft_limit_size: "{{soft_limit_size}}"
            soft_grace_period: "{{soft_grace_period}}"
            period_unit: "{{period_unit}}"
            hard_limit_size: "{{hard_limit_size}}"
            cap_unit: "{{cap_unit}}"
          state: "present"

      - name: Create a Quota for a Directory for accounting includes snapshots and data protection overheads
        dellemc.powerscale.smartquota:
          onefs_host: "{{onefs_host}}"
          verify_ssl: "{{verify_ssl}}"
          api_user: "{{api_user}}"
          api_password: "{{api_password}}"
          path: "<path>"
          quota_type: "directory"
          quota:
            include_snapshots: true
            include_overheads: true
          state: "present"

      - name: Create default-user Quota for a Directory with snaps and overheads
        dellemc.powerscale.smartquota:
          onefs_host: "{{onefs_host}}"
          verify_ssl: "{{verify_ssl}}"
          api_user: "{{api_user}}"
          api_password: "{{api_password}}"
          path: "<path>"
          quota_type: "default-user"
          quota:
            include_snapshots: true
            include_overheads: true
          state: "present"

      - name: Get a Quota Details for a Group
        dellemc.powerscale.smartquota:
          onefs_host: "{{onefs_host}}"
          verify_ssl: "{{verify_ssl}}"
          api_user: "{{api_user}}"
          api_password: "{{api_password}}"
          path: "<path>"
          quota_type: "group"
          group_name: "{{user_name}}"
          access_zone: "sample-zone"
          provider_type: "local"
          quota:
            include_snapshots: true
          state: "present"

      - name: Update Quota for a User
        dellemc.powerscale.smartquota:
          onefs_host: "{{onefs_host}}"
          verify_ssl: "{{verify_ssl}}"
          api_user: "{{api_user}}"
          api_password: "{{api_password}}"
          path: "<path>"
          quota_type: "user"
          user_name: "{{user_name}}"
          access_zone: "sample-zone"
          provider_type: "local"
          quota:
            include_snapshots: true
            include_overheads: true
            advisory_limit_size: "{{new_advisory_limit_size}}"
            hard_limit_size: "{{new_hard_limit_size}}"
            cap_unit: "{{cap_unit}}"
          state: "present"

      - name: Modify Soft Limit and Grace period of default-user Quota
        dellemc.powerscale.smartquota:
          onefs_host: "{{onefs_host}}"
          verify_ssl: "{{verify_ssl}}"
          api_user: "{{api_user}}"
          api_password: "{{api_password}}"
          path: "<path>"
          quota_type: "default-user"
          access_zone: "sample-zone"
          quota:
            include_snapshots: true
            include_overheads: true
            soft_limit_size: "{{soft_limit_size}}"
            cap_unit: "{{cap_unit}}"
            soft_grace_period: "{{soft_grace_period}}"
            period_unit: "{{period_unit}}"
          state: "present"

      - name: Delete a Quota for a Directory
        dellemc.powerscale.smartquota:
          onefs_host: "{{onefs_host}}"
          verify_ssl: "{{verify_ssl}}"
          api_user: "{{api_user}}"
          api_password: "{{api_password}}"
          path: "<path>"
          quota_type: "directory"
          quota:
            include_snapshots: true
          state: "absent"

      - name: Delete Quota for a default-group
        dellemc.powerscale.smartquota:
          onefs_host: "{{onefs_host}}"
          verify_ssl: "{{verify_ssl}}"
          api_user: "{{api_user}}"
          api_password: "{{api_password}}"
          path: "<path>"
          quota_type: "default-group"
          quota:
            include_snapshots: true
          state: "absent"



Return Values
-------------

changed (always, bool, True)
  Whether or not the resource has changed.


quota_details (When Quota exists., complex, )
  The quota details.


  id (, str, 2nQKAAEAAAAAAAAAAAAAQIMCAAAAAAAA)
    The ID of the Quota.


  enforced (, bool, True)
    Whether the limits are enforced on Quota or not.


  container (, bool, True)
    If ``true``, SMB shares using the quota directory see the quota thresholds as share size.


  thresholds (, dict, {'advisory': 3221225472, 'advisory(GB)': '3.0', 'advisory_exceeded': False, 'advisory_last_exceeded': 0, 'hard': 6442450944, 'hard(GB)': '6.0', 'hard_exceeded': False, 'hard_last_exceeded': 0, 'soft': 5368709120, 'soft(GB)': '5.0', 'soft_exceeded': False, 'soft_grace': 3024000, 'soft_last_exceeded': 0})
    Includes information about all the limits imposed on quota. The limits are mentioned in bytes and *soft_grace* is in seconds.


  type (, str, directory)
    The type of Quota.


  usage (, dict, {'inodes': 1, 'logical': 0, 'physical': 2048})
    The Quota usage.






Status
------





Authors
~~~~~~~

- P Srinivas Rao (@srinivas-rao5) <ansible.team@dell.com>

