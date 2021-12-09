**Ansible Modules for Dell EMC PowerScale** 
=========================================
### Release Notes 1.4.0

>   © 2021 Dell Inc. or its subsidiaries. All rights reserved. Dell,
>   EMC, and other trademarks are trademarks of Dell Inc. or its
>   subsidiaries. Other trademarks may be trademarks of their respective
>   owners.

Content
-------
These release notes contain supplemental information about Ansible
Modules for Dell EMC PowerScale.

-   [Revision History](#revision-history)
-   [Product Description](#product-description)
-   [Features](#features) 
-   [Known issues and limitations](#known-issues)
-   [Software media, organization, and files](#software-media-organization-and-files)
-   [Additional resources](#additional-resources) 

Revision history
----------------
The table in this section lists the revision history of this document.

Table 1. Revision history

| Revision | Date      | Description                                               |
|----------|-----------|-----------------------------------------------------------|
| 01      | Dec 2021  | Ansible Modules for Dell EMC PowerScale 1.4.0              |


Product Description
-------------------
This section describes the Ansible Modules for Dell EMC PowerScale.
The Ansible Modules for Dell EMC PowerScale allow Data Center and IT administrators to use RedHat Ansible to automate and orchestrate the configuration and management of Dell EMC PowerScale arrays. 

The Ansible Modules for Dell EMC PowerScale support the following features:
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
- Get attributes and entities of the array. 
  
The Ansible modules use playbooks, written in yaml syntax, to list, show, create, delete, and modify each of these entities.

Features
---------------------------
This section describes the features of the Ansible Modules for Dell EMC PowerScale for this release.

The Ansible Modules for Dell EMC PowerScale release 1.4.0 supports the following features: 
 - Idempotency 
   - Has been handled in all modules.
   - Allows the playbook to be run multiple times.
   - Avoids the need for complex rollbacks. 
     
- Access Zones 
  - PowerScale has a concept of access zones. These are to partition the cluster into multiple isolated sections.
  - Ansible modules support access zone operations that can also operate on the default (system) access zone.
  - Users and Groups can be specific to a particular access zone.
  - For non-system access zones, the path provided by the playbook is a relative path.
  - Absolute path = Access zone base path + relative path provided by the user.

MODULES
-   The Groupnet module supports the following functionality: 
    -   Create a Groupnet
    -   Modify a Groupnet
    -   Delete a Groupnet
    -   Retrieve details of a Groupnet

-   The Subnet module supports the following functionality: 
    -   Create a Subnet
    -   Modify a Subnet
    -   Delete a Subnet
    -   Retrieve details of a Subnet

-   The Network Pool module supports the following functionality: 
    -   Create a Network Pool
    -   Modify a Network Pool
    -   Delete a Network Pool
    -   Retrieve details of a Network Pool

-   The Network Rule module supports the following functionality: 
    -   Create a Network Rule
    -   Modify a Network Rule
    -   Delete a Network Rule
    -   Retrieve details of a Network Rule

-   The Settings module supports the following functionality:
    -   Retrieve details of cluster email
    -   Modify cluster email settings
    -   Addition of NTP Servers
    -   Deletion of NTP Servers

-   The Access zone module is enhanced to support the following functionality:
    -   Create an access zone

-   The Gather Facts module is enhanced to support the following functionality: 
    -   Get details of the any entity listed below:
    
        - Network Groupnets
        - Network Subnets
        - Network Pools
        - Network Rules
        - Network Interfaces
    
Known issues
------------
Known problems in this release are listed.

| **Issue**        | **Description**           | **Resolution**  |
| ------------- |-------------| -----|
| Snapshot schedule | If the playbook has a desired_retention field, running same the playbook again returns the changed as True (Idempotency does not work) | This is an issue in the supported OneFS versions. |
| Filesystem creation | Creation of a filesystem can fail when api_user: "admin" because it is possible that the admin user may not have privileges to set an ACLs | Create a filesystem with api_user: "root". |
| Snapshot creation with alias name | Alias name attribute remains null in spite of creating snapshot with alias name | This is an issue with the PowerScale rest API. Alias name is not getting appended to the attribute in response. |
| SyncIQ Job creation/modification/retrieval | When SyncIQ policy has any job of the type "resync_prep/allow_write/allow_write_revert" then creation, modification or retrieval of SyncIQ job will fail with an error saying "Invalid value for 'action', must be one of ['copy', 'sync']". | This is an issue in the supported OneFS versions. |

Limitations
-----------
This section lists the limitations in this release of Ansible Modules for Dell EMC PowerScale.

- Gatherfacts  
  - Getting the list of users and groups with very long names may fail. 
 
- Users and Groups 
  - Only local users and groups can be created. 
  -  Operations on users and groups with very long names may fail. 

- Access Zone
  
  - Deletion of access zones is not supported. 
 
- Filesystems
  
  - ACLs can only be modified from POSIX to POSIX mode.
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
for PowerScale GitHub](../) page.

Additional resources
--------------------
This section provides more information about the product, how to get support, and provide feedback.

- Documentation
    - This section lists the related documentation for Ansible Modules for Dell EMC PowerScale.
    - The documentation is available on the Ansible Modules for PowerScale GitHub page. The documentation includes the following:
      -  Ansible Modules for Dell EMC PowerScale Release Notes (this document).
      -  Ansible Modules for Dell EMC PowerScale Product Guide

- Troubleshooting and support
    - The Dell Container Community provides your primary source of support services. 

    - For any setup, configuration issues, questions or feedback, join the Dell EMC Container community at https://www.dell.com/community/Containers/bd-p/Containers.

- Technical support 
  
    - [Dell EMC Online Support](https://www.dell.com/support/home/en-in) also provides technical support services.  To open a service request, you must have a valid support agreement.
      
    - To get a valid support agreement or for other questions about your account, contact your Dell EMC sales representative. 

    - For documentation, release notes, software updates, and other information about Dell EMC products, go to [Dell EMC Online Support](https://www.dell.com/support/home/en-in).
    
- Support 
    - Use the resources in this topic to get help and support. 
      

    - The source code available on Github is unsupported and provided solely under the terms of the license attached to the source code. 
      

    - For clarity, Dell EMC does not provide support for any source code modifications. 


    - For any Ansible module setup, configuration issues, questions or feedback, 
    join the Dell EMC Automation community
      at https:// www.dell.com/community/Automation/bd-p/Automation?ref=lithium_menu 
      

    - For any Dell EMC storage issues, please contact Dell support at: https://www.dell.com/support.
