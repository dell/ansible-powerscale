.. _synciqcertificate_module:


synciqcertificate -- Manage SyncIQ target cluster certificate on a PowerScale Storage System
============================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Managing SyncIQ target cluster certificate on an PowerScale system includes getting, importing, modifying and deleting target cluster certificates.



Requirements
------------
The below requirements are needed on the host that executes this module.

- A Dell PowerScale Storage system.
- Ansible-core 2.15 or later.
- Python 3.10, 3.11 or 3.12.



Parameters
----------

  certificate_file (optional, str, None)
    Certificate file path.


  alias_name (optional, str, None)
    Alias name for the certificate.


  description (optional, str, None)
    Description of the certificate.

    Map users to a specific user and/or group ID after a failed auth attempt.


  certificate_id (optional, str, None)
    ID assigned by the system to certificate.

    This parameter does not affect server behavior, but is included to accommodate legacy client requirements.


  new_alias_name (optional, str, None)
    Alias name for the certificate in case of modify operation.


  state (optional, str, present)
    The state option is used to mention the existence of SyncIQ certificate.


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

    
    - name: Import SyncIQ certificate
      dellemc.powerscale.synciqcertificate:
        onefs_host: "{{ onefs_host }}"
        verify_ssl: "{{ verify_ssl }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"
        certificate_file: "/ifs/server.crt"
        description: "From python"
        alias_name: "Test_1"
        state: 'present'

    - name: Get SyncIQ certificate details
      dellemc.powerscale.synciqcertificate:
        onefs_host: "{{ onefs_host }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"
        verify_ssl: "{{ verify_ssl }}"
        certificate_id: "a851d9f3d7b16985be6fcb0402"
        state: "present"

    - name: Modify SyncIQ certificate details
      dellemc.powerscale.synciqcertificate:
        onefs_host: "{{ onefs_host }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"
        verify_ssl: "{{ verify_ssl }}"
        certificate_id: "a851d9f3d7b16985be6fcb0402"
        description: "test description"
        alias_name: "Modify_alias_name"
        state: "present"

    - name: Delete SyncIQ certificate details
      dellemc.powerscale.synciqcertificate:
        onefs_host: "{{ onefs_host }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"
        verify_ssl: "{{ verify_ssl }}"
        certificate_id: "a851d9f3d7b16985be6fcb0402"
        state: "absent"



Return Values
-------------

changed (always, bool, false)
  A boolean indicating if the task had to make changes.


synciq_certificate_details (always, dict, {'description': 'SyncIQ Certificate details', 'fingerprints': [{'type': 'SHA1', 'value': 'xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:5e:xx:xx:xx:xx:xx:xx:xx:xx'}, {'type': 'SHA256', 'value': 'xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:5e:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:'}], 'id': '479891a2b14eb6204b1b9975573fda0fea92cfa851d9f3d7b16985be6fcb0402', 'issuer': 'C=AU, ST=Some-State, O=Internet Widgits Pty Ltd', 'name': 'Test_1_modify', 'not_after': 1753465054, 'not_before': 1690393054, 'status': 'valid', 'subject': 'C=AU, ST=Some-State, O=Internet Widgits Pty Ltd'})
  The synciq certificate details.


  description (, str, )
    Description of the certificate.


  fingerprints (, list, )
    Fingerprint details of the certificate.


  id (, str, )
    System assigned certificate id.


  issuer (, str, )
    Name of the certificate issuer.


  name (, str, )
    Name for the certificate.


  not_after (, str, )
    Specifies the preferred size for directory read operations. This value is used to advise the client of optimal settings for the server, but is not enforced.


  not_before (, str, )
    Validity date of the certificate.


  status (, str, )
    Specifies the validity of the certificate.


  subject (, str, )
    Validity date of the certificate.






Status
------





Authors
~~~~~~~

- Meenakshi Dembi(@dembim) <ansible.team@dell.com>

