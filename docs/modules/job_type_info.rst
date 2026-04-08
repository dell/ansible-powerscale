.. _job_type_info_module:


job_type_info -- Get Job Type information on a PowerScale Storage System
========================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Retrieving information about job types on a PowerScale storage system.

This module supports getting details of all job types or a specific job type by its ID.



Requirements
------------
The below requirements are needed on the host that executes this module.

- A Dell PowerScale Storage system.
- Ansible-core 2.17 or later.
- Python 3.11, 3.12 or 3.13.



Parameters
----------

  job_type_id (optional, str, None)
    The ID of a specific job type to retrieve.

    If specified, only that single job type is returned.


  include_hidden (optional, bool, False)
    Whether to include hidden job types in the listing.

    Defaults to :literal:`false`, which returns only visible job types.


  sort (optional, str, None)
    The field by which to sort the job type results.


  dir (optional, str, None)
    The sort direction.

    Valid choices are :literal:`ASC`, :literal:`DESC`.


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
   - This is a read-only info module and does not make any changes.
   - The :emphasis:`check\_mode` is supported.
   - The modules present in this collection named as 'dellemc.powerscale' are built to support the Dell PowerScale storage platform.




Examples
--------

.. code-block:: yaml+jinja

    
    - name: Get all visible job types
      dellemc.powerscale.job_type_info:
        onefs_host: "{{ onefs_host }}"
        port_no: "{{ port_no }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"
        verify_ssl: "{{ verify_ssl }}"

    - name: Get all job types including hidden
      dellemc.powerscale.job_type_info:
        onefs_host: "{{ onefs_host }}"
        port_no: "{{ port_no }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"
        verify_ssl: "{{ verify_ssl }}"
        include_hidden: true

    - name: Get a specific job type by ID
      dellemc.powerscale.job_type_info:
        onefs_host: "{{ onefs_host }}"
        port_no: "{{ port_no }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"
        verify_ssl: "{{ verify_ssl }}"
        job_type_id: "TreeDelete"

    - name: Get job types sorted by priority in descending order
      dellemc.powerscale.job_type_info:
        onefs_host: "{{ onefs_host }}"
        port_no: "{{ port_no }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"
        verify_ssl: "{{ verify_ssl }}"
        sort: "priority"
        dir: "DESC"



Return Values
-------------

changed (always, bool, false)
  A boolean indicating if the task had to make changes.


job_types (always, list, [{'id': 'TreeDelete', 'name': 'Tree Delete', 'description': 'Delete directory trees', 'is_hidden': False, 'enabled': True, 'priority': 5, 'policy': 'LOW', 'schedule': None, 'allow_multiple_instances': False, 'exclusion_set': 'filesystem_ops'}])
  The list of job type details.


  id (, str, )
    The unique identifier for the job type.


  name (, str, )
    The display name of the job type.


  description (, str, )
    A description of what the job type does.


  is_hidden (, bool, )
    Whether the job type is hidden.


  enabled (, bool, )
    Whether the job type is enabled.


  priority (, int, )
    The priority level of the job type.


  policy (, str, )
    The impact policy of the job type.


  schedule (, str, )
    The schedule for the job type, if any.


  allow_multiple_instances (, bool, )
    Whether multiple instances of this job type can run concurrently.


  exclusion_set (, str, )
    The exclusion set for the job type.





Status
------





Authors
~~~~~~~

- Shrinidhi Rao (@shrinidhirao) <ansible.team@dell.com>
