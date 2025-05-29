.. _smb_global_settings_module:


smb_global_settings -- Manage SMB global settings on a PowerScale Storage System
================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Managing SMB global settings on a PowerScale system includes retrieving details of SMB global settings and modifying SMB global settings.



Requirements
------------
The below requirements are needed on the host that executes this module.

- A Dell PowerScale Storage system.
- Ansible-core 2.16 or later.
- Python 3.10, 3.11 or 3.12.



Parameters
----------

  access_based_share_enum (optional, bool, None)
    Only enumerate files and folders the requesting user has access to.


  dot_snap_accessible_child (optional, bool, None)
    Allow access to .snapshot directories in share subdirectories.


  dot_snap_accessible_root (optional, bool, None)
    Allow access to the .snapshot directory in the root of the share.


  dot_snap_visible_child (optional, bool, None)
    Show .snapshot directories in share subdirectories.


  dot_snap_visible_root (optional, bool, None)
    Show the .snapshot directory in the root of a share.


  enable_security_signatures (optional, bool, None)
    Indicates whether the server supports signed SMB packets.


  guest_user (optional, str, None)
    Specifies the fully-qualified user to use for guest access.


  ignore_eas (optional, bool, None)
    Specify whether to ignore EAs on files.


  onefs_cpu_multiplier (optional, int, None)
    Specify the number of OneFS driver worker threads per CPU.


  onefs_num_workers (optional, int, None)
    Set the maximum number of OneFS driver worker threads.


  reject_unencrypted_access (optional, bool, None)
    If SMB3 encryption is enabled, reject unencrypted access from clients.


  require_security_signatures (optional, bool, None)
    Indicates whether the server requires signed SMB packets.


  server_side_copy (optional, bool, None)
    Enable Server Side Copy.


  server_string (optional, str, None)
    Provides a description of the server.


  service (optional, bool, None)
    Specify whether service is enabled.


  support_multichannel (optional, bool, None)
    Support multichannel.


  support_netbios (optional, bool, None)
    Support NetBIOS.


  support_smb2 (optional, bool, None)
    The support SMB2 attribute.


  support_smb3_encryption (optional, bool, None)
    Support the SMB3 encryption on the server.


  onefs_host (True, str, None)
    IP address or FQDN of the PowerScale cluster.


  port_no (False, str, 8080)
    Port number of the PowerScale cluster.It defaults to 8080 if not specified.


  verify_ssl (True, bool, None)
    boolean variable to specify whether to validate SSL certificate or not.

    \ :literal:`true`\  - indicates that the SSL certificate should be verified.

    \ :literal:`false`\  - indicates that the SSL certificate should not be verified.


  api_user (True, str, None)
    username of the PowerScale cluster.


  api_password (True, str, None)
    the password of the PowerScale cluster.





Notes
-----

.. note::
   - The \ :emphasis:`check\_mode`\  is supported.
   - The modules present in this collection named as 'dellemc.powerscale' are built to support the Dell PowerScale storage platform.




Examples
--------

.. code-block:: yaml+jinja

    
    - name: Get SMB global settings
      dellemc.powerscale.smb_global_settings:
        onefs_host: "{{ onefs_host }}"
        port_no: "{{ port_no }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"
        verify_ssl: "{{ verify_ssl }}"

    - name: Update SMB global settings
      dellemc.powerscale.smb_global_settings:
        onefs_host: "{{ onefs_host }}"
        port_no: "{{ port_no }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"
        verify_ssl: "{{ verify_ssl }}"
        access_based_share_enum: true
        dot_snap_accessible_child: true
        dot_snap_accessible_root: false
        dot_snap_visible_child: false
        dot_snap_visible_root: true
        enable_security_signatures: true
        guest_user: user
        ignore_eas: false
        onefs_cpu_multiplier: 2
        onefs_num_workers: 4
        reject_unencrypted_access: true
        require_security_signatures: true
        server_side_copy: true
        server_string: 'PowerScale Server'
        service: true
        support_multichannel: true
        support_netbios: true
        support_smb2: true
        support_smb3_encryption: true



Return Values
-------------

changed (always, bool, false)
  A boolean indicating if the task had to make changes.


smb_global_settings_details (always, dict, {'access_based_share_enum': False, 'audit_fileshare': None, 'audit_logon': None, 'dot_snap_accessible_child': True, 'dot_snap_accessible_root': True, 'dot_snap_visible_child': False, 'dot_snap_visible_root': True, 'enable_security_signatures': False, 'guest_user': 'nobody', 'ignore_eas': False, 'onefs_cpu_multiplier': 4, 'onefs_num_workers': 0, 'reject_unencrypted_access': False, 'require_security_signatures': False, 'server_side_copy': False, 'server_string': 'PowerScale Server', 'service': True, 'srv_cpu_multiplier': None, 'srv_num_workers': None, 'support_multichannel': True, 'support_netbios': False, 'support_smb2': True, 'support_smb3_encryption': True})
  The updated SMB global settings details.


  access_based_share_enum (, bool, )
    Only enumerate files and folders the requesting user has access to.


  audit_fileshare (, str, )
    Specify level of file share audit events to log.


  audit_logon (, str, )
    Specify the level of logon audit events to log.


  dot_snap_accessible_child (, bool, )
    Allow access to .snapshot directories in share subdirectories.


  dot_snap_accessible_root (, bool, )
    Allow access to the .snapshot directory in the root of the share.


  dot_snap_visible_child (, bool, )
    Show .snapshot directories in share subdirectories.


  dot_snap_visible_root (, bool, )
    Show the .snapshot directory in the root of a share.


  enable_security_signatures (, bool, )
    Indicates whether the server supports signed SMB packets.


  guest_user (, str, )
    Specifies the fully-qualified user to use for guest access.


  ignore_eas (, bool, )
    Specify whether to ignore EAs on files.


  onefs_cpu_multiplier (, int, )
    Specify the number of OneFS driver worker threads per CPU.


  onefs_num_workers (, int, )
    Set the maximum number of OneFS driver worker threads.


  reject_unencrypted_access (, bool, )
    If SMB3 encryption is enabled, reject unencrypted access from clients.


  require_security_signatures (, bool, )
    Indicates whether the server requires signed SMB packets.


  server_side_copy (, bool, )
    Enable Server Side Copy.


  server_string (, str, )
    Provides a description of the server.


  service (, bool, )
    Specify whether service is enabled.


  srv_cpu_multiplier (, int, )
    Specify the number of SRV service worker threads per CPU.


  srv_num_workers (, int, )
    Set the maximum number of SRV service worker threads.


  support_multichannel (, bool, )
    Support multichannel.


  support_netbios (, bool, )
    Support NetBIOS.


  support_smb2 (, bool, )
    The support SMB2 attribute.


  support_smb3_encryption (, bool, )
    Support the SMB3 encryption on the server.






Status
------





Authors
~~~~~~~

- Sachin Apagundi (@sachin-apa) <ansible.team@dell.com>

