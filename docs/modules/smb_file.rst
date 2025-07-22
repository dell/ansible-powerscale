.. _smb_file_module:


smb_file -- Manage SMB files on a PowerScale Storage System
===========================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Managing SMB files on a PowerScale Storage System includes getting details of all SMB open files and closing SMB files.



Requirements
------------
The below requirements are needed on the host that executes this module.

- A Dell PowerScale Storage system.
- Ansible-core 2.17 or later.
- Python 3.10, 3.11 or 3.12.



Parameters
----------

  file_id (optional, int, None)
    Unique id of SMB open file. Mutually exclusive with :emphasis:`file\_path`.


  file_path (optional, str, None)
    Path of SMB file. Mutually exclusive with :emphasis:`file\_id`.

    If file path is provided all the open file sessions in the path will be closed.


  state (optional, str, present)
    Defines the state of SMB file.

    :literal:`present` indicates that the SMB file should exist in system.

    :literal:`absent` indicates that the SMB file is closed in system.


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
   - The :emphasis:`check\_mode` is supported.
   - If :emphasis:`state` is :literal:`absent`\ , the file will be closed.
   - The modules present in this collection named as 'dellemc.powerscale' are built to support the Dell PowerScale storage platform.




Examples
--------

.. code-block:: yaml+jinja

    
    - name: Get list of SMB files of the PowerScale cluster
      dellemc.powerscale.smb_file:
        onefs_host: "{{onefs_host}}"
        verify_ssl: "{{verify_ssl}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        state: "present"

    - name: Close SMB file of the PowerScale cluster
      dellemc.powerscale.smb_file:
        onefs_host: "{{onefs_host}}"
        verify_ssl: "{{verify_ssl}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        file_id: xxx
        state: "absent"

    - name: Close smb file of the PowerScale cluster
      dellemc.powerscale.smb_file:
        onefs_host: "{{onefs_host}}"
        verify_ssl: "{{verify_ssl}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        file_path: "/ifs/ATest"
        state: "absent"



Return Values
-------------

changed (always, bool, false)
  A boolean indicating if the task had to make changes.


smb_file_details (always, dict, {'smb_file_details': [{'file': 'C:\\ifs', 'id': 1370, 'locks': 0, 'permissions': ['read'], 'user': 'admin'}]})
  The SMB file details.


  file (, str, C:\\ifs)
    Path of file within /ifs.


  id (, int, 950)
    The ID of the SMB open file.


  locks (, int, 3)
    The number of locks user holds on file.


  permissions (, list, ['read'])
    The user's permissions on file.


  user (, str, admin)
    User holding file open






Status
------





Authors
~~~~~~~

- Pavan Mudunuri(@Pavan-Mudunuri) <ansible.team@dell.com>

