================================
Dellemc.Powerscale Change Logs
================================

.. contents:: Topics


v1.9.0
======

Minor Changes
-------------

- Added support to create a group using group_id.
- Added support to create a user using user_id.
- Added support to list SMB open files through Info module.
- Added support to update the password of the user.
- Enabled the path parameter of Smart Quota module to be consistent with other modules.

New Modules
-----------

- dellemc.powerscale.smb_file - Find and close SMB open files on a PowerScale Storage system.

v1.8.0
======

Minor Changes
-------------

- Added support for security flavors while creating and modifying NFS export.

v1.7.0
======

Minor Changes
-------------

- Access Zone, SMB, SmartQuota, User and Group module is enhanced to support NIS authentication provider.
- Info module is enhanced to support listing of NFS aliases.
- Support to create and modify additional parameters of an SMB share in SMB module.
- SyncIQ Policy module is enhanced to support accelerated_failback and restrict_target_network of a policy.

New Modules
-----------

- dellemc.powerscale.nfs_alias - Manage NFS aliases on a PowerScale Storage System

v1.6.0
======

Minor Changes
-------------

- Added execution environment manifest file to support building an execution environment with ansible-builder.
- Added files required for Ansible execution environment.
- Check mode is supported for Info, Filepool Policy and Storagepool Tier modules.
- Filesystem module is enhanced to support ACL and container parameter.
- Info module is enhanced to support NodePools and Storagepool Tiers Subsets.
- SmartQuota module is enhanced to support container parameter.

New Modules
-----------

- dellemc.powerscale.filepoolpolicy - Manages file pool policy on PowerScale
- dellemc.powerscale.storagepooltier - Manages storage pool tier on PowerScale

v1.5.0
======

Minor Changes
-------------

- ADS module is enhanced to support machine_account and organizational_unit parameters while creating ADS provider.
- Added rotating file handler for log files.
- Removal of dellemc_powerscale prefix from all the modules name.
- SmartQuota module is enhanced to support float values for Quota Parameters.
- Support for recursive force deletion of filesystem directories.

New Modules
-----------

- dellemc.powerscale.networksettings - Manages Network Settings on PowerScale Storage System
- dellemc.powerscale.smartpoolsettings - Manages Smartpool Settings on PowerScale Storage System

v1.4.0
======

Minor Changes
-------------

- Access zone module is enhanced to support creation of an access zone.
- Gather facts module is enhanced to list network groupnets, network subnets, network pools, network rules and network interfaces.
- Support to retrieve and modify email settings in Settings module.
- Support to retrieve, add and remove NTP servers in Settings module.

New Modules
-----------

- dellemc.powerscale.groupnet - Manages groupnet configuration on PowerScale
- dellemc.powerscale.networkpool - Manages Network Pools on PowerScale Storage System
- dellemc.powerscale.networkrule - Manages Network provisioning rules for PowerScale Storage System
- dellemc.powerscale.settings - Manages general settings for PowerScale storage system
- dellemc.powerscale.subnet - Manages subnet configuration on PowerScale

v1.3.0
======

Minor Changes
-------------

- Added dual licensing.
- Gather facts module is enhanced to list SyncIQ policies, SyncIQ Performance rules, SyncIQ reports, SyncIQ target reports, SyncIQ target cluster certificates.

New Modules
-----------

- dellemc.powerscale.synciqjob - Manage SyncIQ jobs on PowerScale
- dellemc.powerscale.synciqpolicy - Manage SyncIQ policies on PowerScale
- dellemc.powerscale.synciqreports - Provides the SyncIQ reports for PowerScale Storage System
- dellemc.powerscale.synciqrules - Manage SyncIQ performance rules on PowerScale Storage System.
- dellemc.powerscale.synciqtargetreports - Provides SyncIQ target reports on PowerScale Storage System

v1.2.0
======

Minor Changes
-------------

- Filesystem module is enhanced to support additional quota parameters.
- Gather facts module is enhanced to list Nodes, NFS Exports, SMB shares and Active clients.
- Map or unmap authentication providers to/from an access zone.
- Rebranded Isilon to PowerScale.
- SmartQuota module is enhanced to support CRUD operations, for default-user and default-group quotas.
- Support extended for OneFS version 9.1.0.

New Modules
-----------

- dellemc.powerscale.ads - Manages the ADS authentication provider on PowerScale
- dellemc.powerscale.ldap - Manage LDAP authentication provider on PowerScale
- dellemc.powerscale.node - Get node info of PowerScale Storage System.

v1.1.0
======

New Modules
-----------

- dellemc.powerscale.smartquota - Manage Smart Quotas on PowerScale

v1.0.0
======

New Modules
-----------

- dellemc.powerscale.accesszone - Manages access zones on PowerScale
- dellemc.powerscale.filesystem - Manage Filesystems on PowerScale
- dellemc.powerscale.group - Manage Groups on the PowerScale Storage System
- dellemc.powerscale.info - Gathering information about PowerScale Storage
- dellemc.powerscale.nfs - Manage NFS exports on a PowerScale Storage System
- dellemc.powerscale.smb - Manage SMB shares on PowerScale Storage System. You can perform these operations
- dellemc.powerscale.snapshot - Manage snapshots on PowerScale
- dellemc.powerscale.snapshotschedule - Manage snapshot schedules on PowerScale
- dellemc.powerscale.user - Manage users on the PowerScale Storage System
