# ansible-powerscale Change Log
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