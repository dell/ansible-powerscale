.. _s3_key_module:


s3_key -- Manage S3 Keys on a PowerScale Storage System
========================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Managing S3 Keys on an PowerScale system includes retrieving details of S3 keys, creating S3 keys and deleting S3 keys.



Requirements
------------
The below requirements are needed on the host that executes this module.

- A Dell PowerScale Storage system.
- Ansible-core 2.17 or later.
- Python 3.11, 3.12 or 3.13.



Parameters
----------

  user (True, str, None)
    Specifies the user that owns the S3 key.

    If users belongs to another provider domain, it should be mentioned along with domain name as "DOMAIN\_NAME\\\\username" or DOMAIN\_NAME\\username.


  generate_new_key (optional, str, if_not_present)
    Whether a new S3 key should be generated.

    Value :literal:`if_not_present` indicates that a new S3 key is only generated if there is no existing key.

    Value :literal:`always` indicates that a new S3 key is always generated, even if there is an existing key.


  existing_key_expiry_minutes (optional, int, 0)
    Duration in minutes for which old key should remain valid.


  access_zone (optional, str, System)
    Specifies the access zone in which the S3 bucket exists.

    Access zone once set cannot be changed.


  state (optional, str, present)
    Defines whether the S3 key should exist or not.

    Value :literal:`present` indicates that the S3 key should exist in system.

    Value :literal:`absent` indicates that the S3 key should not exist in system.


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
   - The modules present in this collection named as 'dellemc.powerscale' are built to support the Dell PowerScale storage platform.




Examples
--------

.. code-block:: yaml+jinja

    
    - name: Create S3 Key - Check_mode
      dellemc.powerscale.s3_key:
        onefs_host: "{{ onefs_host }}"
        port_no: "{{ port_no }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"
        verify_ssl: "{{ verify_ssl }}"
        access_zone: "{{ access_zone }}"
        user: "{{ user }}"
        state: "present"
      check_mode: true

    - name: Create S3 Key - if not present
      dellemc.powerscale.s3_key:
        onefs_host: "{{ onefs_host }}"
        port_no: "{{ port_no }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"
        verify_ssl: "{{ verify_ssl }}"
        access_zone: "{{ access_zone }}"
        user: "{{ user }}"
        state: "present"
        generate_new_key: "if_not_present"

    - name: Create S3 Key - even if already present
      dellemc.powerscale.s3_key:
        onefs_host: "{{ onefs_host }}"
        port_no: "{{ port_no }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"
        verify_ssl: "{{ verify_ssl }}"
        access_zone: "{{ access_zone }}"
        user: "{{ user }}"
        state: "present"
        generate_new_key: "always"

    - name: Create S3 Key - even if already present, expire old key after 30 min
      dellemc.powerscale.s3_key:
        onefs_host: "{{ onefs_host }}"
        port_no: "{{ port_no }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"
        verify_ssl: "{{ verify_ssl }}"
        access_zone: "{{ access_zone }}"
        user: "{{ user }}"
        state: "present"
        generate_new_key: "always"
        existing_key_expiry_minutes: 30

    - name: Delete S3 Key
      dellemc.powerscale.s3_key:
        onefs_host: "{{ onefs_host }}"
        port_no: "{{ port_no }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"
        verify_ssl: "{{ verify_ssl }}"
        access_zone: "{{ access_zone }}"
        user: "{{ user }}"
        state: "absent"



Return Values
-------------

changed (always, bool, false)
  A boolean indicating if the task had to make changes.


S3_key_details (always, complex, {'access_id': 'sample_user_accid', 'old_key_expiry': 1755783140, 'old_key_timestamp': 1755781594, 'old_secret_key': '****************************', 'secret_key': '1234567890asdfhjkl', 'secret_key_timestamp': 1755782540})
  The updated S3 Key details.


  access_id (, str, )
    S3 access id.


  secret_key (, str, )
    S3 secret key.


  secret_key_timestamp (, int, )
    Creation timestamp of S3 secret key.


  old_key_expiry (, int, )
    Expiry timestamp of old S3 key if existing.


  old_key_timestamp (, int, )
    Creation timestamp of old S3 key if existing.


  old_secret_key (, str, )
    Redacted old S3 key if existing.





Status
------





Authors
~~~~~~~

- Fabian B. (@fpfuetsch)
