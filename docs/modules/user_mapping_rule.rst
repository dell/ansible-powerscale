.. _user_mapping_rule_module:


user_mapping_rule -- Manages user mapping rules on PowerScale
=============================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Manages user mapping rules on PowerScale Storage System. This includes creating a new user mapping rule, modifying a user mapping rule, changing order of a user mapping rule, deleting a user mapping rule and retrieving the details of a user mapping rule.



Requirements
------------
The below requirements are needed on the host that executes this module.

- A Dell PowerScale Storage system.
- Ansible-core 2.16 or later.
- Python 3.10, 3.11 or 3.12.



Parameters
----------

  apply_order (optional, int, None)
    Current order in which the user mapping rule is applied.


  new_order (optional, int, None)
    New order in which the user mapping rule should be applied.


  access_zone (optional, str, System)
    The zone to which the user mapping applies.


  rule (optional, dict, None)
    The user mapping rule.


    operator (optional, str, None)
      The operation that a rule carries out.


    options (optional, dict, None)
      Specifies the properties for user mapping rules.


      break_on_match (optional, bool, None)
        If \ :literal:`true`\ , and the rule was applied successfuly, stop processing further.


      default_user (optional, dict, None)
        If the mapping service fails to find the second user in a rule, the service tries to find the username of the default user.


        domain (optional, str, None)
          The name of domain.


        user (True, str, None)
          The username of the user.



      group (optional, bool, None)
        If \ :literal:`true`\ , the primary GID and primary group SID should be copied to the existing credential.


      groups (optional, bool, None)
        If \ :literal:`true`\ , all additional identifiers should be copied to the existing credential.


      user (optional, bool, None)
        If \ :literal:`true`\ , the primary UID and primary user SID should be copied to the existing credential.



    user1 (optional, dict, None)
      A UNIX user or an Active Directory user.

      The user for which the identifier changes are applied.


      domain (optional, str, None)
        The name of domain.


      user (True, str, None)
        The username of the user.



    user2 (optional, dict, None)
      A UNIX user or an Active Directory user.

      The user from which the identifier are taken.


      domain (optional, str, None)
        The name of domain.


      user (True, str, None)
        The username of the user.




  state (optional, str, present)
    The state option is used to mention the existence of user mapping rule.


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
   - Idempotency is not supported for create and delete operations.
   - The \ :emphasis:`check\_mode`\  is supported.
   - The modules present in this collection named as 'dellemc.powerscale' are built to support the Dell PowerScale storage platform.




Examples
--------

.. code-block:: yaml+jinja

    
    - name: Get a user mapping rule
      dellemc.powerscale.user_mapping_rule:
        onefs_host: "{{onefs_host}}"
        verify_ssl: "{{verify_ssl}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        apply_order: 1

    - name: Delete a user mapping rule
      dellemc.powerscale.user_mapping_rule:
        onefs_host: "{{onefs_host}}"
        verify_ssl: "{{verify_ssl}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        apply_order: 1
        state: 'absent'

    - name: Create a user mapping rule
      dellemc.powerscale.user_mapping_rule:
        onefs_host: "{{onefs_host}}"
        verify_ssl: "{{verify_ssl}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        rule:
        operator: "insert"
        options:
          break: false
          group: true
          groups: true
          user: true
        user1:
          domain: "ansibleneo.com"
          user: "test_user"
        user2:
          user: "ans_user"
        state: 'present'

    - name: Update a user mapping rule
      dellemc.powerscale.user_mapping_rule:
        onefs_host: "{{onefs_host}}"
        verify_ssl: "{{verify_ssl}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        apply_order: 1
        rule:
        options:
          break: true
        state: 'present'

    - name: Apply a new order to the user mapping rule
      dellemc.powerscale.user_mapping_rule:
        onefs_host: "{{onefs_host}}"
        verify_ssl: "{{verify_ssl}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        apply_order: 1
        new_order: 2



Return Values
-------------

changed (always, bool, false)
  Whether or not the resource has changed.


user_mapping_rule_details (When a rule exists, dict, {'user_mapping_rule_details': {'apply_order': 7, 'operator': 'insert', 'options': {'_break': False, 'default_user': None, 'group': True, 'groups': True, 'user': True}, 'user1': {'domain': None, 'user': 'test_ans_user'}, 'user2': {'domain': None, 'user': 'Test_userAnand'}}})
  Rule details.


  apply_order (, int, )
    Current order of the rule.


  operator (, str, )
    The operation that a rule carries out.


  options (, dict, )
    Specifies the properties for user mapping rules.


    _break (, bool, )
      If \ :literal:`true`\ , and the rule was applied successfuly, stop processing further.


    group (, bool, )
      If \ :literal:`true`\ , the primary GID and primary group SID should be copied to the existing credential.


    groups (, bool, )
      If \ :literal:`true`\ , all additional identifiers should be copied to the existing credential.


    user (, bool, )
      If \ :literal:`true`\ , the primary UID and primary user SID should be copied to the existing credential.


    default_user (, dict, )
      If the mapping service fails to find the second user in a rule, the service tries to find the username of the default user..


      user (, str, )
        The username of the user.


      domain (, str, )
        The name of domain.




  user1 (, dict, )
    A UNIX user or an Active Directory user.


    user (, str, )
      The username of the user.


    domain (, str, )
      The name of domain.



  user2 (, dict, )
    A UNIX user or an Active Directory user.


    user (, str, )
      The username of the user.


    domain (, str, )
      The name of domain.







Status
------





Authors
~~~~~~~

- Ananthu S Kuttattu (@kuttattz) <ansible.team@dell.com>

