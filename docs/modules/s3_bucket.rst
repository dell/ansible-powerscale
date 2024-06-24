.. _s3_bucket_module:


s3_bucket -- Manage S3 buckets on a PowerScale Storage System
=============================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Managing S3 buckets on an PowerScale system includes retrieving details of S3 bucket, creating S3 bucket, modifying and deleting S3 bucket.



Requirements
------------
The below requirements are needed on the host that executes this module.

- A Dell PowerScale Storage system.
- Ansible-core 2.15 or later.
- Python 3.10, 3.11 or 3.12.



Parameters
----------

  path (optional, str, None)
    Specifies path on which the S3 bucket will be created. It is the absolute path for System access zone and it is relative if using non-system access zone.

    For example, if your access zone is 'Ansible' and it has a base path '/ifs/ansible' and the path specified is '/user1', then the effective path would be '/ifs/ansible/user1'.

    If your access zone is System, and you have 'directory1' in the access zone, the path provided should be '/ifs/directory1'.

    *path* is required while creating a S3 bucket.

    The S3 bucket path can not be modified after creation.


  create_path (optional, bool, None)
    Will create the path if does not exist.

    API default is ``false``.


  access_zone (optional, str, System)
    Specifies the access zone in which the S3 bucket exists.

    Access zone once set cannot be changed.


  s3_bucket_name (True, str, None)
    Name of the S3 bucket.

    *s3_bucket_name* while creating the S3 bucket.


  owner (optional, str, None)
    Specifies the owner of the S3 bucket.

    If *owner* not passed, then ``root`` will be default *owner* for ``System`` access zone only.

    If owner belongs to another provider domain, it should be mentioned along with domain name as "DOMAIN_NAME\\username" or DOMAIN_NAME\username.


  description (optional, str, None)
    Specifies the description of the S3 bucket.

    Pass empty string to remove the *description*.


  object_acl_policy (optional, str, None)
    Set behaviour of object acls for a specified S3 bucket.


  acl (optional, list, None)
    Specifies the permissions and grantees in the S3 bucket.


    permission (True, str, None)
      Specifies the S3 permission being allowed.

      *permission* and *grantee* are required together.


    grantee (True, dict, None)
      Specifies the properties of grantee.

      *permission* and *grantee* are required together.

      It consists of *name*, *type*, and *provider_type*.


      name (True, str, None)
        Specifies the name of grantee (user, group or wellknown).


      type (optional, str, user)
        Specifies the type of grantee.


      provider_type (optional, str, local)
        Specifies the provider type of grantee.



    acl_state (optional, str, present)
      Specifies if the acls are to be added or removed.



  state (optional, str, present)
    Defines whether the S3 bucket should exist or not.

    Value ``present`` indicates that the S3 bucket should exist in system.

    Value ``absent`` indicates that the S3 bucket should not exist in system.


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
   - To delete the S3 bucket, the S3 service must be enabled.
   - The *check_mode* is supported.
   - The modules present in this collection named as 'dellemc.powerscale' are built to support the Dell PowerScale storage platform.




Examples
--------

.. code-block:: yaml+jinja

    
    - name: Create S3 Bucket
      dellemc.powerscale.s3_bucket:
        onefs_host: "{{onefs_host}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        verify_ssl: "{{verify_ssl}}"
        s3_bucket_name: "Anisble_S3_bucket"
        path: "/sample_bucket_path"
        access_zone: "sample-zone"
        owner: "sample-user"
        description: "the S3 bucket created."
        object_acl_policy: "replace"
        acl:
          - permission: "READ"
            grantee:
              name: "everyone"
              type: "wellknown"
          - permission: "READ_ACL"
            grantee:
              name: "sample-user"
              type: "user"
              provider_type: "local"
            acl_state: "present"
        state: "present"

    - name: Create S3 Bucket
      dellemc.powerscale.s3_bucket:
        onefs_host: "{{onefs_host}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        verify_ssl: "{{verify_ssl}}"
        s3_bucket_name: "Anisble_S3_bucket_1"
        path: "/ifs/sample_bucket_path_1"
        create_path: true
        access_zone: "System"
        owner: "sample-user"
        acl:
          - permission: "READ"
            grantee:
              name: "everyone"
              type: "wellknown"
        state: "present"

    - name: Get S3 Bucket
      dellemc.powerscale.s3_bucket:
        onefs_host: "{{onefs_host}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        verify_ssl: "{{verify_ssl}}"
        s3_bucket_name: "Anisble_S3_bucket"
        access_zone: "sample-zone"

    - name: Modify S3 bucket
      dellemc.powerscale.s3_bucket:
        onefs_host: "{{onefs_host}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        verify_ssl: "{{verify_ssl}}"
        s3_bucket_name: "Anisble_S3_bucket"
        access_zone: "sample-zone"
        description: "the S3 bucket updated."
        object_acl_policy: "deny"
        acl:
          - permission: "WRITE"
            grantee:
              name: "sample-group"
              type: "group"
              provider_type: "ads"

    - name: Remove grantee from S3 bucket
      dellemc.powerscale.s3_bucket:
        onefs_host: "{{onefs_host}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        verify_ssl: "{{verify_ssl}}"
        s3_bucket_name: "Anisble_S3_bucket"
        access_zone: "sample-zone"
        acl:
          - permission: "WRITE"
            grantee:
              name: "sample-group"
              type: "group"
              provider_type: "ads"
            acl_state: "absent"

    - name: Delete S3 Bucket
      dellemc.powerscale.s3_bucket:
        onefs_host: "{{onefs_host}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        verify_ssl: "{{verify_ssl}}"
        s3_bucket_name: "Anisble_S3_bucket"
        access_zone: "sample-zone"
        state: "absent"



Return Values
-------------

changed (always, bool, false)
  A boolean indicating if the task had to make changes.


S3_bucket_details (always, complex, {'access_zone': 'System', 'acl': [{'grantee': {'id': 'ID', 'name': 'ansible-user', 'type': 'user'}, 'permission': 'READ'}], 'description': 'description', 'id': 'ansible_S3_bucket', 'name': 'ansible_S3_bucket', 'object_acl_policy': 'replace', 'owner': 'ansible-user', 'path': '/ifs/<sample-path>', 'zid': 1})
  The updated S3 Bucket details.


  acl (, list, )
    Specifies the properties of S3 access controls.


    grantee (, dict, )
      Specifies details of grantee.


      id (, str, )
        ID of the grantee.


      name (, str, )
        Name of the grantee.


      type (, str, )
        Specifies the type of the grantee.



    permission (, str, )
      Specifies the S3 permission being allowed.



  description (, str, )
    Specifies the description of the S3 bucket.


  id (, str, )
    S3 bucket ID.


  name (, str, )
    S3 bucket name.


  object_acl_policy (, str, )
    Set behaviour of object acls for a specified S3 bucket.


  owner (, str, )
    Specifies the owner of the S3 bucket.


  path (, str, )
    Path of S3 bucket with in ``'/ifs'``.


  zid (, int, )
    Zone id.


  zone (, str, )
    Access zone name.






Status
------





Authors
~~~~~~~

- Bhavneet Sharma(@Bhavneet-Sharma) <ansible.team@dell.com>

