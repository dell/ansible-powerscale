# Ansible Modules for Dell Technologies PowerScale
The Ansible Modules for Dell Technologies (Dell) PowerScale allow Data Center and IT administrators to use RedHat Ansible to automate and orchestrate the configuration and management of Dell PowerScale arrays.

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
- Create, modify, get and delete NFS aliases.
- Get attributes and entities of the array.

The tasks can be executed by running simple playbooks written in yaml syntax.

## Table of contents

* [Code of conduct](https://github.com/dell/ansible-powerscale/blob/1.8.0/docs/CODE_OF_CONDUCT.md)
* [Maintainer guide](https://github.com/dell/ansible-powerscale/blob/1.8.0/docs/MAINTAINER_GUIDE.md)
* [Committer guide](https://github.com/dell/ansible-powerscale/blob/1.8.0/docs/COMMITTER_GUIDE.md)
* [Contributing guide](https://github.com/dell/ansible-powerscale/blob/1.8.0/docs/CONTRIBUTING.md)
* [Branching strategy](https://github.com/dell/ansible-powerscale/blob/1.8.0/docs/BRANCHING.md)
* [List of adopters](https://github.com/dell/ansible-powerscale/blob/1.8.0/docs/ADOPTERS.md)
* [Maintainers](https://github.com/dell/ansible-powerscale/blob/1.8.0/docs/MAINTAINERS.md)
* [Support](https://github.com/dell/ansible-powerscale/blob/1.8.0/docs/SUPPORT.md)
* [Security](https://github.com/dell/ansible-powerscale/blob/1.8.0/docs/SECURITY.md)
* [License](#license)
* [Supported platforms](#supported-platforms)
* [Prerequisites](#prerequisites)
* [List of Ansible modules for Dell PowerScale](#list-of-ansible-modules-for-dell-powerscale)
* [Installation and execution of Ansible modules for Dell PowerScale](#installation-and-execution-of-ansible-modules-for-dell-powerscale)
* [Maintanence](#maintanence)

## License
Ansible collection for PowerScale is released and licensed under the GPL-3.0 license. See [LICENSE](https://github.com/dell/ansible-powerscale/blob/1.8.0/LICENSE) for the full terms. Ansible modules and modules utilities that are part of the Ansible collection for PowerScale are released and licensed under the Apache 2.0 license. See [MODULE-LICENSE](https://github.com/dell/ansible-powerscale/blob/1.8.0/MODULE-LICENSE) for the full terms.

## Supported platforms
  * Dell PowerScale OneFS versions 9.2.x, 9.3.x and 9.4.x

## Prerequisites
This table provides information about the software prerequisites for the Ansible Modules for Dell PowerScale.

| **Ansible Modules** | **OneFS Version** | **Python version** | **Python SDK version** | **Ansible**              |
|---------------------|-----------------------|--------------------|----------------------------|--------------------------|
| v1.8.0 | 9.2.x <br> 9.3.x <br> 9.4.x | 3.9 <br> 3.10 <br> 3.11 | 9.1.0 | 2.12 <br> 2.13 <br> 2.14 | 

# List of Ansible modules for Dell PowerScale
  * [File System Module](https://github.com/dell/ansible-powerscale/blob/1.8.0/docs/Product%20Guide.md#file-system-module)
  * [Access Zone Module](https://github.com/dell/ansible-powerscale/blob/1.8.0/docs/Product%20Guide.md#access-zone-module)
  * [Users Module](https://github.com/dell/ansible-powerscale/blob/1.8.0/docs/Product%20Guide.md#user-module)
  * [Groups Module](https://github.com/dell/ansible-powerscale/blob/1.8.0/docs/Product%20Guide.md#group-module)
  * [Snapshot Module](https://github.com/dell/ansible-powerscale/blob/1.8.0/docs/Product%20Guide.md#snapshot-module)
  * [Snapshot Schedule Module](https://github.com/dell/ansible-powerscale/blob/1.8.0/docs/Product%20Guide.md#snapshot-schedule-module)
  * [NFS Module](https://github.com/dell/ansible-powerscale/blob/1.8.0/docs/Product%20Guide.md#nfs-module)
  * [SMB Module](https://github.com/dell/ansible-powerscale/blob/1.8.0/docs/Product%20Guide.md#smb-module)
  * [Smart Quota Module](https://github.com/dell/ansible-powerscale/blob/1.8.0/docs/Product%20Guide.md#smb-module)
  * [Info Module](https://github.com/dell/ansible-powerscale/blob/1.8.0/docs/Product%20Guide.md#info-module)
  * [Active Directory Module](https://github.com/dell/ansible-powerscale/blob/1.8.0/docs/Product%20Guide.md#ads-module)
  * [LDAP Module](https://github.com/dell/ansible-powerscale/blob/1.8.0/docs/Product%20Guide.md#ldap-module)
  * [Node Module](https://github.com/dell/ansible-powerscale/blob/1.8.0/docs/Product%20Guide.md#node-module)
  * [SyncIQ Policy Module](https://github.com/dell/ansible-powerscale/blob/1.8.0/docs/Product%20Guide.md#synciq-policy-module)
  * [SyncIQ Jobs Module](https://github.com/dell/ansible-powerscale/tree/1.8.0/docs/Product%20Guide.md#synciq-job-module)
  * [SyncIQ Performance Rules Module](https://github.com/dell/ansible-powerscale/tree/1.8.0/docs/Product%20Guide.md#synciq-rules-module)
  * [SyncIQ Reports Module](https://github.com/dell/ansible-powerscale/tree/1.8.0/docs/Product%20Guide.md#synciq-reports-module)
  * [SyncIQ Target Reports Module](https://github.com/dell/ansible-powerscale/tree/1.8.0/docs/Product%20Guide.md#synciq-target-reports-module)
  * [Groupnet Module](https://github.com/dell/ansible-powerscale/tree/1.8.0/docs/Product%20Guide.md#groupnet-module)
  * [Subnet Module](https://github.com/dell/ansible-powerscale/tree/1.8.0/docs/Product%20Guide.md#subnet-module)
  * [Network Pool Module](https://github.com/dell/ansible-powerscale/tree/1.8.0/docs/Product%20Guide.md#network-pool-module)
  * [Network Rule Module](https://github.com/dell/ansible-powerscale/tree/1.8.0/docs/Product%20Guide.md#network-rule-module)
  * [NFS Alias Module](https://github.com/dell/ansible-powerscale/tree/1.8.0/docs/Product%20Guide.md#nfs-alias-module)
  * [Settings Module](https://github.com/dell/ansible-powerscale/tree/1.8.0/docs/Product%20Guide.md#settings-module)
  * [Network Setting Module](https://github.com/dell/ansible-powerscale/blob/1.8.0/docs/Product%20Guide.md#network-settings-module)
  * [Smart Pool Setting Module](https://github.com/dell/ansible-powerscale/blob/1.8.0/docs/Product%20Guide.md#smartpool-settings-module)
  * [Filepool Plicy Module](https://github.com/dell/ansible-powerscale/blob/1.8.0/docs/Product%20Guide.md#filepool-module)
  * [Storagepool Tier Module](https://github.com/dell/ansible-powerscale/blob/1.8.0/docs/Product%20Guide.md#storagepool-tier-module)



## Installation and execution of Ansible modules for Dell PowerScale
The installation and execution steps of Ansible modules for Dell PowerScale can be found [here](https://github.com/dell/ansible-powerscale/blob/1.8.0/docs/INSTALLATION.md).

## Maintanence
Ansible Modules for Dell Technologies PowerScale deprecation cycle is aligned with [Ansible](https://docs.ansible.com/ansible/latest/dev_guide/module_lifecycle.html).
