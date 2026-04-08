.. _cluster_services_module:


cluster_services -- Manage cluster services on a PowerScale Storage System
==========================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Managing cluster services on a PowerScale system includes enabling or disabling NFS, SMB, S3, HDFS, and Antivirus services, and retrieving the current status of all cluster services.

When no service parameters are provided, the module retrieves the current state of all services (facts gathering).



Requirements
------------
The below requirements are needed on the host that executes this module.

- A Dell PowerScale Storage system.
- Ansible\-core 2.17 or later.
- Python 3.11, 3.12 or 3.13.



Parameters
----------

  nfs_service (optional, bool, None)
    Specifies if the NFS service should be enabled or disabled.

    When set to :literal:`true`\ , the NFS service is enabled.

    When set to :literal:`false`\ , the NFS service is disabled.


  smb_service (optional, bool, None)
    Specifies if the SMB service should be enabled or disabled.

    When set to :literal:`true`\ , the SMB service is enabled.

    When set to :literal:`false`\ , the SMB service is disabled.


  s3_service (optional, bool, None)
    Specifies if the S3 service should be enabled or disabled.

    When set to :literal:`true`\ , the S3 service is enabled.

    When set to :literal:`false`\ , the S3 service is disabled.


  hdfs_service (optional, bool, None)
    Specifies if the HDFS service should be enabled or disabled.

    When set to :literal:`true`\ , the HDFS service is enabled.

    When set to :literal:`false`\ , the HDFS service is disabled.


  antivirus_service (optional, bool, None)
    Specifies if the Antivirus service should be enabled or disabled.

    When set to :literal:`true`\ , the Antivirus service is enabled.

    When set to :literal:`false`\ , the Antivirus service is disabled.


  onefs_host (True, str, None)
    IP address or FQDN of the PowerScale cluster.


  port_no (False, str, 8080)
    Port number of the PowerScale cluster.It defaults to 8080 if not specified.


  verify_ssl (True, bool, None)
    boolean variable to specify whether to validate SSL certificate or not.

    :literal:`true` \- indicates that the SSL certificate should be verified.

    :literal:`false` \- indicates that the SSL certificate should not be verified.


  api_user (True, str, None)
    username of the PowerScale cluster.


  api_password (True, str, None)
    the password of the PowerScale cluster.





Notes
-----

.. note::
   - The :emphasis:`check\_mode` is supported.
   - The :emphasis:`diff\_mode` is supported.
   - The modules present in this collection named as 'dellemc.powerscale' are built to support the Dell PowerScale storage platform.




Examples
--------

.. code-block:: yaml+jinja

    
    - name: Get cluster services status (facts gathering)
      dellemc.powerscale.cluster_services:
        onefs_host: "{{ onefs_host }}"
        port_no: "{{ port_no }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"  # example
        verify_ssl: "{{ verify_ssl }}"

    - name: Enable NFS and S3 services, disable SMB service
      dellemc.powerscale.cluster_services:
        onefs_host: "{{ onefs_host }}"
        port_no: "{{ port_no }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"  # example
        verify_ssl: "{{ verify_ssl }}"
        nfs_service: true
        s3_service: true
        smb_service: false

    - name: Enable Antivirus service
      dellemc.powerscale.cluster_services:
        onefs_host: "{{ onefs_host }}"
        port_no: "{{ port_no }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"  # example
        verify_ssl: "{{ verify_ssl }}"
        antivirus_service: true



Return Values
-------------

changed (always, bool, false)
  A boolean indicating if the task had to make changes.


cluster_services_details (always, dict, {'nfs_service': True, 'smb_service': True, 's3_service': False, 'hdfs_service': False, 'antivirus_service': True})
  The cluster services details.


  nfs_service (, bool, )
    Whether the NFS service is enabled.


  smb_service (, bool, )
    Whether the SMB service is enabled.


  s3_service (, bool, )
    Whether the S3 service is enabled.


  hdfs_service (, bool, )
    Whether the HDFS service is enabled.


  antivirus_service (, bool, )
    Whether the Antivirus service is enabled.






Status
------





Authors
~~~~~~~

- Saksham Nautiyal (@Saksham-Nautiyal) <ansible.team@dell.com>

