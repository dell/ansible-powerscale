# PowerScale Ansible Collection Support Matrix

## PowerScale Version Compatibility

| PowerScale Version | Status | Notes |
|--------------------|--------|-------|
| 9.5.x | ✅ Qualified | Fully qualified |
| 9.6.x | ✅ Qualified | Fully qualified |
| 9.7.x | ✅ Qualified | Fully qualified |
| 9.8.x | ✅ Qualified | Fully qualified |
| 9.9.x | ✅ Qualified | Fully qualified |
| 9.10.x | ✅ Qualified | Fully qualified |
| 9.11.x | ✅ Qualified | Fully qualified |
| 9.12.x | ✅ Qualified | Fully qualified |
| 9.13.x | ✅ Qualified | Fully qualified |
| 9.14.x | ✅ Qualified | Fully qualified |
| 9.15.x | ✅ Qualified | Fully qualified - OneFS 9.15.0.0 (Release, Build B_9_15_0_0_002(RELEASE)) |

## Module Compatibility

All 56 modules are qualified for PowerScale 9.15.x:

### Access & Identity
- accesszone
- ads
- group
- groupnet
- ldap
- role
- user
- user_mapping_rules

### File System & Storage
- filesystem
- filepoolpolicy
- smartpoolsettings
- smartquota
- storagepooltier

### Networking
- networkpool
- networkrule
- networksettings
- subnet

### Protocols - NFS
- nfs
- nfs_alias
- nfs_default_settings
- nfs_global_settings
- nfs_zone_settings

### Protocols - SMB
- smb
- smb_file
- smb_global_settings

### Protocols - S3
- s3_bucket
- s3_global_settings
- s3_key
- s3_zone_settings

### Protocols - SyncIQ
- synciqjobs
- synciqpolicy
- synciqreports
- synciqrules
- synciqtargetreports
- synciqcertificate
- synciq_global_settings

### Snapshots
- snapshot
- snapshotschedule
- writable_snapshots

### Jobs & Monitoring
- job
- job_event_info
- job_info
- job_policy
- job_report_info
- job_type_info

### Alerts & Notifications
- alert_channel
- alert_rule
- alert_settings

### Cluster Management
- cluster_services
- info
- ipmi
- node
- settings
- server_certificate
- snmp_settings
- support_assist

## SDK Compatibility

| SDK Version | PowerScale Version | Status |
|------------|-------------------|--------|
| isi_sdk_9_0_0 | 9.15.x | ✅ Qualified | 
| isi_sdk_9_10_0 | 9.15.x | ✅ Qualified (collection pins to SDK 9.10.0 for versions > 9.10) |

## Notes

- All modules tested against OneFS 9.15.0.0 (Release, Build B_9_15_0_0_002(RELEASE))
- SDK 9.0.0 successfully connects to OneFS 9.15 without version incompatibility errors
- Collection pins to SDK 9.10.0 for PowerScale versions > 9.10 for enhanced compatibility
- All modules support check mode for dry-run operations
- All modules maintain idempotency
- All modules follow SDL security guidelines with proper secret masking

## Qualification Date

- PowerScale 9.15: August 21, 2026
- ER-75000: Ansible PowerScale 9.15 Qualification
