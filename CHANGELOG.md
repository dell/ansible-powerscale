# v3.9.0 (Jun 27, 2025)

## Release Summary
This release supports modules mentioned in the Features section for Dell PowerScale.

## Features
- Support to manage RDMA for NFS global settings module on Powerscale 9.8 or later.
- Add `+` as a permission option for Role module.

## Enhancements
- Performs operator validation for all updates of User mapping rule module.
- Avoid to add duplicated trustee for File System module.
- Adapt to muliple PowerScale versions for Alert settings modules.
- Adapt to muliple PowerScale versions for Info modules.

## Bug Fixes
- Fix defect for Support assist module about gateway checking.


# v3.8.1 (May 19, 2025)

## Release Summary
This release addresses bug fixes to improve stability and user experience for Dell PowerScale.

## Features
N/A

## Enhancements
N/A

## Bug Fixes
- GitHub defect fixes for filesystem module. (Issues # 38, # 121 and # 174)


# v3.8.0 (Mar 28, 2025)

## Release Summary
This release addresses bug fixes to improve stability and user experience for Dell PowerScale.

## Features
N/A

## Enhancements
N/A

## Bug Fixes
- GitHub defect fixes networkpool module for unauthorized error (issue 133), smb share module return error (issue 138)
  and filesystem modules cannot delete non empty folders and returns invalid error message (issue 148).
- Internal defect fixes for the modules settings, snapshot, group, nfs, smb, smb_global_settings, alert_rule,
  filesystem, nfs_alias, synciqpolicy, ads and info.


# v3.7.0 (Dec 23, 2024)

## Release Summary
This release adds some minor changes and addresses bug fixes to improve stability and user experience for Dell PowerScale.

## Features
N/A

## Enhancements
- Added check and diff mode support for synciqpolicy module.

## Bug Fixes
- Fixed bugs for synciqpolicy module. (Issues #44 and #130)


# v3.6.0 (Nov 21, 2024)

## Release Summary
This release adds some minor changes to improve stability and user experience for Dell PowerScale.

## Features
N/A

## Enhancements
- Added diff mode support for NFS module.
- Fixed failure of listing support_assist details in info module for oneFS version 9.4.0 and below.

## Bug Fixes
N/A


# v3.5.0 (Oct 24, 2024)

## Release Summary
This release adds some minor changes to improve stability and user experience for Dell PowerScale.

## Features
N/A

## Enhancements
- Added support to make listing of SMB open files cluster aware.
- Added fix for making the ACL trustee zone-aware for filesystem module.

## Bug Fixes
N/A


# v3.4.0 (Sep 20, 2024)

## Release Summary
This release adds some minor changes to improve stability and user experience for Dell PowerScale.

## Features
N/A

## Enhancements
- ADS module has been enhanced to support the additional parameters.
- Added support to list all the paginated data for the users in Info module.
- NFS module is enhanced to remove masked paths in response and also added declarative approach of managing clients.

## Bug Fixes
N/A


# v3.3.0 (Aug 26, 2024)

## Release Summary
This release supports modules mentioned in the Features section for Dell PowerScale.

## Features
- dellemc.powerscale.alert_channel - Manage alert channel on a PowerScale Storage System.
- dellemc.powerscale.alert_rule - Manage alert rule on a PowerScale Storage System.
- dellemc.powerscale.writable_snapshots - Manage writable snapshots on PowerScale Storage System.

## Enhancements
- Added fix for firewall policy issue for network pool operations.
- Added support for listing writable snapshots in Info module.

## Bug Fixes
N/A


# v3.2.0 (Jul 31, 2024)

## Release Summary
This release supports modules mentioned in the Features section for Dell PowerScale.

## Features
- dellemc.powerscale.alert_settings - Manage alert settings on a PowerScale Storage System.

## Enhancements
- Added support for check mode and diff mode in network pool module.
- Added support for check mode in Filesystem, NFS and Smart Quota modules.
- Added support for listing filesystems, smart quotas, alert_settings, alert_rules, alert_categories, event_groups and alert_channels in Info module.
- Added support for query parameters and filters in Info module.

## Bug Fixes
N/A


# v3.1.0 (Jun 24, 2024)

## Release Summary
This release supports modules mentioned in the Features section for Dell PowerScale.

## Features
- dellemc.powerscale.roles - Manage auth roles on a PowerScale Storage System.
- dellemc.powerscale.support_assist - Manage support assist settings on a PowerScale Storage System.

## Enhancements
- Added support for OneFS 9.8 Lonestar release.
- Added support for running as root, along with other boolean flags such as allow_delete_readonly, allow_execute_always, and inheritable_path_acl in SMB module.

## Bug Fixes
N/A


# v3.0.0 (Mar 26, 2024)

## Release Summary
This release supports modules mentioned in the Features section for Dell PowerScale.

## Features
- Added support for OneFS 9.7 Key West release.

## Enhancements
N/A

## Bug Fixes
N/A


# v2.5.0 (Feb 27, 2024)

## Release Summary
This release supports modules mentioned in the Features section for Dell PowerScale.

## Features
- dellemc.powerscale.server_certificate - Manage server certificates on a PowerScale Storage System.

## Enhancements
- Added support for listing server certificates in Info module.

## Bug Fixes
N/A


# v2.4.1 (Dec 27, 2023)

## Release Summary
This release adds some minor changes to improve stability and user experience for Dell PowerScale.

## Features
N/A

## Enhancements
- Document link fixes in README.

## Bug Fixes
N/A


# v2.4.0 (Dec 26, 2023)

## Release Summary
This release supports modules mentioned in the Features section for Dell PowerScale.

## Features
- dellemc.powerscale.smb_global_settings - Manage SMB global settings on a PowerScale Storage System.
- dellemc.powerscale.snmp_settings - Manage SNMP settings on a PowerScale Storage System.

## Enhancements
- Added support for getting and modifying cluster owner information and cluster identity information through settings module.
- Added support for listing SMB global settings, detailed network interfaces, NTP servers, email settings, cluster identity, cluster owner and SNMP settings through info module.
- Added support for removing the static route for IP address pool through network pool module.

## Bug Fixes
N/A


# v2.3.0 (Nov 29, 2023)

## Release Summary
This release supports modules mentioned in the Features section for Dell PowerScale.

## Features
- dellemc.powerscale.synciq_global_settings - Manage SyncIQ global settings on a PowerScale Storage System.
- dellemc.powerscale.synciqcertificate - Manage SyncIQ target cluster certificate on a PowerScale Storage System.

## Enhancements
- Added support for listing SynciqGlobalSettings and S3 buckets in Info module.
- Added support for manually running a SyncIQ policy.

## Bug Fixes
N/A


# v2.2.0 (Aug 29, 2023)

## Release Summary
This release supports modules mentioned in the Features section for Dell PowerScale.

## Features
- dellemc.powerscale.nfs_default_settings - Get details and modify NFS default settings.
- dellemc.powerscale.nfs_global_settings - Get details and modify NFS global settings.
- dellemc.powerscale.nfs_zone_settings - Get details and modify NFS zone settings.

## Enhancements
- Added support for listing NFS default settings, NFS global settings and NFS zone settings in Info module.
- Added support for specifying the users and groups to which non-root and root clients are mapped in nfs module.

## Bug Fixes
N/A


# v2.1.0 (Jul 28, 2023)

## Release Summary
This release supports modules mentioned in the Features section for Dell PowerScale.

## Features
- dellemc.powerscale.s3_bucket - Create, modify, get details and delete an S3 bucket.

## Enhancements
- Added support for SmartConnect zone alaises(DNS names) in network pool module.
- Added support for deleting an access zone and reordering the authentication providers in access zone module.
- Added support for service principal names(SPN) in AD module.

## Bug Fixes
N/A


# v2.0.0 (Jun 28, 2023)

## Release Summary
This release supports modules mentioned in the Features section for Dell PowerScale.

## Features
- dellemc.powerscale.user_mapping_rule - Create, modify, get details, and delete a user mapping rule.

## Enhancements
- Added support for PowerScale OneFS 9.5 Islander release.
- Added support for everyone user in filesystem module.
- Added support for ignoring unresolvable hosts for NFS Export.
- Added support for listing LDAP auth providers and user mapping rules in Info module.
- For the execution of the PowerScale Ansible modules, python library "isilon-sdk" needs to be installed.

## Bug Fixes
N/A


# v1.9.0 (Mar 28, 2023)

## Release Summary
This release supports modules mentioned in the Features section for Dell PowerScale.

## Features
- dellemc.powerscale.smb_file - Find and close SMB open files on a PowerScale Storage system.

## Enhancements
- Added support to create a group using group_id.
- Added support to create a user using user_id.
- Added support to list SMB open files through Info module.
- Added support to update the password of the user.
- Enabled the path parameter of Smart Quota module to be consistent with other modules.

## Bug Fixes
N/A


# v1.8.0 (Dec 14, 2022)

## Release Summary
This release adds some minor changes to improve stability and user experience for Dell PowerScale.

## Features
N/A

## Enhancements
- Added support for security flavors while creating and modifying NFS export.

## Bug Fixes
N/A


# v1.7.0 (Sep 22, 2022)

## Release Summary
This release supports modules mentioned in the Features section for Dell PowerScale.

## Features
- dellemc.powerscale.nfs_alias - Manage NFS aliases on a PowerScale Storage System

## Enhancements
- Access Zone, SMB, SmartQuota, User and Group module is enhanced to support NIS authentication provider.
- Info module is enhanced to support listing of NFS aliases.
- Support to create and modify additional parameters of an SMB share in SMB module.
- SyncIQ Policy module is enhanced to support accelerated_failback and restrict_target_network of a policy.

## Bug Fixes
N/A


# v1.6.0 (Jun 21, 2022)

## Release Summary
This release supports modules mentioned in the Features section for Dell PowerScale.

## Features
- dellemc.powerscale.filepoolpolicy - Manages file pool policy on PowerScale
- dellemc.powerscale.storagepooltier - Manages storage pool tier on PowerScale

## Enhancements
- Added execution environment manifest file to support building an execution environment with ansible-builder.
- Added files required for Ansible execution environment.
- Check mode is supported for Info, Filepool Policy and Storagepool Tier modules.
- Filesystem module is enhanced to support ACL and container parameter.
- Info module is enhanced to support NodePools and Storagepool Tiers Subsets.
- SmartQuota module is enhanced to support container parameter.

## Bug Fixes
N/A


# v1.5.0 (Mar 21, 2022)

## Release Summary
This release supports modules mentioned in the Features section for Dell PowerScale.

## Features
- dellemc.powerscale.networksettings - Manages Network Settings on PowerScale Storage System
- dellemc.powerscale.smartpoolsettings - Manages Smartpool Settings on PowerScale Storage System

## Enhancements
- ADS module is enhanced to support machine_account and organizational_unit parameters while creating ADS provider.
- Added rotating file handler for log files.
- Removal of dellemc_powerscale prefix from all the modules name.
- SmartQuota module is enhanced to support float values for Quota Parameters.
- Support for recursive force deletion of filesystem directories.

## Bug Fixes
N/A


# v1.4.0 (Dec 10, 2021)

## Release Summary
This release supports modules mentioned in the Features section for Dell PowerScale.

## Features
- dellemc.powerscale.groupnet - Manages groupnet configuration on PowerScale
- dellemc.powerscale.networkpool - Manages Network Pools on PowerScale Storage System
- dellemc.powerscale.networkrule - Manages Network provisioning rules for PowerScale Storage System
- dellemc.powerscale.settings - Manages general settings for PowerScale storage system
- dellemc.powerscale.subnet - Manages subnet configuration on PowerScale

## Enhancements
- Access zone module is enhanced to support creation of an access zone.
- Gather facts module is enhanced to list network groupnets, network subnets, network pools, network rules and network interfaces.
- Support to retrieve and modify email settings in Settings module.
- Support to retrieve, add and remove NTP servers in Settings module.

## Bug Fixes
N/A


# v1.3.0 (Sep 22, 2021)

## Release Summary
This release supports modules mentioned in the Features section for Dell PowerScale.

## Features
- dellemc.powerscale.synciqjob - Manage SyncIQ jobs on PowerScale
- dellemc.powerscale.synciqpolicy - Manage SyncIQ policies on PowerScale
- dellemc.powerscale.synciqreports - Provides the SyncIQ reports for PowerScale Storage System
- dellemc.powerscale.synciqrules - Manage SyncIQ performance rules on PowerScale Storage System.
- dellemc.powerscale.synciqtargetreports - Provides SyncIQ target reports on PowerScale Storage System

## Enhancements
- Added dual licensing.
- Gather facts module is enhanced to list SyncIQ policies, SyncIQ Performance rules, SyncIQ reports, SyncIQ target reports, SyncIQ target cluster certificates.

## Bug Fixes
N/A


# v1.2.0 (Jun 25, 2021)

## Release Summary
This release supports modules mentioned in the Features section for Dell PowerScale.

## Features
- dellemc.powerscale.ads - Manages the ADS authentication provider on PowerScale
- dellemc.powerscale.ldap - Manage LDAP authentication provider on PowerScale
- dellemc.powerscale.node - Get node info of PowerScale Storage System.

## Enhancements
- Filesystem module is enhanced to support additional quota parameters.
- Gather facts module is enhanced to list Nodes, NFS Exports, SMB shares and Active clients.
- Map or unmap authentication providers to/from an access zone.
- Rebranded Isilon to PowerScale.
- SmartQuota module is enhanced to support CRUD operations, for default-user and default-group quotas.
- Support extended for OneFS version 9.1.0.

## Bug Fixes
N/A


# v1.1.0 (Jun 25, 2021)

## Release Summary
This release supports modules mentioned in the Features section for Dell PowerScale.

## Features
- dellemc.powerscale.ads - Manages the ADS authentication provider on PowerScale
- dellemc.powerscale.ldap - Manage LDAP authentication provider on PowerScale
- dellemc.powerscale.node - Get node info of PowerScale Storage System.

## Enhancements
- Filesystem module is enhanced to support additional quota parameters.
- Gather facts module is enhanced to list Nodes, NFS Exports, SMB shares and Active clients.
- Map or unmap authentication providers to/from an access zone.
- Rebranded Isilon to PowerScale.
- SmartQuota module is enhanced to support CRUD operations, for default-user and default-group quotas.
- Support extended for OneFS version 9.1.0.

## Bug Fixes
N/A


# v1.1.0

## Release Summary
This release supports modules mentioned in the Features section for Dell PowerScale.

## Features
- dellemc.powerscale.smartquota - Manage Smart Quotas on PowerScale

## Enhancements
N/A

## Bug Fixes
N/A


# v1.0.0

## Release Summary
This release supports modules mentioned in the Features section for Dell PowerScale.

## Features
- dellemc.powerscale.accesszone - Manages access zones on PowerScale
- dellemc.powerscale.filesystem - Manage Filesystems on PowerScale
- dellemc.powerscale.group - Manage Groups on the PowerScale Storage System
- dellemc.powerscale.info - Gathering information about PowerScale Storage
- dellemc.powerscale.nfs - Manage NFS exports on a PowerScale Storage System
- dellemc.powerscale.smb - Manage SMB shares on PowerScale Storage System. You can perform these operations
- dellemc.powerscale.snapshot - Manage snapshots on PowerScale
- dellemc.powerscale.snapshotschedule - Manage snapshot schedules on PowerScale
- dellemc.powerscale.user - Manage users on the PowerScale Storage System

## Enhancements
N/A

## Bug Fixes
N/A
