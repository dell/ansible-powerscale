.. _nfs_zone_settings_module:


nfs_zone_settings -- Manage NFS zone settings on a PowerScale Storage System
============================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Managing NFS zone settings on an PowerScale system includes retrieving details and modifying NFS zone settings.



Requirements
------------
The below requirements are needed on the host that executes this module.

- A Dell PowerScale Storage system.
- Ansible-core 2.14 or later.
- Python 3.9, 3.10 or 3.11.



Parameters
----------

  access_zone (optional, str, System)
    Specifies the access zone in which the NFS zone settings apply.


  nfsv4_allow_numeric_ids (optional, bool, None)
    If ``true``, send owner and groups as UIDs and GIDs when look up fails or *nfsv4_no_names* is set ``rue``.


  nfsv4_domain (optional, str, None)
    Specifies the domain through which users and groups are associated.


  nfsv4_no_domain (optional, bool, None)
    If ``true``, sends owners and groups without a domain name.


  nfsv4_no_domain_uids (optional, bool, None)
    If ``true``, sends UIDs and GIDs without a domain name.


  nfsv4_no_names (optional, bool, None)
    If ``true``, sends owners and groups as UIDs and GIDs.


  nfsv4_replace_domain (optional, bool, None)
    If ``true``, replaces the owner or group domain with an NFS domain name.


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
   - The *check_mode* is supported.
   - The modules present in this collection named as 'dellemc.powerscale' are built to support the Dell PowerScale storage platform.




Examples
--------

.. code-block:: yaml+jinja

    
    - name: Get NFS zone settings
      dellemc.powerscale.nfs_zone_settings:
        onefs_host: "{{onefs_host}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        verify_ssl: "{{verify_ssl}}"
        access_zone: "sample-zone"

    - name: Modify NFS zone settings
      dellemc.powerscale.nfs_zone_settings:
        onefs_host: "{{onefs_host}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        verify_ssl: "{{verify_ssl}}"
        access_zone: "sample-zone"
        nfsv4_allow_numeric_ids: true
        nfsv4_domain: "example.com"
        nfsv4_no_domain: true
        nfsv4_no_domain_uids: false



Return Values
-------------

changed (always, bool, false)
  A boolean indicating if the task had to make changes.


nfs_zone_settings_details (always, dict, {'nfsv4_allow_numeric_ids': False, 'nfsv4_domain': '', 'nfsv4_no_domain': False, 'nfsv4_no_domain_uids': False, 'nfsv4_no_names': False, 'nfsv4_replace_domain': False, 'zone': 'System'})
  The NFS zone settings details.


  nfsv4_allow_numeric_ids (, bool, )
    If ``true``, sends owners and groups as UIDs and GIDs when look up fails or if the *nfsv4_no_names* property is set to 1.


  nfsv4_domain (, str, )
    Specifies the domain through which users and groups are associated.


  nfsv4_no_domain (, bool, )
    If ``true``, sends owners and groups without a domain name.


  nfsv4_no_domain_uids (, bool, )
    If ``true``, sends UIDs and GIDs without a domain name.


  nfsv4_no_names (, bool, )
    If ``true``, sends owners and groups as UIDs and GIDs.


  nfsv4_replace_domain (, bool, )
    If ``true``, replaces the owner or group domain with an NFS domain name.


  zone (, str, )
    Specifies the access zone in which the NFS zone settings apply.






Status
------





Authors
~~~~~~~

- Bhavneet Sharma(@Bhavneet-Sharma) <ansible.team@dell.com>

