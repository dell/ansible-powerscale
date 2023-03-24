**Ansible Modules for Dell Technologies PowerScale** 
=========================================
### Release notes 1.9.0

>   © 2022 Dell Inc. or its subsidiaries. All rights reserved. Dell
>   and other trademarks are trademarks of Dell Inc. or its
>   subsidiaries. Other trademarks may be trademarks of their respective
>   owners.

Content
-------
These release notes contain supplemental information about Ansible
Modules for Dell Technologies (Dell) PowerScale.

-   [Revision History](#revision-history)
-   [Product Description](#product-description)
-   [New Features and Enhancements](#new-features-and-enhancements) 
-   [Known issues and limitations](#known-issues)
-   [Software media, organization, and files](#software-media-organization-and-files)
-   [Additional resources](#additional-resources) 

Revision history
----------------
The table in this section lists the revision history of this document.

Table 1. Revision history

| Revision | Date          | Description                                               |
|----------|---------------|-----------------------------------------------------------|
| 01       | March 2023    | Ansible Modules for Dell PowerScale 1.9.0                 |


Product description
-------------------
This section describes the Ansible Modules for Dell PowerScale.
The Ansible Modules for Dell PowerScale allow Data Center and IT administrators to use RedHat Ansible to automate and orchestrate the configuration and management of Dell  PowerScale arrays. 

The Ansible Modules for Dell PowerScale support the following features:
- Create user, groups, filesystem, NFS export, smart quotas, SMB share, snapshot and snapshot schedule of a filesystem.
- Modify user, groups, filesystem, access zone, NFS export, smart quotas, SMB share, snapshot and snapshot schedule of a filesystem.
- Delete user, groups, filesystem, NFS export, smart quotas, SMB share, snapshot and snapshot schedule of a filesystem.
- Get details of user, groups, node, filesystem, access zone, NFS export, smart quotas, SMB share, snapshot and snapshot schedule of a filesystem.
- Get details of SyncIQ policies, SyncIQ jobs, SyncIQ reports, SyncIQ target reports and SyncIQ performance rules of the cluster.
- Add, modify and remove Active Directory and LDAP to Authentication providers list.
- Map or unmap Active Directory and LDAP Authentication providers to Access zone.
- Create, modify and delete SyncIQ policy.
- Create job on SyncIQ policy and modify the state of SyncIQ Job.
- Create, modify and delete SyncIQ performance rule.
- Create, modify and delete Groupnet, Subnet, Network Pool and Network Rule.
- Get details of Groupnet, Subnet, Network Pool and Network Rule.
- Modify cluster email settings.
- Get cluster email settings and NTP Server details.
- Add and remove NTP Servers
- Create an access zone.
- Get network and smart pool settings.
- Modify network and smart pool settings.
- Get Filepool policy and Storagepool tiers.
- Create, delete Filepool policy and Storagepool tiers.
- Get, Create, modify and delete NFS aliases. 
- Get attributes and entities of the array.
- Get details and close open SMB files.
  
The Ansible modules use playbooks, written in yaml syntax, to list, show, create, delete, and modify each of these entities.

New Features and Enhancements
---------------------------
This section describes the features of the Ansible Modules for Dell PowerScale for this release.

The Ansible Modules for Dell PowerScale release 1.9.0 supports the following features:

- The SMB file module supports this functionality:
    - Get details and close open SMB files.
- The User module supports this functionality:
    - Added support for modifying the user password and creating user with user_id.
- The Group module supports this functionality:
    - Added support for creating group with group_id.
- The Smart quota module supports this functionality:
    - Added support for providing path of a non-system access zone to begin without slash.

Known issues
------------
Known problems in this release are listed.

| **Issue**        | **Description**           | **Resolution**  |
| ------------- |-------------| -----|
| Snapshot schedule | If the playbook has a desired_retention field, running the same playbook again returns the changed as True (Idempotency does not work). | This is an issue in the supported OneFS versions. |
| Filesystem creation | Creation of a filesystem can fail when api_user: "admin" is used because it is possible that the admin user may not have privileges to set an ACLs. | Assigning privileges ISI_PRIV_IFS_RESTORE and ISI_PRIV_NS_TRAVERSE to the user should enable the creation of filesystem with ACL permissions. |
| Snapshot creation with alias name | Alias name attribute remains null in spite of creating snapshot with alias name | This is an issue with the PowerScale rest API. Alias name is not getting appended to the attribute in response. |
| SyncIQ Job creation/modification/retrieval | When SyncIQ policy has any job of the type "resync_prep/allow_write/allow_write_revert" then creation, modification or retrieval of SyncIQ job will fail with an error saying "Invalid value for 'action', must be one of ['copy', 'sync']". | This is an issue in the supported OneFS versions. |
| SMB share creation with NIS group permissions | Creating a SMB share with NIS group permissions fails with error that the group cannot be found. | This is an issue in the supported OneFS versions. |
| Getting group details  | Getting the details of a group by group_name with provider type as NIS fails. | This is an issue in the supported OneFS versions. |

Limitations
-----------
This section lists the limitations in this release of Ansible Modules for Dell PowerScale.

- Info  
  - Getting the list of users and groups with very long names may fail. 
 
- Users and Groups 
  - Only local users and groups can be created. 
  -  Operations on users and groups with very long names may fail. 

- Access Zone
  - Deletion of access zones is not supported. 
 
- Filesystems
  -  Only directory quotas are supported but not user or group quotas.
  -  Modification of include_snap_data flag is not supported.
     
- NFS Export
  - If there are multiple exports present with the same path in an access zone, operations on such exports fail. 
    
- Smart Quota
  - Once the limits are assigned to the quota, then the quota can't be converted to accounting. Only modification to the threshold limits is permitted.
  - It's mandatory to pass 'quota' parameter for create and modify operations for any quota type.

- SyncIQ Performance Rule
  - Operations performed in parallel from other interfaces apart from playbook cannot guarantee desirable results.
    
- No support for advanced PowerScale features
  - Advanced PowerScale features include tiering, replication, and so on.  
----------------
Software media, organization, and files 
-----------
The software package is available for download from the [Ansible Modules
for PowerScale GitHub](https://github.com/dell/ansible-powerscale/tree/1.9.0) page.

Additional resources
--------------------
This section provides more information about the product, how to get support, and provide feedback.

- Documentation
    - This section lists the related documentation for Ansible Modules for Dell PowerScale.
    - The documentation is available on the Ansible Modules for PowerScale GitHub page. The documentation includes the following:
      -  Ansible Modules for Dell Technologies PowerScale Release Notes (this document).
      -  Ansible Modules for Dell Technologies PowerScale Product Guide

- Troubleshooting and support
    - The Dell Container Community provides your primary source of support services. 

    - For any setup, configuration issues, questions or feedback, join the Dell Container community at https://www.dell.com/community/Containers/bd-p/Containers.

- Technical support 
  
    - [Dell Online Support](https://www.dell.com/support/home/en-in) also provides technical support services.  To open a service request, you must have a valid support agreement.
      
    - To get a valid support agreement or for other questions about your account, contact your Dell sales representative. 

    - For documentation, release notes, software updates, and other information about Dell products, go to [Dell Online Support](https://www.dell.com/support/home/en-in).
    
- Support 
    - Use the resources in this topic to get help and support. 
      

    - The source code available on Github is unsupported and provided solely under the terms of the license attached to the source code. 
      

    - For clarity, Dell does not provide support for any source code modifications. 


    - For any Ansible module setup, configuration issues, questions or feedback, 
    join the Dell Automation community
      at https:// www.dell.com/community/Automation/bd-p/Automation?ref=lithium_menu 
      

    - For any Dell storage issues, please contact Dell support at: https://www.dell.com/support.
