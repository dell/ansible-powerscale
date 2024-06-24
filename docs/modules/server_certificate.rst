.. _server_certificate_module:


server_certificate -- Manage server certificates on a PowerScale Storage System
===============================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Manage server certificates on a PowerScale Storage System includes import, update, set certificate to default, and delete server certificates.



Requirements
------------
The below requirements are needed on the host that executes this module.

- A Dell PowerScale Storage system.
- Ansible-core 2.15 or later.
- Python 3.10, 3.11 or 3.12.



Parameters
----------

  state (optional, str, present)
    The state option is used to mention the existence of server certificate.


  alias_name (optional, str, None)
    The name of the certificate.

    *alias_name* is mutually exclusive with *certificate_id*.

    The maximum length for *alias_name* is 128.


  description (optional, str, None)
    The description of the certificate.

    The maximum length for *description* is 2048.

    Setting an empty value is necessary to remove the certificate description.


  new_alias_name (optional, str, None)
    The *alias_name* of the certificate.

    The maximum length for *new_alias_name* is 128.


  certificate_id (optional, str, None)
    The ID of the imported certificate.

    *certificate_id* is mutually exclusive with *alias_name*.


  certificate_path (optional, path, None)
    The path of the certificate file.


  certificate_key_path (optional, path, None)
    The path of the certificate key file.


  certificate_key_password (optional, str, None)
    The password of the certificate key.

    The maximum length for *certificate_key_password* is 256.


  is_default_certificate (optional, bool, False)
    To set the certificate as the default.

    If the ``True`` is selected, the server certificate is set to default.

    Another certificate must be selected as default to designate a certificate as non-default.


  certificate_monitor_enabled (optional, bool, None)
    Boolean value indicating whether certificate expiration monitoring is enabled.

    This option is applicable if *is_default_certificate* is ``True``.


  certificate_pre_expiration_threshold (optional, int, None)
    The number of seconds before certificate expiration that the certificate expiration monitor will start raising alerts.

    The range for this value is from 0 to 4294967295.

    This option is applicable if *is_default_certificate* is ``True``.


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
   - The *check_mode* and idempotency is not supported for *certificate_path*, *certificate_key_path*, and *certificate_key_password* when updating certificates.
   - The modules present in this collection named as 'dellemc.powerscale' are built to support the Dell PowerScale storage platform.




Examples
--------

.. code-block:: yaml+jinja

    
    - name: To import the new server certificate
      dellemc.powerscale.server_certificate:
        onefs_host: "{{ onefs_host }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"
        verify_ssl: "{{ verify_ssl }}"
        state: present
        alias_name: certificate_name
        description: The certificate description
        certificate_path: "/ifs/certificates/server.crt"
        certificate_key_path: "/ifs/certificates/server.key"
        certificate_key_password: "Secret@123"

    - name: To import the new server certificate and set the certificate as default
      dellemc.powerscale.server_certificate:
        onefs_host: "{{ onefs_host }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"
        verify_ssl: "{{ verify_ssl }}"
        state: present
        alias_name: default_certificate
        description: The default certificate description
        certificate_path: "/ifs/certificates/server.crt"
        certificate_key_path: "/ifs/certificates/server.key"
        certificate_key_password: "Secret@123"
        is_default_certificate: true
        certificate_monitor_enabled: true
        certificate_pre_expiration_threshold: 300

    - name: To update the server certificate
      dellemc.powerscale.server_certificate:
        onefs_host: "{{ onefs_host }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"
        verify_ssl: "{{ verify_ssl }}"
        state: present
        alias_name: certificate_new_name
        description: The updated certificate description

    - name: To update the server certificate and set the certificate as default
      dellemc.powerscale.server_certificate:
        onefs_host: "{{ onefs_host }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"
        verify_ssl: "{{ verify_ssl }}"
        state: present
        certificate_id: "a851d9f3d7b16985be6fcb0402"
        description: The updated certificate description
        is_default_certificate: true
        certificate_monitor_enabled: true
        certificate_pre_expiration_threshold: 42949

    - name: To delete the server certificate
      dellemc.powerscale.server_certificate:
        onefs_host: "{{ onefs_host }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"
        verify_ssl: "{{ verify_ssl }}"
        state: absent
        alias_name: certificate_new_name

    - name: To delete the server certificate using certificate ID
      dellemc.powerscale.server_certificate:
        onefs_host: "{{ onefs_host }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"
        verify_ssl: "{{ verify_ssl }}"
        state: absent
        certificate_id: "a851d9f3d7b16985be6fcb0402"



Return Values
-------------

changed (always, bool, false)
  A boolean indicating if the task had to make changes.


certificate_details (always, dict, {'certificate_monitor_enabled': True, 'certificate_pre_expiration_threshold': 4294, 'description': 'This the example test description', 'dnsnames': ['powerscale'], 'fingerprints': [{'type': 'SHA1', 'value': '68:b2:d5:5d:cc:b0:70:f1:f0:39:3a:bb:e0:44:49:70:6e:05:c3:ed'}, {'type': 'SHA256', 'value': '69:99:b9:c0:29:49:c9:62:e8:4b:60:05:60:a8:fa:f0:01:ab:24:43:8a:47:4c:2f:66:2c:95:a1:7c:d8:10:34'}], 'id': '6999b9c02949c962e84b600560a8faf001ab24438a474c2f662c95a17cd81034', 'issuer': 'C=IN, ST=Karnataka, L=Bangalore, O=Dell, OU=ISG, CN=powerscale, emailAddress=contact@dell.com', 'name': 'test', 'not_after': 1769586969, 'not_before': 1706514969, 'status': 'valid', 'subject': 'C=IN, ST=Karnataka, L=Bangalore, O=Dell, OU=ISG, CN=powerscale, emailAddress=contact@dell.com'})
  The server certificate details.


  description (, str, )
    Description of the certificate.


  id (, str, )
    System assigned certificate id.


  issuer (, str, )
    Name of the certificate issuer.


  name (, str, )
    Name for the certificate.


  not_after (, str, )
    The date and time from which the certificate becomes valid and can be used for authentication and encryption.


  not_before (, str, )
    The date and time until which the certificate is valid and can be used for authentication and encryption.


  status (, str, )
    Status of the certificate.


  fingerprints (, str, )
    Fingerprint details of the certificate.


  dnsnames (, list, )
    Subject alternative names of the certificate.


  subject (, str, )
    Subject of the certificate.


  certificate_monitor_enabled (, bool, )
    Boolean value indicating whether certificate expiration monitoring is enabled.


  certificate_pre_expiration_threshold (, int, )
    The number of seconds before certificate expiration that the certificate expiration monitor will start raising alerts.






Status
------





Authors
~~~~~~~

- Felix Stephen (@felixs88) <ansible.team@dell.com>

