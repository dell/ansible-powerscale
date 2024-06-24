.. _synciq_global_settings_module:


synciq_global_settings -- Manage SyncIQ global settings on a PowerScale Storage System
======================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Managing SyncIQ global settings on an PowerScale system includes retrieving details of SyncIQ global settings and modifying SyncIQ global settings.



Requirements
------------
The below requirements are needed on the host that executes this module.

- A Dell PowerScale Storage system.
- Ansible-core 2.15 or later.
- Python 3.10, 3.11 or 3.12.



Parameters
----------

  service (optional, str, on)
    Specifies if the SyncIQ service currently ``on``, ``paused``, or ``off``.

    If ``paused``, all sync jobs will be paused. If turned ``off``, all jobs will be canceled.


  encryption_required (optional, bool, False)
    If true, requires all SyncIQ policies to utilize encrypted communications.


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

    
    - name: Get SyncIQ global settings
      dellemc.powerscale.synciq_global_settings:
        onefs_host: "{{ onefs_host }}"
        port_no: "{{ port_no }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"
        verify_ssl: "{{ verify_ssl }}"

    - name: Update service of SyncIQ global settings
      dellemc.powerscale.synciq_global_settings:
        onefs_host: "{{ onefs_host }}"
        port_no: "{{ port_no }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"
        verify_ssl: "{{ verify_ssl }}"
        service: "on"
        encryption_required: true



Return Values
-------------

changed (always, bool, false)
  A boolean indicating if the task had to make changes.


synciq_global_settings (always, dict, {'bandwidth_reservation_reserve_absolute': None, 'bandwidth_reservation_reserve_percentage': 1, 'cluster_certificate_id': 'xxxx', 'encryption_cipher_list': '', 'encryption_required': True, 'force_interface': False, 'max_concurrent_jobs': 16, 'ocsp_address': '', 'ocsp_issuer_certificate_id': '', 'preferred_rpo_alert': 0, 'renegotiation_period': 28800, 'report_email': [], 'report_max_age': 31536000, 'report_max_count': 2000, 'restrict_target_network': False, 'rpo_alerts': True, 'service': 'off', 'service_history_max_age': 31536000, 'service_history_max_count': 2000, 'source_network': None, 'tw_chkpt_interval': None, 'use_workers_per_node': False})
  The SyncIQ global settings details.


  bandwidth_reservation_reserve_absolute (, int, )
    The absolute bandwidth reservation for SyncIQ.


  bandwidth_reservation_reserve_percentage (, int, )
    The percentage-based bandwidth reservation for SyncIQ.


  cluster_certificate_id (, str, )
    The ID of the cluster certificate used for SyncIQ.


  encryption_cipher_list (, str, )
    The list of encryption ciphers used for SyncIQ.


  encryption_required (, bool, )
    Whether encryption is required or not for SyncIQ.


  force_interface (, bool, )
    Whether the force interface is enabled or not for SyncIQ.


  max_concurrent_jobs (, int, )
    The maximum number of concurrent jobs for SyncIQ.


  ocsp_address (, str, )
    The address of the OCSP server used for SyncIQ certificate validation.


  ocsp_issuer_certificate_id (, str, )
    The ID of the issuer certificate used for OCSP validation in SyncIQ.


  preferred_rpo_alert (, bool, )
    Whether the preferred RPO alert is enabled or not for SyncIQ.


  renegotiation_period (, int, )
    The renegotiation period in seconds for SyncIQ.


  report_email (, str, )
    The email address to which SyncIQ reports are sent.


  report_max_age (, int, )
    The maximum age in days of reports that are retained by SyncIQ.


  report_max_count (, int, )
    The maximum number of reports that are retained by SyncIQ.


  restrict_target_network (, bool, )
    Whether to restrict the target network in SyncIQ.


  rpo_alerts (, bool, )
    Whether RPO alerts are enabled or not in SyncIQ.


  service (, str, )
    Specifies whether the SyncIQ service is currently on, off, or paused.


  service_history_max_age (, int, )
    The maximum age in days of service history that is retained by SyncIQ.


  service_history_max_count (, int, )
    The maximum number of service history records that are retained by SyncIQ.


  source_network (, str, )
    The source network used by SyncIQ.


  tw_chkpt_interval (, int, )
    The interval between checkpoints in seconds in SyncIQ.


  use_workers_per_node (, bool, )
    Whether to use workers per node in SyncIQ or not.






Status
------





Authors
~~~~~~~

- Pavan Mudunuri(@Pavan-Mudunuri) <ansible.team@dell.com>

