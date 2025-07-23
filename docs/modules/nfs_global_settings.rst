.. _nfs_global_settings_module:


nfs_global_settings -- Manage NFS global settings on a PowerScale Storage System
================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Managing NFS global settings on an PowerScale system includes retrieving details of NFS global settings and modifying NFS global settings.



Requirements
------------
The below requirements are needed on the host that executes this module.

- A Dell PowerScale Storage system.
- Ansible-core 2.17 or later.
- Python 3.11, 3.12 or 3.13.



Parameters
----------

  service (optional, bool, None)
    Specifies if the NFS service needs to be enabled or not.


  rpc_maxthreads (optional, int, None)
    Specifies the maximum number of threads in the nfsd thread pool.


  rpc_minthreads (optional, int, None)
    Specifies the minimum number of threads in the nfsd thread pool.


  rquota_enabled (optional, bool, None)
    Enable/Disable the rquota protocol.


  nfs_rdma_enabled (optional, bool, None)
    Enables or disables RDMA for NFS.

    Supported on PowerScale 9.8 and later.


  nfsv3 (optional, dict, None)
    Enable/disable NFSv3 protocol.


    nfsv3_enabled (optional, bool, None)
      Enable/disable NFSv3 protocol.


    nfsv3_rdma_enabled (optional, bool, None)
      To enable/disable RDMA for NFSv3 protocol.

      For PowerScale 9.8 :emphasis:`nfsv3\_rdma\_enabled` is not supported and :emphasis:`nfs\_rdma\_enabled` is used for both nfsv3 and nfsv4.



  nfsv4 (optional, dict, None)
    Specifies the minor versions of NFSv4 protocol.


    nfsv4_enabled (optional, bool, None)
      Enable/disable all minor versions of NFSv4 protocol.


    nfsv40_enabled (optional, bool, None)
      Enable/disable minor version 0 of NFSv4 protocol.


    nfsv41_enabled (optional, bool, None)
      Enable/disable minor version 1 of NFSv4 protocol.


    nfsv42_enabled (optional, bool, None)
      Enable/disable minor version 2 of NFSv4 protocol.



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

    
    - name: Get NFS global settings
      dellemc.powerscale.nfs_global_settings:
        onefs_host: "{{ onefs_host }}"
        port_no: "{{ port_no }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"
        verify_ssl: "{{ verify_ssl }}"

    - name: Update service of NFS global settings
      dellemc.powerscale.nfs_global_settings:
        onefs_host: "{{ onefs_host }}"
        port_no: "{{ port_no }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"
        verify_ssl: "{{ verify_ssl }}"
        service: true
        nfsv3:
          nfsv3_enabled: false
        nfsv4:
          nfsv40_enabled: true
          nfsv41_enabled: true
          nfsv42_enabled: false
        nfs_rdma_enabled: true
        rpc_minthreads: 17
        rpc_maxthreads: 20
        rquota_enabled: true



Return Values
-------------

changed (always, bool, false)
  A boolean indicating if the task had to make changes.


nfs_global_settings_details (always, complex, {'nfsv3_enabled': False, 'nfsv3_rdma_enabled': True, 'nfsv40_enabled': True, 'nfsv41_enabled': True, 'nfsv42_enabled': False, 'nfsv4_enabled': True, 'rpc_maxthreads': 20, 'rpc_minthreads': 17, 'rquota_enabled': True, 'service': True})
  The updated nfs global settings details.


  nfsv3_enabled (, bool, )
    Whether NFSv3 protocol is enabled/disabled.


  nfsv3_rdma_enabled (, bool, )
    Whether rdma is enabled for NFSv3 protocol.


  nfsv40_enabled (, bool, )
    Whether version 0 of NFSv4 protocol is enabled/disabled.


  nfsv41_enabled (, bool, )
    Whether version 1 of NFSv4 protocol is enabled/disabled.


  nfsv42_enabled (, bool, )
    Whether version 2 of NFSv4 protocol is enabled/disabled.


  nfsv4_enabled (, bool, )
    Whether NFSv4 protocol is enabled/disabled.


  rpc_maxthreads (, int, )
    Specifies the maximum number of threads in the nfsd thread pool.


  rpc_minhreads (, int, )
    Specifies the minimum number of threads in the nfsd thread pool.


  rquota_enabled (, bool, )
    Whether the rquota protocol is enabled/disabled.


  service (, bool, )
    Whether the NFS service is enabled/disabled.






Status
------





Authors
~~~~~~~

- Trisha Datta (@trisha-dell) <ansible.team@dell.com>

