# Ansible Modules for Dell Technologies PowerScale

[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-v2.0%20adopted-ff69b4.svg)](https://github.com/dell/ansible-powerscale/blob/main/docs/CODE_OF_CONDUCT.md)
[![License](https://img.shields.io/github/license/dell/ansible-powerscale)](https://github.com/dell/ansible-powerscale/blob/main/LICENSE)
[![Python version](https://img.shields.io/badge/python-3.9.6+-blue.svg)](https://www.python.org/downloads/)
[![Ansible version](https://img.shields.io/badge/ansible-2.15.6+-blue.svg)](https://pypi.org/project/ansible/)
[![Pypowerscale](https://img.shields.io/github/v/release/dell/python-powerscale?include_prereleases&label=Pypowerscale&style=flat-square)](https://github.com/Isilon/isilon_sdk_python)
[![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/dell/ansible-powerscale?include_prereleases&label=latest&style=flat-square)](https://github.com/dell/ansible-powerscale/releases)
[![codecov](https://codecov.io/gh/dell/ansible-powerscale/branch/main/graph/badge.svg)](https://app.codecov.io/gh/dell/ansible-powerscale)

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
- Find and close the SMB open files.
- Create, modify, get details and delete a user mapping rule.
- Create, modify, get details and delete an S3 bucket.
- Get details and modify NFS default settings.
- Get details and modify NFS global settings.
- Get details and modify NFS zone settings.
- Get details and modify SyncIQ global settings.
- Get details, modify, import, and delete SyncIQ certificates.
- Get details and modify SMB global settings.
- Get details and modify SNMP settings.
- Get details, import, modify, setting default and delete server certificates.

The tasks can be executed by running simple playbooks written in yaml syntax.

## Table of contents

* [Code of conduct](https://github.com/dell/ansible-powerscale/blob/main/docs/CODE_OF_CONDUCT.md)
* [Maintainer guide](https://github.com/dell/ansible-powerscale/blob/main/docs/MAINTAINER_GUIDE.md)
* [Committer guide](https://github.com/dell/ansible-powerscale/blob/main/docs/COMMITTER_GUIDE.md)
* [Contributing guide](https://github.com/dell/ansible-powerscale/blob/main/docs/CONTRIBUTING.md)
* [Branching strategy](https://github.com/dell/ansible-powerscale/blob/main/docs/BRANCHING.md)
* [List of adopters](https://github.com/dell/ansible-powerscale/blob/main/docs/ADOPTERS.md)
* [Maintainers](https://github.com/dell/ansible-powerscale/blob/main/docs/MAINTAINERS.md)
* [Support](https://github.com/dell/ansible-powerscale/blob/main/docs/SUPPORT.md)
* [Security](https://github.com/dell/ansible-powerscale/blob/main/docs/SECURITY.md)
* [License](#license)
* [Supported platforms](#supported-platforms)
* [Prerequisites](#prerequisites)
* [List of Ansible modules for Dell PowerScale](#list-of-ansible-modules-for-dell-powerscale)
* [Installation and execution of Ansible modules for Dell PowerScale](#installation-and-execution-of-ansible-modules-for-dell-powerscale)
* [Maintanence](#maintanence)

## License
Ansible collection for PowerScale is released and licensed under the GPL-3.0 license. See [LICENSE](https://github.com/dell/ansible-powerscale/blob/main/LICENSE) for the full terms. Ansible modules and modules utilities that are part of the Ansible collection for PowerScale are released and licensed under the Apache 2.0 license. See [MODULE-LICENSE](https://github.com/dell/ansible-powerscale/blob/main/MODULE-LICENSE) for the full terms.

## Supported platforms
  * Dell PowerScale OneFS versions 9.3.x, 9.4.x and 9.5.x

## Prerequisites
This table provides information about the software prerequisites for the Ansible Modules for Dell PowerScale.

| **Ansible Modules** | **OneFS Version** | **Python version** | **Python SDK version** | **Ansible**              |
|---------------------|-----------------------|--------------------|----------------------------|--------------------------|
| main | 9.4.x <br> 9.5.x <br> 9.7.x <br> 9.8.x | 3.9 <br> 3.10 <br> 3.11 <br> 3.11 | 0.3.0.1 | 2.14 <br> 2.15 <br> 2.16 <br> 2.16 |

# List of Ansible modules for Dell PowerScale
  * [File System Module](https://github.com/dell/ansible-powerscale/blob/main/docs/modules/filesystem.rst)
  * [Access Zone Module](https://github.com/dell/ansible-powerscale/blob/main/docs/modules/accesszone.rst)
  * [User Module](https://github.com/dell/ansible-powerscale/blob/main/docs/modules/user.rst)
  * [Group Module](https://github.com/dell/ansible-powerscale/blob/main/docs/modules/group.rst)
  * [Snapshot Module](https://github.com/dell/ansible-powerscale/blob/main/docs/modules/snapshot.rst)
  * [Snapshot Schedule Module](https://github.com/dell/ansible-powerscale/blob/main/docs/modules/snapshotschedule.rst)
  * [NFS Module](https://github.com/dell/ansible-powerscale/blob/main/docs/modules/nfs.rst)
  * [SMB Module](https://github.com/dell/ansible-powerscale/blob/main/docs/modules/smb.rst)
  * [Smart Quota Module](https://github.com/dell/ansible-powerscale/blob/main/docs/modules/smartquota.rst)
  * [Info Module](https://github.com/dell/ansible-powerscale/blob/main/docs/modules/info.rst)
  * [Active Directory Module](https://github.com/dell/ansible-powerscale/blob/main/docs/modules/ads.rst)
  * [LDAP Module](https://github.com/dell/ansible-powerscale/blob/main/docs/modules/ldap.rst)
  * [Node Module](https://github.com/dell/ansible-powerscale/blob/main/docs/modules/node.rst)
  * [SyncIQ Policy Module](https://github.com/dell/ansible-powerscale/blob/main/docs/modules/synciqpolicy.rst)
  * [SyncIQ Jobs Module](https://github.com/dell/ansible-powerscale/tree/main/docs/modules/synciqjob.rst)
  * [SyncIQ Performance Rules Module](https://github.com/dell/ansible-powerscale/tree/main/docs/modules/synciqrules.rst)
  * [SyncIQ Reports Module](https://github.com/dell/ansible-powerscale/tree/main/docs/modules/synciqreports.rst)
  * [SyncIQ Target Reports Module](https://github.com/dell/ansible-powerscale/tree/main/docs/modules/synciqtargetreports.rst)
  * [Groupnet Module](https://github.com/dell/ansible-powerscale/tree/main/docs/modules/groupnet.rst)
  * [Subnet Module](https://github.com/dell/ansible-powerscale/tree/main/docs/modules/subnet.rst)
  * [Network Pool Module](https://github.com/dell/ansible-powerscale/tree/main/docs/modules/networkpool.rst)
  * [Network Rule Module](https://github.com/dell/ansible-powerscale/tree/main/docs/modules/networkrule.rst)
  * [NFS Alias Module](https://github.com/dell/ansible-powerscale/tree/main/docs/modules/nfs_alias.rst)
  * [Settings Module](https://github.com/dell/ansible-powerscale/tree/main/docs/modules/settings.rst)
  * [Network Setting Module](https://github.com/dell/ansible-powerscale/blob/main/docs/modules/networksettings.rst)
  * [Smart Pool Setting Module](https://github.com/dell/ansible-powerscale/blob/main/docs/modules/smartpoolsettings.rst)
  * [Filepool Policy Module](https://github.com/dell/ansible-powerscale/blob/main/docs/modules/filepoolpolicy.rst)
  * [Storagepool Tier Module](https://github.com/dell/ansible-powerscale/blob/main/docs/modules/storagepooltier.rst)
  * [SMB File Module](https://github.com/dell/ansible-powerscale/blob/main/docs/modules/smb_file.rst)
  * [User Mapping Rule Module](https://github.com/dell/ansible-powerscale/blob/main/docs/modules/user_mapping_rule.rst)
  * [S3 Bucket Module](https://github.com/dell/ansible-powerscale/blob/main/docs/modules/s3_bucket.rst)
  * [NFS Default Settings Module](https://github.com/dell/ansible-powerscale/blob/main/docs/modules/nfs_default_settings.rst)
  * [NFS Global Settings Module](https://github.com/dell/ansible-powerscale/blob/main/docs/modules/nfs_global_settings.rst)
  * [NFS Zone Settings Module](https://github.com/dell/ansible-powerscale/blob/main/docs/modules/nfs_zone_settings.rst)
  * [SyncIQ Global Settings Module](https://github.com/dell/ansible-powerscale/blob/main/docs/modules/synciq_global_settings.rst)
  * [SyncIQ Certificate Module](https://github.com/dell/ansible-powerscale/blob/main/docs/modules/synciqcertificate.rst)
  * [SMB Global Settings Module](https://github.com/dell/ansible-powerscale/blob/main/docs/modules/smb_global_settings.rst)
  * [SNMP Settings Module](https://github.com/dell/ansible-powerscale/blob/main/docs/modules/snmp_settings.rst)
  * [Server Certificate Module](https://github.com/dell/ansible-powerscale/blob/main/docs/modules/server_certificate.rst)
  * [Roles](https://github.com/dell/ansible-powerscale/blob/main/docs/modules/roles.rst)


## Installation and execution of Ansible modules for Dell PowerScale
The installation and execution steps of Ansible modules for Dell PowerScale can be found [here](https://github.com/dell/ansible-powerscale/blob/main/docs/INSTALLATION.md).

## Maintenance
Ansible Modules for Dell Technologies PowerScale deprecation cycle is aligned with [Ansible](https://docs.ansible.com/ansible/latest/dev_guide/module_lifecycle.html).
