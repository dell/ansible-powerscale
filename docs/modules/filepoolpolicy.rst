.. _filepoolpolicy_module:


filepoolpolicy -- Manages file pool policy on PowerScale
========================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Managing file pool policy on PowerScale Storage System. This includes creating a new file pool policy, deleting a file pool policy and retrieving the details of a file pool policy.



Requirements
------------
The below requirements are needed on the host that executes this module.

- A Dell PowerScale Storage system.
- Ansible-core 2.17 or later.
- Python 3.11, 3.12 or 3.13.



Parameters
----------

  policy_id (optional, str, None)
    Unique Id of the file pool policy.

    It is mutually exclusive with :emphasis:`policy\_name`.


  policy_name (optional, str, None)
    Unique name of the file pool policy.

    It is mutually exclusive with :emphasis:`policy\_id`.

    Mandatory for file pool policy creation.


  description (optional, str, None)
    A description of the file pool policy.


  apply_order (optional, int, None)
    The order in which the policy should be applied.

    It is relative to other policies.


  apply_data_storage_policy (optional, dict, None)
    Action to move files to storage pool or tier.


    ssd_strategy (optional, str, None)
      Strategy for ssd.


    storagepool (optional, str, anywhere)
      Name of the storage pool.



  apply_snapshot_storage_policy (optional, dict, None)
    Action to move snapshots to storage pool or tier.


    ssd_strategy (optional, str, None)
      Strategy for ssd.


    storagepool (optional, str, anywhere)
      Name of the storage pool.



  set_requested_protection (optional, str, None)
    Action to change requested protection.


  set_data_access_pattern (optional, str, None)
    Action to set data access pattern optimization.


  set_write_performance_optimization (optional, str, None)
    Action to set write performance optimization.


  file_matching_pattern (optional, dict, None)
    The file matching rules for the policy.


    or_criteria (True, list, None)
      or criteria conditions for the file policy.

      Maximum of 3 criteria's is possible.


      and_criteria (True, list, None)
        The and criteria conditions for the file policy.

        Maximum of 5 criteria is possible.


        type (True, str, None)
          The file criteria to be compared to a given value.


        condition (optional, str, None)
          The condition to use while comparing an attribute with its value.

          If :emphasis:`type` is :literal:`size` then the conditions are ['equal', 'not\_equal', 'greater\_than', 'greater\_than\_equal\_to', 'less\_than', 'less\_than\_equal\_to'].

          If :emphasis:`type` is :literal:`accessed` or :literal:`created` or :literal:`modified` or :literal:`metadata\_changed` then the conditions are ['after','before', 'is\_newer\_than', 'is\_older\_than'].

          If :emphasis:`type` is :literal:`file\_attribute` then the conditions are ['matches','does\_not\_match', 'exists', 'does\_not\_exist'].

          If :emphasis:`type` is :literal:`file\_path` then the conditions are ['matches','does\_not\_match', 'contains', 'does\_not\_contain'].

          If :emphasis:`type` is :literal:`file\_type` or  :literal:`file\_name` then the conditions are ['matches','does\_not\_match'].


        value (optional, str, None)
          The value to be compared against a file criteria.

          Required in case if :emphasis:`type` is :literal:`file\_name` or :literal:`file\_path` or :literal:`file\_attribute`.

          If :emphasis:`type` is :literal:`file\_name` then value wil have file name.

          If :emphasis:`type` is :literal:`file\_path` then value wil have file path.

          If :emphasis:`type` is :literal:`file\_attribute` then value wil have file attribute field value.


        field (optional, str, None)
          File attribute field name to be compared in a custom comparison.

          Required only if the :emphasis:`type` is :literal:`file\_attribute`.


        case_sensitive (optional, bool, None)
          :literal:`true` to indicate case sensitivity when comparing file attributes.

          Required only if the :emphasis:`type` is :literal:`file\_name` or :literal:`file\_path`.


        file_type_option (optional, str, None)
          File type option.

          Required only if the :emphasis:`type` is :literal:`file\_type`.


        size_info (optional, dict, None)
          File size value and unit.

          Required only if the :emphasis:`type` is :literal:`size`.


          size_value (True, int, None)
            Size value.


          size_unit (True, str, None)
            Unit for the size value



        datetime_value (optional, str, None)
          Date and Time value.

          Format is 'YYYY-MM-DD HOUR:MINUTE'

          Required only if the :emphasis:`type` is :literal:`accessed` or :literal:`created` or :literal:`modified` or :literal:`metadata\_changed` and \\ the :emphasis:`condition` is :literal:`after` or :literal:`before`


        relative_datetime_count (optional, dict, None)
          A relative duration (e.g., 2 years, 3 weeks, 50 seconds).

          Required only if the :emphasis:`type` is :literal:`accessed` or :literal:`created` or :literal:`modified` or :literal:`metadata\_changed` and \\ the :literal:`condition` is :literal:`is\_newer\_than` or :literal:`is\_older\_than`


          time_value (True, int, None)
            Relative time count.


          time_unit (True, str, None)
            Unit for the relative time count






  state (True, str, None)
    The state option is used to mention the existence of file pool policy.


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
   - Modifying a file pool policy is not supported.
   - The :emphasis:`check\_mode` is supported.
   - The modules present in this collection named as 'dellemc.powerscale' are built to support the Dell PowerScale storage platform.




Examples
--------

.. code-block:: yaml+jinja

    
    - name: Get a file pool policy
      dellemc.powerscale.filepoolpolicy:
        onefs_host: "{{onefs_host}}"
        verify_ssl: "{{verify_ssl}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        policy_name: "test_11"
        state: 'present'

    - name: Delete a file pool policy
      dellemc.powerscale.filepoolpolicy:
        onefs_host: "{{onefs_host}}"
        verify_ssl: "{{verify_ssl}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        policy_name: "test_11"
        state: 'absent'

    - name: Create a file pool policy
      dellemc.powerscale.filepoolpolicy:
        onefs_host: "{{onefs_host}}"
        verify_ssl: "{{verify_ssl}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        policy_name: "test_policy_1"
        description: 'Creating a policy'
        apply_order: 1
        apply_data_storage_policy:
          ssd_strategy: "SSD_metadata_read_acceleration"
          storagepool: "test_tier"
        set_data_access_pattern: "concurrency"
        set_requested_protection: "mirrored_over_3_nodes"
        set_write_performance_optimization: "enable_smartcache"
        file_matching_pattern:
          or_criteria:
            - and_criteria:
                - type: "file_name"
                  condition: "does_not_match"
                  value: "file_name_test"
                  case_sensitive: true
                - type: "accessed"
                  condition: "after"
                  datetime_value: "2022-04-04 23:30"
                - type: "created"
                  condition: "is_newer_than"
                  relative_datetime_count:
                    time_value: 12
                    time_unit: "years"
            - and_criteria:
                - type: "size"
                  condition: "not_equal"
                  size_info:
                    size_value: 60
                    size_unit: "MB"
                - type: "file_attribute"
                  condition: "does_not_match"
                  field: "test_field"
                  value: "uni"
                - type: "file_attribute"
                  condition: "exists"
                  field: "test"
        state: 'present'



Return Values
-------------

changed (always, bool, false)
  Whether or not the resource has changed.


filepool_policy_details (When a Policy exists, complex, {'filepool_policy_details': {'actions': [{'action_param': '3x', 'action_type': 'set_requested_protection'}, {'action_param': 'concurrency', 'action_type': 'set_data_access_pattern'}, {'action_param': 'True', 'action_type': 'enable_coalescer'}, {'action_param': "{'ssd_strategy': 'metadata', 'storagepool': 'test_tier'}", 'action_type': 'apply_data_storage_policy'}], 'apply_order': 1, 'description': 'Creating a policy', 'file_matching_pattern': {'or_criteria': [{'and_criteria': [{'attribute_exists': None, 'begins_with': None, 'case_sensitive': True, 'field': None, 'operator': '!=', 'type': 'name', 'units': None, 'use_relative_time': None, 'value': 'we'}]}, {'and_criteria': [{'attribute_exists': None, 'begins_with': None, 'case_sensitive': False, 'field': None, 'operator': '!=', 'type': 'name', 'units': None, 'use_relative_time': None, 'value': 'we'}, {'attribute_exists': None, 'begins_with': None, 'case_sensitive': False, 'field': None, 'operator': '==', 'type': 'name', 'units': None, 'use_relative_time': None, 'value': 'we'}]}]}, 'id': 25, 'name': 'test_policy'}})
  Policy details.


  id (, int, )
    Unique ID of the policy.


  name (, str, )
    Unique name of the policy.


  description (, str, )
    Description of the policy.


  apply_order (, int, )
    The order in which policy is present with respect to other policies.


  actions (, list, )
    List of action's available for the policy.


  file_matching_pattern (, complex, )
    File matching pattern of the policy.


    or_criteria (, list, )
      or criteria conditions for the file policy.







Status
------





Authors
~~~~~~~

- Ananthu S Kuttattu (@kuttattz) <ansible.team@dell.com>

