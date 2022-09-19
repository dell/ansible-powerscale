# ansible-powerscale Change Log
## Version 1.7.0 - released on 27/09/22
- Support to retrieve, create, modify and delete NFS alias in NFS Alias module.
- Support to create and modify additional parameters of an SMB share in SMB module.
- Access Zone, SMB, SmartQuota, User and Group module is enhanced to support NIS authentication provider.
- SyncIQ Policy module is enhanced to support accelerated_failback and restrict_target_network of a policy.
- Info module is enhanced to support listing of NFS aliases.

## Version 1.6.0 - released on 28/06/22
- Support to retrieve, create and delete filepool policy in Filepool Policy module.
- Support to retrieve, create and delete storagetier in Storagepool Tier module.
- SmartQuota module is enhanced to support container parameter.
- Filesystem module is enhanced to support ACL and container parameter.
- Info module is enhanced to support NodePools and Storagepool Tiers Subsets.
- Added files required for Ansible execution environment.
- Check mode is supported for Info, Filepool Policy and Storagepool Tier modules.
- Added execution environment manifest file to support building an execution environment with ansible-builder.

## Version 1.5.0 - released on 25/03/22
- Support to retrieve and modify network settings in Network Settings module.
- Support to retrieve and modify smartpool settings in Smartpool Settings module.
- SmartQuota module is enhanced to support float values for Quota Parameters.
- ADS module is enhanced to support machine_account & organizational_unit parameters while creating ADS provider.
- Removal of dellemc_powerscale prefix from all the modules name.
- Support for recursive force deletion of filesystem directories.
- Added rotating file handler for log files.

## Version 1.4.0 - released on 16/12/21
- Added CRUD operations for Groupnet module.
- Added CRUD operations for Subnet module.
- Added CRUD operations for Network Pool module.
- Added CRUD operations for Network Rule module.
- Support to retrieve and modify email settings in Settings module.
- Support to retrieve, add and remove NTP servers in Settings module.
- Access zone module is enhanced to support creation of an access zone.
- Gather facts module is enhanced to list network groupnets, network subnets, network pools, network rules and network interfaces.

## Version 1.3.0 - released on 23/09/21
- Added CRUD operations for SyncIQ Policy module.
- Added CRUD operations for SyncIQ Performance Rule module.
- Added support to create a job for SyncIQ Policy module.
- Support to retrieve and modify details of a SyncIQ job in SyncIQ jobs module.
- Support to fetch details of a SyncIQ report and all sub-reports in SyncIQ report module.
- Support to fetch details of a SyncIQ target report and all target sub-reports in SyncIQ report module.
- Gather facts module is enhanced to list SyncIQ policies, SyncIQ Performance rules, SyncIQ reports, SyncIQ target reports, SyncIQ target cluster certificates. 
- Added dual licensing

## Version 1.2.0 - released on 25/06/21
- Map or unmap authentication providers to/from an access zone
- Support extended for OneFS version 9.1.0.
- Filesystem module is enhanced to support additional quota parameters.
- Added CRUD operations support for Active Directory module.
- Added CRUD operations support for LDAP module.
- Added support for getting details of a Node.
- Gather facts module is enhanced to list Nodes, NFS Exports, SMB shares and Active clients.
- SmartQuota module is enhanced to support CRUD operations for default-user and default-group quotas.
- Rebranded Isilon to PowerScale.

## Version 1.1.0 - released on 12/06/20
- Added CRUD operations support for UserQuota and GroupQuota as part of SmartQuota module.

## Version 1.0.0 - released on 19/03/20
- Added CRUD operations support for local user in User module. This also supports adding/removing roles for users of all provider types in system access zone. Also supports getting details of local/AD/LDAP/File users.
- Added CRUD operations support for local group in Group module. This also supports adding/removing local users from local groups. Also supports getting details of local/AD/LDAP/File group.
- Added CRUD operations support for File system. This also supports create/modify File system with Quota parameters.
- Added support to retrieve details of the access zone.
- Added support to modify default settings of SMB share and NFS export using AccessZone module.
- Added CRUD operations support for NFS export.
- Added CRUD operations support for SMB share.
- Added CRUD operations support for the snapshot.
- Added CRUD operations support for the snapshot schedule.
- Added Gather facts module to list Attributes, Access_zone, Nodes, Providers, Users and Groups.