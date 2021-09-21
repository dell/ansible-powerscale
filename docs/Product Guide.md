# Ansible Modules for Dell EMC PowerScale
## Product Guide 1.3.0
© 2021 Dell Inc. or its subsidiaries. All rights reserved. Dell, EMC, and other trademarks are trademarks of Dell Inc. or its subsidiaries. Other trademarks may be trademarks of their respective owners.

--------------
## Contents
*   [LDAP Module](#ldap-module)
    *   [Synopsis](#synopsis)
    *   [Parameters](#parameters)
    *   [Notes](#notes)
    *   [Examples](#examples)
    *   [Return Values](#return-values)
    *   [Authors](#authors)
*   [SyncIQ Reports Module](#synciq-reports-module)
    *   [Synopsis](#synopsis-1)
    *   [Parameters](#parameters-1)
    *   [Examples](#examples-1)
    *   [Return Values](#return-values-1)
    *   [Authors](#authors-1)
*   [Smart Quota Module](#smart-quota-module)
    *   [Synopsis](#synopsis-2)
    *   [Parameters](#parameters-2)
    *   [Notes](#notes-1)
    *   [Examples](#examples-2)
    *   [Return Values](#return-values-2)
    *   [Authors](#authors-2)
*   [SyncIQ Target Reports Module](#synciq-target-reports-module)
    *   [Synopsis](#synopsis-3)
    *   [Parameters](#parameters-3)
    *   [Examples](#examples-3)
    *   [Return Values](#return-values-3)
    *   [Authors](#authors-3)
*   [ADS Module](#ads-module)
    *   [Synopsis](#synopsis-4)
    *   [Parameters](#parameters-4)
    *   [Examples](#examples-4)
    *   [Return Values](#return-values-4)
    *   [Authors](#authors-4)
*   [Snapshot Schedule Module](#snapshot-schedule-module)
    *   [Synopsis](#synopsis-5)
    *   [Parameters](#parameters-5)
    *   [Examples](#examples-5)
    *   [Return Values](#return-values-5)
    *   [Authors](#authors-5)
*   [User Module](#user-module)
    *   [Synopsis](#synopsis-6)
    *   [Parameters](#parameters-6)
    *   [Examples](#examples-6)
    *   [Return Values](#return-values-6)
    *   [Authors](#authors-6)
*   [SMB Module](#smb-module)
    *   [Synopsis](#synopsis-7)
    *   [Parameters](#parameters-7)
    *   [Examples](#examples-7)
    *   [Return Values](#return-values-7)
    *   [Authors](#authors-7)
*   [Snapshot Module](#snapshot-module)
    *   [Synopsis](#synopsis-8)
    *   [Parameters](#parameters-8)
    *   [Examples](#examples-8)
    *   [Return Values](#return-values-8)
    *   [Authors](#authors-8)
*   [SyncIQ Performance Rules Module](#synciq-performance-rules-module)
    *   [Synopsis](#synopsis-9)
    *   [Parameters](#parameters-9)
    *   [Notes](#notes-2)
    *   [Examples](#examples-9)
    *   [Return Values](#return-values-9)
    *   [Authors](#authors-9)
*   [Accesszone Module](#accesszone-module)
    *   [Synopsis](#synopsis-10)
    *   [Parameters](#parameters-10)
    *   [Notes](#notes-3)
    *   [Examples](#examples-10)
    *   [Return Values](#return-values-10)
    *   [Authors](#authors-10)
*   [SyncIQ Job Module](#synciq-job-module)
    *   [Synopsis](#synopsis-11)
    *   [Parameters](#parameters-11)
    *   [Notes](#notes-4)
    *   [Examples](#examples-11)
    *   [Return Values](#return-values-11)
    *   [Authors](#authors-11)
*   [NFS Module](#nfs-module)
    *   [Synopsis](#synopsis-12)
    *   [Parameters](#parameters-12)
    *   [Examples](#examples-12)
    *   [Return Values](#return-values-12)
    *   [Authors](#authors-12)
*   [SyncIQ Policy Module](#synciq-policy-module)
    *   [Synopsis](#synopsis-13)
    *   [Parameters](#parameters-13)
    *   [Notes](#notes-5)
    *   [Examples](#examples-13)
    *   [Return Values](#return-values-13)
    *   [Authors](#authors-13)
*   [Group Module](#group-module)
    *   [Synopsis](#synopsis-14)
    *   [Parameters](#parameters-14)
    *   [Examples](#examples-14)
    *   [Return Values](#return-values-14)
    *   [Authors](#authors-14)
*   [File System Module](#file-system-module)
    *   [Synopsis](#synopsis-15)
    *   [Parameters](#parameters-15)
    *   [Examples](#examples-15)
    *   [Return Values](#return-values-15)
    *   [Authors](#authors-15)

--------------

# LDAP Module

Manage LDAP authentication provider on PowerScale

### Synopsis
 Managing LDAP authentication provider on PowerScale storage system includes creating, modifying, deleting and retrieving details of LDAP provider.

### Parameters
                                                                                                                                                                                                                                                                                                                    
<table>
    <tr>
        <th colspan=2>Parameter</th>
        <th width="20%">Type</th>
        <th>Required</th>
        <th>Default</th>
        <th>Choices</th>
        <th width="80%">Description</th>
    </tr>
                                                            <tr>
            <td colspan=2 > ldap_name</td>
            <td> str  </td>
            <td> True </td>
            <td></td>
            <td></td>
            <td> <br> Specifies the name of the LDAP provider. </td>
        </tr>
                    <tr>
            <td colspan=2 > server_uris</td>
            <td> list   <br> elements: str </td>
            <td></td>
            <td></td>
            <td></td>
            <td> <br> Specifies the server URIs.  <br> This parameter is mandatory during create.  <br> Server_uris should begin with ldap:// or ldaps:// if not validation error will be displayed. </td>
        </tr>
                    <tr>
            <td colspan=2 > server_uri_state</td>
            <td> str  </td>
            <td></td>
            <td></td>
            <td> <ul> <li>present-in-ldap</li>  <li>absent-in-ldap</li> </ul></td>
            <td> <br> Specifies if the server_uris need to be added or removed from the provider.  <br> This parameter is mandatory if server_uris is specified.  <br> While creating LDAP provider, this parameter value should be specified as 'present-in-ldap'. </td>
        </tr>
                    <tr>
            <td colspan=2 > base_dn</td>
            <td> str  </td>
            <td></td>
            <td></td>
            <td></td>
            <td> <br> Specifies the root of the tree in which to search identities.  <br> This parameter is mandatory during create. </td>
        </tr>
                    <tr>
            <td colspan=2 > ldap_parameters</td>
            <td> dict  </td>
            <td></td>
            <td></td>
            <td></td>
            <td> <br> Specify additional parameters to configure LDAP domain. </td>
        </tr>
                            <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > groupnet </td>
                <td> str  </td>
                <td></td>
                <td></td>
                <td></td>
                <td>  <br> Groupnet identifier.  <br> This is an optional parameter and defaults to groupnet0.  </td>
            </tr>
                    <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > bind_dn </td>
                <td> str  </td>
                <td></td>
                <td></td>
                <td></td>
                <td>  <br> Specifies the distinguished name for binding to the LDAP server.  </td>
            </tr>
                    <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > bind_password </td>
                <td> str  </td>
                <td></td>
                <td></td>
                <td></td>
                <td>  <br> Specifies the password for the distinguished name for binding to the LDAP server.  </td>
            </tr>
                            <tr>
            <td colspan=2 > state</td>
            <td> str  </td>
            <td> True </td>
            <td></td>
            <td> <ul> <li>absent</li>  <li>present</li> </ul></td>
            <td> <br> The state of the LDAP provider after the task is performed.  <br> present - indicates that the LDAP provider should exist on the system.  <br> absent - indicates that the LDAP provider should not exist on the system. </td>
        </tr>
                    <tr>
            <td colspan=2 > onefs_host</td>
            <td> str  </td>
            <td> True </td>
            <td></td>
            <td></td>
            <td> <br> IP address or FQDN of the PowerScale cluster. </td>
        </tr>
                    <tr>
            <td colspan=2 > port_no</td>
            <td> str  </td>
            <td></td>
            <td> 8080 </td>
            <td></td>
            <td> <br> Port number of the PowerScale cluster.It defaults to 8080 if not specified. </td>
        </tr>
                    <tr>
            <td colspan=2 > verify_ssl</td>
            <td> bool  </td>
            <td> True </td>
            <td></td>
            <td> <ul> <li>True</li>  <li>False</li> </ul></td>
            <td> <br> boolean variable to specify whether to validate SSL certificate or not.  <br> True - indicates that the SSL certificate should be verified.  <br> False - indicates that the SSL certificate should not be verified. </td>
        </tr>
                    <tr>
            <td colspan=2 > api_user</td>
            <td> str  </td>
            <td> True </td>
            <td></td>
            <td></td>
            <td> <br> username of the PowerScale cluster. </td>
        </tr>
                    <tr>
            <td colspan=2 > api_password</td>
            <td> str  </td>
            <td> True </td>
            <td></td>
            <td></td>
            <td> <br> the password of the PowerScale cluster. </td>
        </tr>
                                                    </table>

### Notes
* This module does not support modification of bind_password of LDAP provider. The value specified for bind_password will be ignored during modify.

### Examples
```
- name: Add an LDAP provider
  dellemc_powerscale_ldap:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      ldap_name: "ldap_test"
      server_uris:
        - "{{server_uri_1}}"
        - "{{server_uri_2}}"
      server_uri_state: 'present-in-ldap'
      base_dn: "DC=ansildap,DC=com"
      ldap_parameters:
        groupnet: "groupnet_ansildap"
        bind_dn: "cn=admin,dc=example,dc=com"
        bind_password: "{{bind_password}}"
      state: "present"

- name: Add server_uris to an LDAP provider
  dellemc_powerscale_ldap:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      ldap_name: "ldap_test"
      server_uris:
        - "{{server_uri_1}}"
      server_uri_state: "present-in-ldap"
      state: "present"

- name: Remove server_uris from an LDAP provider
  dellemc_powerscale_ldap:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      ldap_name: "ldap_test"
      server_uris:
        - "{{server_uri_1}}"
      server_uri_state: "absent-in-ldap"
      state: "present"

- name: Modify LDAP provider
  dellemc_powerscale_ldap:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      ldap_name: "ldap_test"
      base_dn: "DC=ansi_ldap,DC=com"
      ldap_parameters:
        bind_dn: "cn=admin,dc=test,dc=com"
      state: "present"

- name: Get LDAP provider details
  dellemc_powerscale_ldap:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      ldap_name: "ldap_test"
      state: "present"

- name: Delete a LDAP provider
  dellemc_powerscale_ldap:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      ldap_name: "ldap_test"
      state: "absent"
```

### Return Values
                                                                                                                                                                                                                                                                                    
<table>
    <tr>
        <th colspan=2>Key</th>
        <th>Type</th>
        <th>Returned</th>
        <th width="100%">Description</th>
    </tr>
                                                                                            <tr>
            <td colspan=2 > changed </td>
            <td>  bool </td>
            <td> always </td>
            <td> Whether or not the resource has changed </td>
        </tr>
                    <tr>
            <td colspan=2 > ldap_provider_details </td>
            <td>  complex </td>
            <td> When LDAP provider exists </td>
            <td> The LDAP provider details </td>
        </tr>
                            <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > base_dn </td>
                <td> str </td>
                <td>success</td>
                <td> Specifies the root of the tree in which to search identities. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > bind_dn </td>
                <td> str </td>
                <td>success</td>
                <td> Specifies the distinguished name for binding to the LDAP server. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > groupnet </td>
                <td> str </td>
                <td>success</td>
                <td> Groupnet identifier. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > linked_access_zones </td>
                <td> list </td>
                <td>success</td>
                <td> List of access zones linked to the authentication provider. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > name </td>
                <td> str </td>
                <td>success</td>
                <td> Specifies the name of the LDAP provider. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > server_uris </td>
                <td> str </td>
                <td>success</td>
                <td> Specifies the server URIs. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > status </td>
                <td> str </td>
                <td>success</td>
                <td> Specifies the status of the provider. </td>
            </tr>
                                        </table>

### Authors
* Jennifer John (@johnj9) <ansible.team@dell.com>

--------------------------------
# SyncIQ Reports Module

Provides the SyncIQ reports for PowerScale Storage System

### Synopsis
 This module provides the SyncIQ reports for PowerScale Storage System.

### Parameters
                                                                                                                                                                                                                                                    
<table>
    <tr>
        <th colspan=1>Parameter</th>
        <th width="20%">Type</th>
        <th>Required</th>
        <th>Default</th>
        <th>Choices</th>
        <th width="80%">Description</th>
    </tr>
                                                            <tr>
            <td colspan=1 > id</td>
            <td> str  </td>
            <td></td>
            <td></td>
            <td></td>
            <td> <br> The id of the SyncIQ report. </td>
        </tr>
                    <tr>
            <td colspan=1 > name</td>
            <td> str  </td>
            <td></td>
            <td></td>
            <td></td>
            <td> <br> The name of the SyncIQ report. </td>
        </tr>
                    <tr>
            <td colspan=1 > sub_report_id</td>
            <td> str  </td>
            <td></td>
            <td></td>
            <td></td>
            <td> <br> The id of the SyncIQ sub report. </td>
        </tr>
                    <tr>
            <td colspan=1 > include_sub_reports</td>
            <td> bool  </td>
            <td></td>
            <td> False </td>
            <td></td>
            <td> <br> This flag is used to fetch the list of sub reports. </td>
        </tr>
                    <tr>
            <td colspan=1 > state</td>
            <td> str  </td>
            <td> True </td>
            <td></td>
            <td> <ul> <li>absent</li>  <li>present</li> </ul></td>
            <td> <br> The state option is used to mention the existence of reports. </td>
        </tr>
                    <tr>
            <td colspan=1 > onefs_host</td>
            <td> str  </td>
            <td> True </td>
            <td></td>
            <td></td>
            <td> <br> IP address or FQDN of the PowerScale cluster. </td>
        </tr>
                    <tr>
            <td colspan=1 > port_no</td>
            <td> str  </td>
            <td></td>
            <td> 8080 </td>
            <td></td>
            <td> <br> Port number of the PowerScale cluster.It defaults to 8080 if not specified. </td>
        </tr>
                    <tr>
            <td colspan=1 > verify_ssl</td>
            <td> bool  </td>
            <td> True </td>
            <td></td>
            <td> <ul> <li>True</li>  <li>False</li> </ul></td>
            <td> <br> boolean variable to specify whether to validate SSL certificate or not.  <br> True - indicates that the SSL certificate should be verified.  <br> False - indicates that the SSL certificate should not be verified. </td>
        </tr>
                    <tr>
            <td colspan=1 > api_user</td>
            <td> str  </td>
            <td> True </td>
            <td></td>
            <td></td>
            <td> <br> username of the PowerScale cluster. </td>
        </tr>
                    <tr>
            <td colspan=1 > api_password</td>
            <td> str  </td>
            <td> True </td>
            <td></td>
            <td></td>
            <td> <br> the password of the PowerScale cluster. </td>
        </tr>
                                            </table>


### Examples
```
  - name: Get a single SyncIQ report with id
    register: result
    dellemc_powerscale_synciqreports:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      id: "1-Test_syncIQ_policy"
      state: "present"

  - name: Get a single SyncIQ report with name
    register: result
    dellemc_powerscale_synciqreports:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      name: "Test_snap_schedule_123"
      state: "present"

  - name: Get all SyncIQ sub-reports with report id
    register: result
    dellemc_powerscale_synciqreports:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      id: "1-Test_syncIQ_policy"
      include_sub_reports: "True"
      state: "present"

  - name: Get all SyncIQ sub-reports with report name
    register: result
    dellemc_powerscale_synciqreports:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      name: "Test_syncIQ_policy"
      include_sub_reports: "True"
      state: "present"

  - name: Get a single SyncIQ sub-report with sub-report id
    register: result
    dellemc_powerscale_synciqreports:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      id: "1-Test_syncIQ_policy"
      sub_report_id: "1"
      state: "present"
```

### Return Values
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
<table>
    <tr>
        <th colspan=5>Key</th>
        <th>Type</th>
        <th>Returned</th>
        <th width="100%">Description</th>
    </tr>
                                                                                    <tr>
            <td colspan=5 > changed </td>
            <td>  bool </td>
            <td> always </td>
            <td> Whether or not the resource has changed </td>
        </tr>
                    <tr>
            <td colspan=5 > synciq_report </td>
            <td>  complex </td>
            <td> When SyncIQ report exists </td>
            <td> Details of the SyncIQ report. </td>
        </tr>
                            <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > action </td>
                <td> str </td>
                <td>success</td>
                <td> The action to be taken by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > ads_streams_replicated </td>
                <td> int </td>
                <td>success</td>
                <td> The number of ads streams replicated by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > block_specs_replicated </td>
                <td> int </td>
                <td>success</td>
                <td> The number of block specs replicated by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > bytes_recoverable </td>
                <td> int </td>
                <td>success</td>
                <td> The number of bytes recoverable by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > bytes_transferred </td>
                <td> int </td>
                <td>success</td>
                <td> The number of bytes that have been transferred by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > char_specs_replicated </td>
                <td> int </td>
                <td>success</td>
                <td> The number of char specs replicated by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > committed_files </td>
                <td> int </td>
                <td>success</td>
                <td> The number of WORM committed files. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > corrected_lins </td>
                <td> int </td>
                <td>success</td>
                <td> The number of LINs corrected by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > dead_node </td>
                <td> bool </td>
                <td>success</td>
                <td> This field is true if the node running this job is dead. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > directories_replicated </td>
                <td> int </td>
                <td>success</td>
                <td> The number of directories replicated. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > dirs_changed </td>
                <td> int </td>
                <td>success</td>
                <td> The number of directories changed by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > dirs_deleted </td>
                <td> int </td>
                <td>success</td>
                <td> The number of directories deleted by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > dirs_moved </td>
                <td> int </td>
                <td>success</td>
                <td> The number of directories moved by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > dirs_new </td>
                <td> int </td>
                <td>success</td>
                <td> The number of directories created by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > duration </td>
                <td> int </td>
                <td>success</td>
                <td> The amount of time in seconds between when the job was started and when it ended. If the job has not yet ended, this is the amount of time since the job started. This field is null if the job has not yet started. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > encrypted </td>
                <td> bool </td>
                <td>success</td>
                <td> If true, syncs will be encrypted. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > end_time </td>
                <td> int </td>
                <td>success</td>
                <td> The time the job ended in unix epoch seconds. The field is null if the job hasn't ended. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > error </td>
                <td> str </td>
                <td>success</td>
                <td> The primary error message for this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > error_checksum_files_skipped </td>
                <td> int </td>
                <td>success</td>
                <td> The number of files with checksum errors skipped by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > error_io_files_skipped </td>
                <td> int </td>
                <td>success</td>
                <td> The number of files with io errors skipped by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > error_net_files_skipped </td>
                <td> int </td>
                <td>success</td>
                <td> The number of files with network errors skipped by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > errors </td>
                <td> list </td>
                <td>success</td>
                <td> A list of error messages for this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > failed_chunks </td>
                <td> int </td>
                <td>success</td>
                <td> The number of data chunks that failed transmission. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > fifos_replicated </td>
                <td> int </td>
                <td>success</td>
                <td> The number of fifos replicated by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > file_data_bytes </td>
                <td> int </td>
                <td>success</td>
                <td> The number of bytes transferred that belong to files. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > files_changed </td>
                <td> int </td>
                <td>success</td>
                <td> The number of files changed by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > files_linked </td>
                <td> int </td>
                <td>success</td>
                <td> The number of files linked by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > files_new </td>
                <td> int </td>
                <td>success</td>
                <td> The number of files created by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > files_selected </td>
                <td> int </td>
                <td>success</td>
                <td> The number of files selected by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > files_transferred </td>
                <td> int </td>
                <td>success</td>
                <td> The number of files transferred by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > files_unlinked </td>
                <td> int </td>
                <td>success</td>
                <td> The number of files unlinked by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > files_with_ads_replicated </td>
                <td> int </td>
                <td>success</td>
                <td> The number of files with ads replicated by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > flipped_lins </td>
                <td> int </td>
                <td>success</td>
                <td> The number of LINs flipped by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > hard_links_replicated </td>
                <td> int </td>
                <td>success</td>
                <td> TThe number of hard links replicated by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > hash_exceptions_fixed </td>
                <td> int </td>
                <td>success</td>
                <td> The number of hash exceptions fixed by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > hash_exceptions_found </td>
                <td> int </td>
                <td>success</td>
                <td> The number of hash exceptions found by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > id </td>
                <td> str </td>
                <td>success</td>
                <td> A unique identifier for this object. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > job_id </td>
                <td> int </td>
                <td>success</td>
                <td> The ID of the job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > lins_total </td>
                <td> int </td>
                <td>success</td>
                <td> The number of LINs transferred by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > network_bytes_to_source </td>
                <td> int </td>
                <td>success</td>
                <td> The total number of bytes sent to the source by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > network_bytes_to_target </td>
                <td> int </td>
                <td>success</td>
                <td> The total number of bytes sent to the target by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > new_files_replicated </td>
                <td> int </td>
                <td>success</td>
                <td> The number of new files replicated by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > num_retransmitted_files </td>
                <td> int </td>
                <td>success</td>
                <td> The number of files that have been retransmitted by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > phases </td>
                <td> complex </td>
                <td>success</td>
                <td> Data for each phase of this job. </td>
            </tr>
                                         <tr>
                    <td class="elbow-placeholder">&nbsp;</td>
                    <td class="elbow-placeholder">&nbsp;</td>
                    <td colspan=3 > end_time </td>
                    <td> int </td>
                    <td>success</td>
                    <td> The time the job ended this phase. </td>
                </tr>
                                             <tr>
                    <td class="elbow-placeholder">&nbsp;</td>
                    <td class="elbow-placeholder">&nbsp;</td>
                    <td colspan=3 > phase </td>
                    <td> str </td>
                    <td>success</td>
                    <td> The phase that the job was in. </td>
                </tr>
                                             <tr>
                    <td class="elbow-placeholder">&nbsp;</td>
                    <td class="elbow-placeholder">&nbsp;</td>
                    <td colspan=3 > start_time </td>
                    <td> int </td>
                    <td>success</td>
                    <td> The time the job began this phase. </td>
                </tr>
                                                            <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > policy </td>
                <td> complex </td>
                <td>success</td>
                <td> Policy details </td>
            </tr>
                                         <tr>
                    <td class="elbow-placeholder">&nbsp;</td>
                    <td class="elbow-placeholder">&nbsp;</td>
                    <td colspan=3 > name </td>
                    <td> str </td>
                    <td>success</td>
                    <td> User-assigned name of this sync policy. </td>
                </tr>
                                             <tr>
                    <td class="elbow-placeholder">&nbsp;</td>
                    <td class="elbow-placeholder">&nbsp;</td>
                    <td colspan=3 > source_root_path </td>
                    <td> str </td>
                    <td>success</td>
                    <td> The root directory on the source cluster the files will be synced from. </td>
                </tr>
                                             <tr>
                    <td class="elbow-placeholder">&nbsp;</td>
                    <td class="elbow-placeholder">&nbsp;</td>
                    <td colspan=3 > target_host </td>
                    <td> str </td>
                    <td>success</td>
                    <td> Hostname or IP address of sync target cluster. </td>
                </tr>
                                                            <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > policy_action </td>
                <td> str </td>
                <td>success</td>
                <td> This is the action the policy is configured to perform. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > policy_id </td>
                <td> str </td>
                <td>success</td>
                <td> The ID of the policy. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > policy_name </td>
                <td> str </td>
                <td>success</td>
                <td> The name of the policy. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > quotas_deleted </td>
                <td> int </td>
                <td>success</td>
                <td> The number of quotas removed from the target. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > regular_files_replicated </td>
                <td> int </td>
                <td>success</td>
                <td> The number of regular files replicated by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > resynced_lins </td>
                <td> int </td>
                <td>success</td>
                <td> The number of LINs resynched by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > retransmitted_files </td>
                <td> list </td>
                <td>success</td>
                <td> The files that have been retransmitted by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > retry </td>
                <td> int </td>
                <td>success</td>
                <td> The number of times the job has been retried. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > running_chunks </td>
                <td> int </td>
                <td>success</td>
                <td> The number of data chunks currently being transmitted. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > service_report </td>
                <td> complex </td>
                <td>success</td>
                <td> Data for each component exported as part of service replication. </td>
            </tr>
                                         <tr>
                    <td class="elbow-placeholder">&nbsp;</td>
                    <td class="elbow-placeholder">&nbsp;</td>
                    <td colspan=3 > end_time </td>
                    <td> int </td>
                    <td>success</td>
                    <td> The time the job end this component. </td>
                </tr>
                                             <tr>
                    <td class="elbow-placeholder">&nbsp;</td>
                    <td class="elbow-placeholder">&nbsp;</td>
                    <td colspan=3 > start_time </td>
                    <td> int </td>
                    <td>success</td>
                    <td> The time the job began this component. </td>
                </tr>
                                             <tr>
                    <td class="elbow-placeholder">&nbsp;</td>
                    <td class="elbow-placeholder">&nbsp;</td>
                    <td colspan=3 > status </td>
                    <td> str </td>
                    <td>success</td>
                    <td> The current status of export for this component. </td>
                </tr>
                                                            <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > sockets_replicated </td>
                <td> int </td>
                <td>success</td>
                <td> The number of sockets replicated by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > source_bytes_recovered </td>
                <td> int </td>
                <td>success</td>
                <td> The number of bytes recovered on the source. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > source_directories_created </td>
                <td> int </td>
                <td>success</td>
                <td> The number of directories created on the source. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > source_directories_deleted </td>
                <td> int </td>
                <td>success</td>
                <td> The number of directories deleted on the source. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > source_directories_linked </td>
                <td> int </td>
                <td>success</td>
                <td> The number of directories linked on the source. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > source_directories_unlinked </td>
                <td> int </td>
                <td>success</td>
                <td> The number of directories unlinked on the source. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > source_directories_visited </td>
                <td> int </td>
                <td>success</td>
                <td> The number of directories visited on the source. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > source_files_deleted </td>
                <td> int </td>
                <td>success</td>
                <td> The number of files deleted on the source. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > source_files_linked </td>
                <td> int </td>
                <td>success</td>
                <td> The number of files linked on the source. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > source_files_unlinked </td>
                <td> int </td>
                <td>success</td>
                <td> The number of sparse data bytes transferred by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > start_time </td>
                <td> int </td>
                <td>success</td>
                <td> The time the job started in unix epoch seconds. The field is null if the job hasn't started. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > state </td>
                <td> str </td>
                <td>success</td>
                <td> The state of the job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > subreport_count </td>
                <td> int </td>
                <td>success</td>
                <td> The number of subreports that are available for this job report. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > succeeded_chunks </td>
                <td> int </td>
                <td>success</td>
                <td> The number of data chunks that have been transmitted successfully. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > symlinks_replicated </td>
                <td> int </td>
                <td>success</td>
                <td> The number of symlinks replicated by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > sync_type </td>
                <td> str </td>
                <td>success</td>
                <td> The type of sync being performed by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > target_bytes_recovered </td>
                <td> int </td>
                <td>success</td>
                <td> The number of bytes recovered on the target. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > target_directories_created </td>
                <td> int </td>
                <td>success</td>
                <td> The number of directories created on the target. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > target_directories_deleted </td>
                <td> int </td>
                <td>success</td>
                <td> The number of directories deleted on the target. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > target_directories_linked </td>
                <td> int </td>
                <td>success</td>
                <td> The number of directories linked on the target. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > target_directories_unlinked </td>
                <td> int </td>
                <td>success</td>
                <td> The number of directories unlinked on the target. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > target_files_deleted </td>
                <td> int </td>
                <td>success</td>
                <td> The number of files deleted on the target. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > target_files_linked </td>
                <td> int </td>
                <td>success</td>
                <td> The number of files linked on the target. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > target_files_unlinked </td>
                <td> int </td>
                <td>success</td>
                <td> The number of files unlinked on the target. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > target_snapshots </td>
                <td> list </td>
                <td>success</td>
                <td> The target snapshots created by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > total_chunks </td>
                <td> int </td>
                <td>success</td>
                <td> The total number of data chunks transmitted by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > total_data_bytes </td>
                <td> int </td>
                <td>success</td>
                <td> The total number of bytes transferred by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > total_exported_services </td>
                <td> int </td>
                <td>success</td>
                <td> The total number of components exported as part of service replication. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > total_files </td>
                <td> int </td>
                <td>success</td>
                <td> The number of files affected by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > total_network_bytes </td>
                <td> int </td>
                <td>success</td>
                <td> The total number of bytes sent over the network by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > total_phases </td>
                <td> int </td>
                <td>success</td>
                <td> The total number of phases for this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > unchanged_data_bytes </td>
                <td> int </td>
                <td>success</td>
                <td> The number of bytes unchanged by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > up_to_date_files_skipped </td>
                <td> int </td>
                <td>success</td>
                <td> The number of up-to-date files skipped by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > updated_files_replicated </td>
                <td> int </td>
                <td>success</td>
                <td> The number of updated files replicated by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > user_conflict_files_skipped </td>
                <td> int </td>
                <td>success</td>
                <td> The number of files with user conflicts skipped by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > warnings </td>
                <td> list </td>
                <td>success</td>
                <td> A list of warning messages for this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > worm_committed_file_conflicts </td>
                <td> int </td>
                <td>success</td>
                <td> The number of WORM committed files which needed to be reverted. Since WORM committed files cannot be reverted, this is the number of files that were preserved in the compliance store. </td>
            </tr>
                                        </table>

### Authors
* Meenakshi Dembi (@dembim) <ansible.team@dell.com>

--------------------------------
# Smart Quota Module

Manage Smart Quotas on PowerScale

### Synopsis
 Manages Smart Quotas on a PowerScale storage system. This includes getting details, modifying, creating and deleting Smart Quotas.

### Parameters
                                                                                                                                                                                                                                                                                                                                                            
<table>
    <tr>
        <th colspan=2>Parameter</th>
        <th width="20%">Type</th>
        <th>Required</th>
        <th>Default</th>
        <th>Choices</th>
        <th width="80%">Description</th>
    </tr>
                                                            <tr>
            <td colspan=2 > path</td>
            <td> str  </td>
            <td> True </td>
            <td></td>
            <td></td>
            <td> <br> The path on which the quota will be imposed.  <br> For system access zone, the path is absolute. For all other access zones, the path is a relative path from the base of the access zone. </td>
        </tr>
                    <tr>
            <td colspan=2 > quota_type</td>
            <td> str  </td>
            <td> True </td>
            <td></td>
            <td> <ul> <li>user</li>  <li>group</li>  <li>directory</li>  <li>default-user</li>  <li>default-group</li> </ul></td>
            <td> <br> The type of quota which will be imposed on the path. </td>
        </tr>
                    <tr>
            <td colspan=2 > user_name</td>
            <td> str  </td>
            <td></td>
            <td></td>
            <td></td>
            <td> <br> The name of the user account for which quota operations will be performed. </td>
        </tr>
                    <tr>
            <td colspan=2 > group_name</td>
            <td> str  </td>
            <td></td>
            <td></td>
            <td></td>
            <td> <br> The name of the group for which quota operations will be performed. </td>
        </tr>
                    <tr>
            <td colspan=2 > access_zone</td>
            <td> str  </td>
            <td></td>
            <td> system </td>
            <td></td>
            <td> <br> This option mentions the zone in which the user/group exists.  <br> For a non-system access zone, the path relative to the non-system Access Zone's base directory has to be given.  <br> For a system access zone, the absolute path has to be given. </td>
        </tr>
                    <tr>
            <td colspan=2 > provider_type</td>
            <td> str  </td>
            <td></td>
            <td> local </td>
            <td> <ul> <li>local</li>  <li>file</li>  <li>ldap</li>  <li>ads</li> </ul></td>
            <td> <br> This option defines the type which is used to authenticate the user/group.  <br> If the provider_type is 'ads' then the domain name of the Active Directory Server has to be mentioned in the user_name. The format for the user_name should be 'DOMAIN_NAME\user_name' or "DOMAIN_NAME\\user_name".  <br> This option acts as a filter for all operations except creation. </td>
        </tr>
                    <tr>
            <td colspan=2 > quota</td>
            <td> dict  </td>
            <td></td>
            <td></td>
            <td></td>
            <td> <br> Specifies Smart Quota parameters. </td>
        </tr>
                            <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > include_snapshots </td>
                <td> bool  </td>
                <td></td>
                <td> False </td>
                <td></td>
                <td>  <br> Whether to include the snapshots in the quota or not.  </td>
            </tr>
                    <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > include_overheads </td>
                <td> bool  </td>
                <td></td>
                <td></td>
                <td></td>
                <td>  <br> Whether to include the data protection overheads in the quota or not.  <br> If not passed during quota creation then quota will be created excluding the overheads.  <br> This parameter is supported for SDK 8.1.1  </td>
            </tr>
                    <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > thresholds_on </td>
                <td> str  </td>
                <td></td>
                <td></td>
                <td> <ul> <li>app_logical_size</li>  <li>fs_logical_size</li>  <li>physical_size</li> </ul></td>
                <td>  <br> For SDK 9.0.0 the parameter include_overheads is deprecated and thresholds_on is used.  </td>
            </tr>
                    <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > advisory_limit_size </td>
                <td> int  </td>
                <td></td>
                <td></td>
                <td></td>
                <td>  <br> The threshold value after which the advisory notification will be sent.  </td>
            </tr>
                    <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > soft_limit_size </td>
                <td> int  </td>
                <td></td>
                <td></td>
                <td></td>
                <td>  <br> Threshold value after which the soft limit exceeded notification will be sent and the soft_grace period will start.  <br> Write access will be restricted after the grace period expires.  <br> Both soft_grace_period and soft_limit_size are required to modify soft threshold for the quota.  </td>
            </tr>
                    <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > soft_grace_period </td>
                <td> int  </td>
                <td></td>
                <td></td>
                <td></td>
                <td>  <br> Grace Period after the soft limit for quota is exceeded.  <br> After the grace period, the write access to the quota will be restricted.  <br> Both soft_grace_period and soft_limit_size are required to modify soft threshold for the quota.  </td>
            </tr>
                    <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > period_unit </td>
                <td> str  </td>
                <td></td>
                <td></td>
                <td> <ul> <li>days</li>  <li>weeks</li>  <li>months</li> </ul></td>
                <td>  <br> Unit of the time period for soft_grace_period.  <br> For months the number of days is assumed to be 30 days.  <br> This parameter is required only if the soft_grace_period, is specified.  </td>
            </tr>
                    <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > hard_limit_size </td>
                <td> int  </td>
                <td></td>
                <td></td>
                <td></td>
                <td>  <br> Threshold value after which a hard limit exceeded notification will be sent.  <br> Write access will be restricted after the hard limit is exceeded.  </td>
            </tr>
                    <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > cap_unit </td>
                <td> str  </td>
                <td></td>
                <td></td>
                <td> <ul> <li>GB</li>  <li>TB</li> </ul></td>
                <td>  <br> Unit of storage for the hard, soft and advisory limits.  <br> This parameter is required if any of the hard, soft or advisory limits is specified.  </td>
            </tr>
                            <tr>
            <td colspan=2 > state</td>
            <td> str  </td>
            <td> True </td>
            <td></td>
            <td> <ul> <li>absent</li>  <li>present</li> </ul></td>
            <td> <br> Define whether the Smart Quota should exist or not.  <br> present - indicates that the Smart Quota should exist on the system.  <br> absent - indicates that the Smart Quota should not exist on the system. </td>
        </tr>
                    <tr>
            <td colspan=2 > onefs_host</td>
            <td> str  </td>
            <td> True </td>
            <td></td>
            <td></td>
            <td> <br> IP address or FQDN of the PowerScale cluster. </td>
        </tr>
                    <tr>
            <td colspan=2 > port_no</td>
            <td> str  </td>
            <td></td>
            <td> 8080 </td>
            <td></td>
            <td> <br> Port number of the PowerScale cluster.It defaults to 8080 if not specified. </td>
        </tr>
                    <tr>
            <td colspan=2 > verify_ssl</td>
            <td> bool  </td>
            <td> True </td>
            <td></td>
            <td> <ul> <li>True</li>  <li>False</li> </ul></td>
            <td> <br> boolean variable to specify whether to validate SSL certificate or not.  <br> True - indicates that the SSL certificate should be verified.  <br> False - indicates that the SSL certificate should not be verified. </td>
        </tr>
                    <tr>
            <td colspan=2 > api_user</td>
            <td> str  </td>
            <td> True </td>
            <td></td>
            <td></td>
            <td> <br> username of the PowerScale cluster. </td>
        </tr>
                    <tr>
            <td colspan=2 > api_password</td>
            <td> str  </td>
            <td> True </td>
            <td></td>
            <td></td>
            <td> <br> the password of the PowerScale cluster. </td>
        </tr>
                                                    </table>

### Notes
* To perform any operation, path, quota_type and state are mandatory parameters.
* There can be two quotas for each type per directory, one with snapshots included and one without snapshots included.
* Once the limits are assigned, then the quota can't be converted to accounting. Only modification to the threshold limits is permitted.

### Examples
```
  - name: Create a Quota for a User excluding snapshot.
    dellemc_powerscale_smartquota:
      onefs_host: "{{onefs_host}}"
      verify_ssl: "{{verify_ssl}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      path: "<path>"
      quota_type: "user"
      user_name: "{{user_name}}"
      access_zone: "sample-zone"
      provider_type: "local"
      quota:
        include_overheads: False
        advisory_limit_size: "{{advisory_limit_size}}"
        soft_limit_size: "{{soft_limit_size}}"
        soft_grace_period: "{{soft_grace_period}}"
        period_unit: "{{period_unit}}"
        hard_limit_size: "{{hard_limit_size}}"
        cap_unit: "{{cap_unit}}"
      state: "present"

  - name: Create a Quota for a Directory for accounting includes snapshots and data protection overheads.
    dellemc_powerscale_smartquota:
      onefs_host: "{{onefs_host}}"
      verify_ssl: "{{verify_ssl}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      path: "<path>"
      quota_type: "directory"
      quota:
        include_snapshots: "True"
        include_overheads: True
      state: "present"

  - name: Create default-user Quota for a Directory with snaps and overheads
    dellemc_powerscale_smartquota:
      onefs_host: "{{onefs_host}}"
      verify_ssl: "{{verify_ssl}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      path: "<path>"
      quota_type: "default-user"
      quota:
        include_snapshots: "True"
        include_overheads: True
      state: "present"

  - name: Get a Quota Details for a Group
    dellemc_powerscale_smartquota:
      onefs_host: "{{onefs_host}}"
      verify_ssl: "{{verify_ssl}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      path: "<path>"
      quota_type: "group"
      group_name: "{{user_name}}"
      access_zone: "sample-zone"
      provider_type: "local"
      quota:
        include_snapshots: "True"
      state: "present"

  - name: Update Quota for a User
    dellemc_powerscale_smartquota:
      onefs_host: "{{onefs_host}}"
      verify_ssl: "{{verify_ssl}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      path: "<path>"
      quota_type: "user"
      user_name: "{{user_name}}"
      access_zone: "sample-zone"
      provider_type: "local"
      quota:
        include_snapshots: "True"
        include_overheads: True
        advisory_limit_size: "{{new_advisory_limit_size}}"
        hard_limit_size: "{{new_hard_limit_size}}"
        cap_unit: "{{cap_unit}}"
      state: "present"

  - name: Modify Soft Limit and Grace period of default-user Quota
    dellemc_powerscale_smartquota:
      onefs_host: "{{onefs_host}}"
      verify_ssl: "{{verify_ssl}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      path: "<path>"
      quota_type: "default-user"
      access_zone: "sample-zone"
      quota:
        include_snapshots: "True"
        include_overheads: True
        soft_limit_size: "{{soft_limit_size}}"
        cap_unit: "{{cap_unit}}"
        soft_grace_period: "{{soft_grace_period}}"
        period_unit: "{{period_unit}}"
      state: "present"

  - name: Delete a Quota for a Directory
    dellemc_powerscale_smartquota:
      onefs_host: "{{onefs_host}}"
      verify_ssl: "{{verify_ssl}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      path: "<path>"
      quota_type: "directory"
      quota:
        include_snapshots: "True"
      state: "absent"

  - name: Delete Quota for a default-group
    dellemc_powerscale_smartquota:
      onefs_host: "{{onefs_host}}"
      verify_ssl: "{{verify_ssl}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      path: "<path>"
      quota_type: "default-group"
      quota:
        include_snapshots: "True"
      state: "absent"
```

### Return Values
                                                                                                                                                                                                                                            
<table>
    <tr>
        <th colspan=2>Key</th>
        <th>Type</th>
        <th>Returned</th>
        <th width="100%">Description</th>
    </tr>
                                                                                            <tr>
            <td colspan=2 > changed </td>
            <td>  bool </td>
            <td> always </td>
            <td> Whether or not the resource has changed </td>
        </tr>
                    <tr>
            <td colspan=2 > quota_details </td>
            <td>  complex </td>
            <td> When Quota exists. </td>
            <td> The quota details. </td>
        </tr>
                            <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > enforced </td>
                <td> bool </td>
                <td>success</td>
                <td> Whether the limits are enforced on Quota or not. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > id </td>
                <td> str </td>
                <td>success</td>
                <td> The ID of the Quota. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > thresholds </td>
                <td> dict </td>
                <td>success</td>
                <td> Includes information about all the limits imposed on quota. The limits are mentioned in bytes and soft_grace is in seconds. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > type </td>
                <td> str </td>
                <td>success</td>
                <td> The type of Quota. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > usage </td>
                <td> dict </td>
                <td>success</td>
                <td> The Quota usage. </td>
            </tr>
                                        </table>

### Authors
* P Srinivas Rao (@srinivas-rao5) <ansible.team@dell.com>

--------------------------------
# SyncIQ Target Reports Module

Provides the SyncIQ target reports for PowerScale Storage System

### Synopsis
 This module provides the SyncIQ target reports for PowerScale Storage System.

### Parameters
                                                                                                                                                                                                                                                    
<table>
    <tr>
        <th colspan=1>Parameter</th>
        <th width="20%">Type</th>
        <th>Required</th>
        <th>Default</th>
        <th>Choices</th>
        <th width="80%">Description</th>
    </tr>
                                                            <tr>
            <td colspan=1 > name</td>
            <td> str  </td>
            <td></td>
            <td></td>
            <td></td>
            <td> <br> The name of the SyncIQ target report. </td>
        </tr>
                    <tr>
            <td colspan=1 > id</td>
            <td> str  </td>
            <td></td>
            <td></td>
            <td></td>
            <td> <br> The id of the SyncIQ target report. </td>
        </tr>
                    <tr>
            <td colspan=1 > sub_report_id</td>
            <td> str  </td>
            <td></td>
            <td></td>
            <td></td>
            <td> <br> The id of the SyncIQ target sub report. </td>
        </tr>
                    <tr>
            <td colspan=1 > include_sub_reports</td>
            <td> bool  </td>
            <td></td>
            <td> False </td>
            <td></td>
            <td> <br> This flag is used to fetch the list of target sub reports. </td>
        </tr>
                    <tr>
            <td colspan=1 > state</td>
            <td> str  </td>
            <td> True </td>
            <td></td>
            <td> <ul> <li>absent</li>  <li>present</li> </ul></td>
            <td> <br> The state option is used to mention the existence of target reports. </td>
        </tr>
                    <tr>
            <td colspan=1 > onefs_host</td>
            <td> str  </td>
            <td> True </td>
            <td></td>
            <td></td>
            <td> <br> IP address or FQDN of the PowerScale cluster. </td>
        </tr>
                    <tr>
            <td colspan=1 > port_no</td>
            <td> str  </td>
            <td></td>
            <td> 8080 </td>
            <td></td>
            <td> <br> Port number of the PowerScale cluster.It defaults to 8080 if not specified. </td>
        </tr>
                    <tr>
            <td colspan=1 > verify_ssl</td>
            <td> bool  </td>
            <td> True </td>
            <td></td>
            <td> <ul> <li>True</li>  <li>False</li> </ul></td>
            <td> <br> boolean variable to specify whether to validate SSL certificate or not.  <br> True - indicates that the SSL certificate should be verified.  <br> False - indicates that the SSL certificate should not be verified. </td>
        </tr>
                    <tr>
            <td colspan=1 > api_user</td>
            <td> str  </td>
            <td> True </td>
            <td></td>
            <td></td>
            <td> <br> username of the PowerScale cluster. </td>
        </tr>
                    <tr>
            <td colspan=1 > api_password</td>
            <td> str  </td>
            <td> True </td>
            <td></td>
            <td></td>
            <td> <br> the password of the PowerScale cluster. </td>
        </tr>
                                            </table>


### Examples
```
  - name: Get a single SyncIQ target report with id
    register: result
    dellemc_powerscale_synciqtargetreports:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      id: "2-sample_policy"
      state: "present"

  - name: Get a single SyncIQ target report with name
    register: result
    dellemc_powerscale_synciqtargetreports:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      name: "sample_policy"
      state: "present"

  - name: Get all SyncIQ target sub-reports with report id
    register: result
    dellemc_powerscale_synciqtargetreports:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      id: "2-sample_policy"
      include_sub_reports: "True"
      state: "present"

  - name: Get all SyncIQ target sub-reports with report name
    register: result
    dellemc_powerscale_synciqtargetreports:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      name: "sample_policy"
      include_sub_reports: "True"
      state: "present"

  - name: Get a single SyncIQ target sub-report with sub-report id
    register: result
    dellemc_powerscale_synciqreports:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      id: "2-sample_policy"
      sub_report_id: "1"
      state: "present"
```

### Return Values
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
<table>
    <tr>
        <th colspan=5>Key</th>
        <th>Type</th>
        <th>Returned</th>
        <th width="100%">Description</th>
    </tr>
                                                                                    <tr>
            <td colspan=5 > changed </td>
            <td>  bool </td>
            <td> always </td>
            <td> Whether or not the resource has changed </td>
        </tr>
                    <tr>
            <td colspan=5 > synciq_target_report </td>
            <td>  complex </td>
            <td> When SyncIQ target report exists </td>
            <td> Details of the SyncIQ target report. </td>
        </tr>
                            <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > action </td>
                <td> str </td>
                <td>success</td>
                <td> The action to be taken by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > ads_streams_replicated </td>
                <td> int </td>
                <td>success</td>
                <td> The number of ads streams replicated by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > block_specs_replicated </td>
                <td> int </td>
                <td>success</td>
                <td> The number of block specs replicated by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > bytes_recoverable </td>
                <td> int </td>
                <td>success</td>
                <td> The number of bytes recoverable by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > bytes_transferred </td>
                <td> int </td>
                <td>success</td>
                <td> The number of bytes that have been transferred by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > char_specs_replicated </td>
                <td> int </td>
                <td>success</td>
                <td> The number of char specs replicated by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > committed_files </td>
                <td> int </td>
                <td>success</td>
                <td> The number of WORM committed files. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > corrected_lins </td>
                <td> int </td>
                <td>success</td>
                <td> The number of LINs corrected by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > dead_node </td>
                <td> bool </td>
                <td>success</td>
                <td> This field is true if the node running this job is dead. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > directories_replicated </td>
                <td> int </td>
                <td>success</td>
                <td> The number of directories replicated. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > dirs_changed </td>
                <td> int </td>
                <td>success</td>
                <td> The number of directories changed by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > dirs_deleted </td>
                <td> int </td>
                <td>success</td>
                <td> The number of directories deleted by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > dirs_moved </td>
                <td> int </td>
                <td>success</td>
                <td> The number of directories moved by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > dirs_new </td>
                <td> int </td>
                <td>success</td>
                <td> The number of directories created by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > duration </td>
                <td> int </td>
                <td>success</td>
                <td> The amount of time in seconds between when the job was started and when it ended. If the job has not yet ended, this is the amount of time since the job started. This field is null if the job has not yet started. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > encrypted </td>
                <td> bool </td>
                <td>success</td>
                <td> If true, syncs will be encrypted. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > end_time </td>
                <td> int </td>
                <td>success</td>
                <td> The time the job ended in unix epoch seconds. The field is null if the job hasn't ended. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > error </td>
                <td> str </td>
                <td>success</td>
                <td> The primary error message for this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > error_checksum_files_skipped </td>
                <td> int </td>
                <td>success</td>
                <td> The number of files with checksum errors skipped by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > error_io_files_skipped </td>
                <td> int </td>
                <td>success</td>
                <td> The number of files with io errors skipped by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > error_net_files_skipped </td>
                <td> int </td>
                <td>success</td>
                <td> The number of files with network errors skipped by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > errors </td>
                <td> list </td>
                <td>success</td>
                <td> A list of error messages for this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > failed_chunks </td>
                <td> int </td>
                <td>success</td>
                <td> The number of data chunks that failed transmission. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > fifos_replicated </td>
                <td> int </td>
                <td>success</td>
                <td> The number of fifos replicated by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > file_data_bytes </td>
                <td> int </td>
                <td>success</td>
                <td> The number of bytes transferred that belong to files. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > files_changed </td>
                <td> int </td>
                <td>success</td>
                <td> The number of files changed by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > files_linked </td>
                <td> int </td>
                <td>success</td>
                <td> The number of files linked by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > files_new </td>
                <td> int </td>
                <td>success</td>
                <td> The number of files created by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > files_selected </td>
                <td> int </td>
                <td>success</td>
                <td> The number of files selected by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > files_transferred </td>
                <td> int </td>
                <td>success</td>
                <td> The number of files transferred by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > files_unlinked </td>
                <td> int </td>
                <td>success</td>
                <td> The number of files unlinked by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > files_with_ads_replicated </td>
                <td> int </td>
                <td>success</td>
                <td> The number of files with ads replicated by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > flipped_lins </td>
                <td> int </td>
                <td>success</td>
                <td> The number of LINs flipped by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > hard_links_replicated </td>
                <td> int </td>
                <td>success</td>
                <td> The number of hard links replicated by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > hash_exceptions_fixed </td>
                <td> int </td>
                <td>success</td>
                <td> The number of hash exceptions fixed by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > hash_exceptions_found </td>
                <td> int </td>
                <td>success</td>
                <td> The number of hash exceptions found by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > id </td>
                <td> str </td>
                <td>success</td>
                <td> A unique identifier for this object. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > job_id </td>
                <td> int </td>
                <td>success</td>
                <td> The ID of the job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > lins_total </td>
                <td> int </td>
                <td>success</td>
                <td> The number of LINs transferred by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > network_bytes_to_source </td>
                <td> int </td>
                <td>success</td>
                <td> The total number of bytes sent to the source by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > network_bytes_to_target </td>
                <td> int </td>
                <td>success</td>
                <td> The total number of bytes sent to the target by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > new_files_replicated </td>
                <td> int </td>
                <td>success</td>
                <td> The number of new files replicated by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > num_retransmitted_files </td>
                <td> int </td>
                <td>success</td>
                <td> The number of files that have been retransmitted by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > phases </td>
                <td> complex </td>
                <td>success</td>
                <td> Data for each phase of this job. </td>
            </tr>
                                         <tr>
                    <td class="elbow-placeholder">&nbsp;</td>
                    <td class="elbow-placeholder">&nbsp;</td>
                    <td colspan=3 > end_time </td>
                    <td> int </td>
                    <td>success</td>
                    <td> The time the job ended this phase. </td>
                </tr>
                                             <tr>
                    <td class="elbow-placeholder">&nbsp;</td>
                    <td class="elbow-placeholder">&nbsp;</td>
                    <td colspan=3 > phase </td>
                    <td> str </td>
                    <td>success</td>
                    <td> The phase that the job was in. </td>
                </tr>
                                             <tr>
                    <td class="elbow-placeholder">&nbsp;</td>
                    <td class="elbow-placeholder">&nbsp;</td>
                    <td colspan=3 > start_time </td>
                    <td> int </td>
                    <td>success</td>
                    <td> The time the job began this phase. </td>
                </tr>
                                                            <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > policy </td>
                <td> complex </td>
                <td>success</td>
                <td> Policy details </td>
            </tr>
                                         <tr>
                    <td class="elbow-placeholder">&nbsp;</td>
                    <td class="elbow-placeholder">&nbsp;</td>
                    <td colspan=3 > name </td>
                    <td> str </td>
                    <td>success</td>
                    <td> User-assigned name of this sync policy. </td>
                </tr>
                                             <tr>
                    <td class="elbow-placeholder">&nbsp;</td>
                    <td class="elbow-placeholder">&nbsp;</td>
                    <td colspan=3 > source_root_path </td>
                    <td> str </td>
                    <td>success</td>
                    <td> The root directory on the source cluster the files will be synced from. </td>
                </tr>
                                             <tr>
                    <td class="elbow-placeholder">&nbsp;</td>
                    <td class="elbow-placeholder">&nbsp;</td>
                    <td colspan=3 > target_host </td>
                    <td> str </td>
                    <td>success</td>
                    <td> Hostname or IP address of sync target cluster. </td>
                </tr>
                                                            <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > policy_action </td>
                <td> str </td>
                <td>success</td>
                <td> This is the action the policy is configured to perform. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > policy_id </td>
                <td> str </td>
                <td>success</td>
                <td> The ID of the policy. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > policy_name </td>
                <td> str </td>
                <td>success</td>
                <td> The name of the policy. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > quotas_deleted </td>
                <td> int </td>
                <td>success</td>
                <td> The number of quotas removed from the target. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > regular_files_replicated </td>
                <td> int </td>
                <td>success</td>
                <td> The number of regular files replicated by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > resynced_lins </td>
                <td> int </td>
                <td>success</td>
                <td> The number of LINs resynched by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > retransmitted_files </td>
                <td> list </td>
                <td>success</td>
                <td> The files that have been retransmitted by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > retry </td>
                <td> int </td>
                <td>success</td>
                <td> The number of times the job has been retried. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > running_chunks </td>
                <td> int </td>
                <td>success</td>
                <td> The number of data chunks currently being transmitted. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > service_report </td>
                <td> complex </td>
                <td>success</td>
                <td> Data for each component exported as part of service replication. </td>
            </tr>
                                         <tr>
                    <td class="elbow-placeholder">&nbsp;</td>
                    <td class="elbow-placeholder">&nbsp;</td>
                    <td colspan=3 > end_time </td>
                    <td> int </td>
                    <td>success</td>
                    <td> The time the job end this component. </td>
                </tr>
                                             <tr>
                    <td class="elbow-placeholder">&nbsp;</td>
                    <td class="elbow-placeholder">&nbsp;</td>
                    <td colspan=3 > start_time </td>
                    <td> int </td>
                    <td>success</td>
                    <td> The time the job began this component. </td>
                </tr>
                                             <tr>
                    <td class="elbow-placeholder">&nbsp;</td>
                    <td class="elbow-placeholder">&nbsp;</td>
                    <td colspan=3 > status </td>
                    <td> str </td>
                    <td>success</td>
                    <td> The current status of export for this component. </td>
                </tr>
                                                            <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > sockets_replicated </td>
                <td> int </td>
                <td>success</td>
                <td> The number of sockets replicated by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > source_bytes_recovered </td>
                <td> int </td>
                <td>success</td>
                <td> The number of bytes recovered on the source. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > source_directories_created </td>
                <td> int </td>
                <td>success</td>
                <td> The number of directories created on the source. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > source_directories_deleted </td>
                <td> int </td>
                <td>success</td>
                <td> The number of directories deleted on the source. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > source_directories_linked </td>
                <td> int </td>
                <td>success</td>
                <td> The number of directories linked on the source. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > source_directories_unlinked </td>
                <td> int </td>
                <td>success</td>
                <td> The number of directories unlinked on the source. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > source_directories_visited </td>
                <td> int </td>
                <td>success</td>
                <td> The number of directories visited on the source. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > source_files_deleted </td>
                <td> int </td>
                <td>success</td>
                <td> The number of files deleted on the source. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > source_files_linked </td>
                <td> int </td>
                <td>success</td>
                <td> The number of files linked on the source. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > source_files_unlinked </td>
                <td> int </td>
                <td>success</td>
                <td> The number of sparse data bytes transferred by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > start_time </td>
                <td> int </td>
                <td>success</td>
                <td> The time the job started in unix epoch seconds. The field is null if the job hasn't started. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > state </td>
                <td> str </td>
                <td>success</td>
                <td> The state of the job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > subreport_count </td>
                <td> int </td>
                <td>success</td>
                <td> The number of subreports that are available for this job report. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > succeeded_chunks </td>
                <td> int </td>
                <td>success</td>
                <td> The number of data chunks that have been transmitted successfully. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > symlinks_replicated </td>
                <td> int </td>
                <td>success</td>
                <td> The number of symlinks replicated by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > sync_type </td>
                <td> str </td>
                <td>success</td>
                <td> The type of sync being performed by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > target_bytes_recovered </td>
                <td> int </td>
                <td>success</td>
                <td> The number of bytes recovered on the target. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > target_directories_created </td>
                <td> int </td>
                <td>success</td>
                <td> The number of directories created on the target. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > target_directories_deleted </td>
                <td> int </td>
                <td>success</td>
                <td> The number of directories deleted on the target. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > target_directories_linked </td>
                <td> int </td>
                <td>success</td>
                <td> The number of directories linked on the target. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > target_directories_unlinked </td>
                <td> int </td>
                <td>success</td>
                <td> The number of directories unlinked on the target. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > target_files_deleted </td>
                <td> int </td>
                <td>success</td>
                <td> The number of files deleted on the target. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > target_files_linked </td>
                <td> int </td>
                <td>success</td>
                <td> The number of files linked on the target. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > target_files_unlinked </td>
                <td> int </td>
                <td>success</td>
                <td> The number of files unlinked on the target. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > target_snapshots </td>
                <td> list </td>
                <td>success</td>
                <td> The target snapshots created by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > total_chunks </td>
                <td> int </td>
                <td>success</td>
                <td> The total number of data chunks transmitted by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > total_data_bytes </td>
                <td> int </td>
                <td>success</td>
                <td> The total number of bytes transferred by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > total_exported_services </td>
                <td> int </td>
                <td>success</td>
                <td> The total number of components exported as part of service replication. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > total_files </td>
                <td> int </td>
                <td>success</td>
                <td> The number of files affected by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > total_network_bytes </td>
                <td> int </td>
                <td>success</td>
                <td> The total number of bytes sent over the network by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > total_phases </td>
                <td> int </td>
                <td>success</td>
                <td> The total number of phases for this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > unchanged_data_bytes </td>
                <td> int </td>
                <td>success</td>
                <td> The number of bytes unchanged by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > up_to_date_files_skipped </td>
                <td> int </td>
                <td>success</td>
                <td> The number of up-to-date files skipped by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > updated_files_replicated </td>
                <td> int </td>
                <td>success</td>
                <td> The number of updated files replicated by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > user_conflict_files_skipped </td>
                <td> int </td>
                <td>success</td>
                <td> The number of files with user conflicts skipped by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > warnings </td>
                <td> list </td>
                <td>success</td>
                <td> A list of warning messages for this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > worm_committed_file_conflicts </td>
                <td> int </td>
                <td>success</td>
                <td> The number of WORM committed files which needed to be reverted. Since WORM committed files cannot be reverted, this is the number of files that were preserved in the compliance store. </td>
            </tr>
                                        </table>

### Authors
* Meenakshi Dembi (@dembim) <ansible.team@dell.com>

--------------------------------
# ADS Module

Manages the ADS authentication provider on PowerScale

### Synopsis
 Manages the Active Directory authentication provider on the PowerScale storage system. This includes creating, modifying, deleting and retreiving the details of an ADS provider.

### Parameters
                                                                                                                                                                                                                                                                                                                
<table>
    <tr>
        <th colspan=2>Parameter</th>
        <th width="20%">Type</th>
        <th>Required</th>
        <th>Default</th>
        <th>Choices</th>
        <th width="80%">Description</th>
    </tr>
                                                            <tr>
            <td colspan=2 > domain_name</td>
            <td> str  </td>
            <td></td>
            <td></td>
            <td></td>
            <td> <br> Specifies the domain name of an Active Directory provider.  <br> This parameter is mandatory during create. </td>
        </tr>
                    <tr>
            <td colspan=2 > instance_name</td>
            <td> str  </td>
            <td></td>
            <td></td>
            <td></td>
            <td> <br> Specifies the instance name of Active Directory provider.  <br> This is an optional parameter during create, and defaults to the provider name if it is not specified during the create operation.  <br> get, modify and delete operations can also be performed through instance_name.  <br> It is mutually exclusive with domain_name for get, modify and delete operations. </td>
        </tr>
                    <tr>
            <td colspan=2 > ads_user</td>
            <td> str  </td>
            <td></td>
            <td></td>
            <td></td>
            <td> <br> Specifies the user name that has permission to join a machine to the given domain.  <br> This parameter is mandatory during create. </td>
        </tr>
                    <tr>
            <td colspan=2 > ads_password</td>
            <td> str  </td>
            <td></td>
            <td></td>
            <td></td>
            <td> <br> Specifies the password used during domain join.  <br> This parameter is mandatory during create. </td>
        </tr>
                    <tr>
            <td colspan=2 > ads_parameters</td>
            <td> dict  </td>
            <td></td>
            <td></td>
            <td></td>
            <td> <br> Specify additional parameters to configure ADS domain. </td>
        </tr>
                            <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > groupnet </td>
                <td> str  </td>
                <td></td>
                <td></td>
                <td></td>
                <td>  <br> Groupnet identifier.  <br> This is an optional parameter and defaults to groupnet0.  </td>
            </tr>
                    <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > home_directory_template </td>
                <td> str  </td>
                <td></td>
                <td></td>
                <td></td>
                <td>  <br> Specifies the path to the home directory template.  <br> This is an optional parameter and defaults to '/ifs/home/%D/%U'.  </td>
            </tr>
                    <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > login_shell </td>
                <td> str  </td>
                <td></td>
                <td></td>
                <td> <ul> <li>/bin/sh</li>  <li>/bin/csh</li>  <li>/bin/tcsh</li>  <li>/bin/zsh</li>  <li>/bin/bash</li>  <li>/bin/rbash</li>  <li>/sbin/nologin</li> </ul></td>
                <td>  <br> Specifies the login shell path.  <br> This is an optional parameter and defaults to '/bin/zsh'.  </td>
            </tr>
                            <tr>
            <td colspan=2 > state</td>
            <td> str  </td>
            <td> True </td>
            <td></td>
            <td> <ul> <li>absent</li>  <li>present</li> </ul></td>
            <td> <br> The state of the ads provider after the task is performed.  <br> present - indicates that the ADS provider should exist on the system.  <br> absent - indicates that the ADS provider should not exist on the system. </td>
        </tr>
                    <tr>
            <td colspan=2 > onefs_host</td>
            <td> str  </td>
            <td> True </td>
            <td></td>
            <td></td>
            <td> <br> IP address or FQDN of the PowerScale cluster. </td>
        </tr>
                    <tr>
            <td colspan=2 > port_no</td>
            <td> str  </td>
            <td></td>
            <td> 8080 </td>
            <td></td>
            <td> <br> Port number of the PowerScale cluster.It defaults to 8080 if not specified. </td>
        </tr>
                    <tr>
            <td colspan=2 > verify_ssl</td>
            <td> bool  </td>
            <td> True </td>
            <td></td>
            <td> <ul> <li>True</li>  <li>False</li> </ul></td>
            <td> <br> boolean variable to specify whether to validate SSL certificate or not.  <br> True - indicates that the SSL certificate should be verified.  <br> False - indicates that the SSL certificate should not be verified. </td>
        </tr>
                    <tr>
            <td colspan=2 > api_user</td>
            <td> str  </td>
            <td> True </td>
            <td></td>
            <td></td>
            <td> <br> username of the PowerScale cluster. </td>
        </tr>
                    <tr>
            <td colspan=2 > api_password</td>
            <td> str  </td>
            <td> True </td>
            <td></td>
            <td></td>
            <td> <br> the password of the PowerScale cluster. </td>
        </tr>
                                            </table>


### Examples
```
- name: Add an Active Directory provider
  dellemc_powerscale_ads:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      domain_name: "ansibleneo.com"
      instance_name: "ansibleneo.com"
      ads_user: "administrator"
      ads_password: "*****"
      ads_parameters:
        groupnet: "groupnet5"
        home_directory_template: "/ifs/home/%D/%U"
        login_shell: "/bin/zsh"
      state: "present"

- name: Modify an Active Directory provider with domain name
  dellemc_powerscale_ads:
      onefs_host: "{{onefs_host}}"
      verify_ssl: "{{verify_ssl}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      domain_name: "ansibleneo.com"
      ads_parameters:
        home_directory_template: "/ifs/usr_home/%D/%U"
        login_shell: "/bin/rbash"
      state: "present"

- name: Modify an Active Directory provider with instance name
  dellemc_powerscale_ads:
      onefs_host: "{{onefs_host}}"
      verify_ssl: "{{verify_ssl}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      instance_name: "ansibleneo.com"
      ads_parameters:
        home_directory_template: "/ifs/usr_home/%D/%U"
        login_shell: "/bin/rbash"
      state: "present"

- name: Get Active Directory provider details with domain name
  dellemc_powerscale_ads:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      domain_name: "ansibleneo.com"
      state: "present"

- name: Get Active Directory provider details with instance name
  dellemc_powerscale_ads:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      instance_name: "ansibleneo.com"
      state: "present"

- name: Delete an Active Directory provider with domain name
  dellemc_powerscale_ads:
      onefs_host: "{{onefs_host}}"
      verify_ssl: "{{verify_ssl}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      domain_name: "ansibleneo.com"
      state: "absent"

- name: Delete an Active Directory provider with instance name
  dellemc_powerscale_ads:
      onefs_host: "{{onefs_host}}"
      verify_ssl: "{{verify_ssl}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      instance_name: "ansibleneo.com"
      state: "absent"
```

### Return Values
                                                                                                                                                                                                                                                            
<table>
    <tr>
        <th colspan=2>Key</th>
        <th>Type</th>
        <th>Returned</th>
        <th width="100%">Description</th>
    </tr>
                                                                                    <tr>
            <td colspan=2 > ads_provider_details </td>
            <td>  complex </td>
            <td> When Active Directory provider exists </td>
            <td> The Active Directory provider details </td>
        </tr>
                            <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > groupnet </td>
                <td> str </td>
                <td>success</td>
                <td> Groupnet identifier. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > home_directory_template </td>
                <td> str </td>
                <td>success</td>
                <td> Specifies the path to the home directory template. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > id </td>
                <td> str </td>
                <td>success</td>
                <td> Specifies the ID of the Active Directory provider instance. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > linked_access_zones </td>
                <td> list </td>
                <td>success</td>
                <td> List of access zones linked to the authentication provider. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > login_shell </td>
                <td> str </td>
                <td>success</td>
                <td> Specifies the login shell path. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > name </td>
                <td> str </td>
                <td>success</td>
                <td> Specifies the Active Directory provider name. </td>
            </tr>
                                        <tr>
            <td colspan=2 > changed </td>
            <td>  bool </td>
            <td> always </td>
            <td> Whether or not the resource has changed </td>
        </tr>
                    </table>

### Authors
* Jennifer John (@johnj9) <ansible.team@dell.com>

--------------------------------
# Snapshot Schedule Module

Manage snapshot schedules on Dell EMC PowerScale.

### Synopsis
 You can perform the following operations
 Managing snapshot schedules on PowerScale.
 Create snapshot schedule.
 Modify snapshot schedule.
 Get details of snapshot schedule.
 Delete snapshot schedule.

### Parameters
                                                                                                                                                                                                                                                                                                                                                        
<table>
    <tr>
        <th colspan=1>Parameter</th>
        <th width="20%">Type</th>
        <th>Required</th>
        <th>Default</th>
        <th>Choices</th>
        <th width="80%">Description</th>
    </tr>
                                                            <tr>
            <td colspan=1 > name</td>
            <td> str  </td>
            <td> True </td>
            <td></td>
            <td></td>
            <td> <br> The name of the snapshot schedule. </td>
        </tr>
                    <tr>
            <td colspan=1 > path</td>
            <td> str  </td>
            <td></td>
            <td></td>
            <td></td>
            <td> <br> The path on which the snapshot will be taken. This path is relative to the base path of the Access Zone.  <br> For 'System' access zone, the path is absolute.  <br> This parameter is required at the time of creation.  <br> Modification of the path is not allowed through the Ansible module. </td>
        </tr>
                    <tr>
            <td colspan=1 > access_zone</td>
            <td> str  </td>
            <td></td>
            <td> System </td>
            <td></td>
            <td> <br> The effective path where the snapshot is created will be determined by the base path of the Access Zone and the path provided by the user in the playbook. </td>
        </tr>
                    <tr>
            <td colspan=1 > new_name</td>
            <td> str  </td>
            <td></td>
            <td></td>
            <td></td>
            <td> <br> The new name of the snapshot schedule. </td>
        </tr>
                    <tr>
            <td colspan=1 > desired_retention</td>
            <td> int  </td>
            <td></td>
            <td></td>
            <td></td>
            <td> <br> The number of hours/days for which snapshots created by this snapshot schedule should be retained.  <br> If retention is not specified at the time of creation, then the snapshots created by the snapshot schedule will be retained forever.  <br> Minimum retention duration is 2 hours.  <br> For large durations (beyond days/weeks), PowerScale may round off the retention to a somewhat larger value to match a whole number of days/weeks. </td>
        </tr>
                    <tr>
            <td colspan=1 > retention_unit</td>
            <td> str  </td>
            <td></td>
            <td> hours </td>
            <td> <ul> <li>hours</li>  <li>days</li> </ul></td>
            <td> <br> The retention unit for the snapshot created by this schedule. </td>
        </tr>
                    <tr>
            <td colspan=1 > alias</td>
            <td> str  </td>
            <td></td>
            <td></td>
            <td></td>
            <td> <br> The alias will point to the latest snapshot created by the snapshot schedule. </td>
        </tr>
                    <tr>
            <td colspan=1 > pattern</td>
            <td> str  </td>
            <td></td>
            <td></td>
            <td></td>
            <td> <br> Pattern expanded with strftime to create snapshot names.  <br> This parameter is required at the time of creation. </td>
        </tr>
                    <tr>
            <td colspan=1 > schedule</td>
            <td> str  </td>
            <td></td>
            <td></td>
            <td></td>
            <td> <br> The isidate compatible natural language description of the schedule.  <br> It specifies the frequency of the schedule.  <br> This parameter is required at the time of creation. </td>
        </tr>
                    <tr>
            <td colspan=1 > state</td>
            <td> str  </td>
            <td> True </td>
            <td></td>
            <td> <ul> <li>absent</li>  <li>present</li> </ul></td>
            <td> <br> Defines whether the snapshot schedule should exist or not. </td>
        </tr>
                    <tr>
            <td colspan=1 > onefs_host</td>
            <td> str  </td>
            <td> True </td>
            <td></td>
            <td></td>
            <td> <br> IP address or FQDN of the PowerScale cluster. </td>
        </tr>
                    <tr>
            <td colspan=1 > port_no</td>
            <td> str  </td>
            <td></td>
            <td> 8080 </td>
            <td></td>
            <td> <br> Port number of the PowerScale cluster.It defaults to 8080 if not specified. </td>
        </tr>
                    <tr>
            <td colspan=1 > verify_ssl</td>
            <td> bool  </td>
            <td> True </td>
            <td></td>
            <td> <ul> <li>True</li>  <li>False</li> </ul></td>
            <td> <br> boolean variable to specify whether to validate SSL certificate or not.  <br> True - indicates that the SSL certificate should be verified.  <br> False - indicates that the SSL certificate should not be verified. </td>
        </tr>
                    <tr>
            <td colspan=1 > api_user</td>
            <td> str  </td>
            <td> True </td>
            <td></td>
            <td></td>
            <td> <br> username of the PowerScale cluster. </td>
        </tr>
                    <tr>
            <td colspan=1 > api_password</td>
            <td> str  </td>
            <td> True </td>
            <td></td>
            <td></td>
            <td> <br> the password of the PowerScale cluster. </td>
        </tr>
                                            </table>


### Examples
```
- name: Create snapshot schedule
  dellemc_powerscale_snapshotschedule:
      onefs_host: "{{onefs_host}}"
      verify_ssl: "{{verify_ssl}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      name: "{{name}}"
      access_zone: '{{access_zone}}'
      path: '<path>'
      alias: "{{alias1}}"
      desired_retention: "{{desired_retention1}}"
      pattern: "{{pattern1}}"
      schedule: "{{schedule1}}"
      state: "{{state_present}}"

- name: Get details of snapshot schedule
  dellemc_powerscale_snapshotschedule:
      onefs_host: "{{onefs_host}}"
      verify_ssl: "{{verify_ssl}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      name: "{{name}}"
      state: "{{state_present}}"

- name: Rename snapshot schedule
  dellemc_powerscale_snapshotschedule:
      onefs_host: "{{onefs_host}}"
      verify_ssl: "{{verify_ssl}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      name: "{{name}}"
      new_name: "{{new_name}}"
      state: "{{state_present}}"

- name: Modify alias of snapshot schedule
  dellemc_powerscale_snapshotschedule:
      onefs_host: "{{onefs_host}}"
      verify_ssl: "{{verify_ssl}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      name: "{{new_name}}"
      alias: "{{alias2}}"
      state: "{{state_present}}"

- name: Modify pattern of snapshot schedule
  dellemc_powerscale_snapshotschedule:
      onefs_host: "{{onefs_host}}"
      verify_ssl: "{{verify_ssl}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      name: "{{new_name}}"
      pattern: "{{pattern2}}"
      state: "{{state_present}}"

- name: Modify schedule of snapshot schedule
  dellemc_powerscale_snapshotschedule:
      onefs_host: "{{onefs_host}}"
      verify_ssl: "{{verify_ssl}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      name: "{{new_name}}"
      schedule: "{{schedule2}}"
      state: "{{state_present}}"

- name: Modify retention of snapshot schedule
  dellemc_powerscale_snapshotschedule:
      onefs_host: "{{onefs_host}}"
      verify_ssl: "{{verify_ssl}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      name: "{{new_name}}"
      desired_retention: 2
      retention_unit: "{{retention_unit_days}}"
      state: "{{state_present}}"

- name: Delete snapshot schedule
  dellemc_powerscale_snapshotschedule:
      onefs_host: "{{onefs_host}}"
      verify_ssl: "{{verify_ssl}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      name: "{{new_name}}"
      state: "{{state_absent}}"

- name: Delete snapshot schedule - Idempotency
  dellemc_powerscale_snapshotschedule:
      onefs_host: "{{onefs_host}}"
      verify_ssl: "{{verify_ssl}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      name: "{{new_name}}"
      state: "{{state_absent}}"
```

### Return Values
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
<table>
    <tr>
        <th colspan=5>Key</th>
        <th>Type</th>
        <th>Returned</th>
        <th width="100%">Description</th>
    </tr>
                                                                                    <tr>
            <td colspan=5 > changed </td>
            <td>  bool </td>
            <td> always </td>
            <td> Whether or not the resource has changed </td>
        </tr>
                    <tr>
            <td colspan=5 > snapshot_schedule_details </td>
            <td>  complex </td>
            <td> When snapshot schedule exists </td>
            <td> Details of the snapshot schedule including snapshot details </td>
        </tr>
                            <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > schedules </td>
                <td> complex </td>
                <td>success</td>
                <td> Details of snapshot schedule </td>
            </tr>
                                         <tr>
                    <td class="elbow-placeholder">&nbsp;</td>
                    <td class="elbow-placeholder">&nbsp;</td>
                    <td colspan=3 > duration </td>
                    <td> int </td>
                    <td>success</td>
                    <td> Time in seconds added to creation time to construction expiration time </td>
                </tr>
                                             <tr>
                    <td class="elbow-placeholder">&nbsp;</td>
                    <td class="elbow-placeholder">&nbsp;</td>
                    <td colspan=3 > id </td>
                    <td> int </td>
                    <td>success</td>
                    <td> The system ID given to the schedule </td>
                </tr>
                                             <tr>
                    <td class="elbow-placeholder">&nbsp;</td>
                    <td class="elbow-placeholder">&nbsp;</td>
                    <td colspan=3 > next_run </td>
                    <td> int </td>
                    <td>success</td>
                    <td> Unix Epoch time of next snapshot to be created </td>
                </tr>
                                             <tr>
                    <td class="elbow-placeholder">&nbsp;</td>
                    <td class="elbow-placeholder">&nbsp;</td>
                    <td colspan=3 > next_snapshot </td>
                    <td> str </td>
                    <td>success</td>
                    <td> Formatted name of next snapshot to be created </td>
                </tr>
                                                            <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > snapshot_list </td>
                <td> complex </td>
                <td>success</td>
                <td> List of snapshots taken by this schedule </td>
            </tr>
                                         <tr>
                    <td class="elbow-placeholder">&nbsp;</td>
                    <td class="elbow-placeholder">&nbsp;</td>
                    <td colspan=3 > snapshots </td>
                    <td> complex </td>
                    <td>success</td>
                    <td> Details of snapshot </td>
                </tr>
                                                    <tr>
                        <td class="elbow-placeholder">&nbsp;</td>
                        <td class="elbow-placeholder">&nbsp;</td>
                        <td class="elbow-placeholder">&nbsp;</td>
                        <td colspan=2 > created </td>
                        <td> int </td>
                        <td>success</td>
                        <td> The Unix Epoch time the snapshot was created </td>
                    </tr>
                                    <tr>
                        <td class="elbow-placeholder">&nbsp;</td>
                        <td class="elbow-placeholder">&nbsp;</td>
                        <td class="elbow-placeholder">&nbsp;</td>
                        <td colspan=2 > expires </td>
                        <td> int </td>
                        <td>success</td>
                        <td> The Unix Epoch time the snapshot will expire and be eligible for automatic deletion. </td>
                    </tr>
                                    <tr>
                        <td class="elbow-placeholder">&nbsp;</td>
                        <td class="elbow-placeholder">&nbsp;</td>
                        <td class="elbow-placeholder">&nbsp;</td>
                        <td colspan=2 > id </td>
                        <td> int </td>
                        <td>success</td>
                        <td> The system ID given to the snapshot.This is useful for tracking the status of delete pending snapshots </td>
                    </tr>
                                    <tr>
                        <td class="elbow-placeholder">&nbsp;</td>
                        <td class="elbow-placeholder">&nbsp;</td>
                        <td class="elbow-placeholder">&nbsp;</td>
                        <td colspan=2 > name </td>
                        <td> str </td>
                        <td>success</td>
                        <td> The user or system supplied snapshot name. This will be null for snapshots pending delete </td>
                    </tr>
                                    <tr>
                        <td class="elbow-placeholder">&nbsp;</td>
                        <td class="elbow-placeholder">&nbsp;</td>
                        <td class="elbow-placeholder">&nbsp;</td>
                        <td colspan=2 > size </td>
                        <td> int </td>
                        <td>success</td>
                        <td> The amount of storage in bytes used to store this snapshot </td>
                    </tr>
                                                             <tr>
                    <td class="elbow-placeholder">&nbsp;</td>
                    <td class="elbow-placeholder">&nbsp;</td>
                    <td colspan=3 > total </td>
                    <td> int </td>
                    <td>success</td>
                    <td> Total number of items available </td>
                </tr>
                                                                    </table>

### Authors
* Akash Shendge (@shenda1) <ansible.team@dell.com>

--------------------------------
# User Module

Manage users on the PowerScale Storage System

### Synopsis
 Managing Users on the PowerScale Storage System includes create user, delete user, update user, get user, add role and remove role.

### Parameters
                                                                                                                                                                                                                                                                                                                                                                                                                                        
<table>
    <tr>
        <th colspan=1>Parameter</th>
        <th width="20%">Type</th>
        <th>Required</th>
        <th>Default</th>
        <th>Choices</th>
        <th width="80%">Description</th>
    </tr>
                                                            <tr>
            <td colspan=1 > user_name</td>
            <td> str  </td>
            <td></td>
            <td></td>
            <td></td>
            <td> <br> The name of the user account.  <br> Required at the time of user creation, for rest of the operations either user_name or user_id is required. </td>
        </tr>
                    <tr>
            <td colspan=1 > user_id</td>
            <td> str  </td>
            <td></td>
            <td></td>
            <td></td>
            <td> <br> The user_id is auto generated at the time of creation.  <br> For all other operations either user_name or user_id is needed. </td>
        </tr>
                    <tr>
            <td colspan=1 > password</td>
            <td> str  </td>
            <td></td>
            <td></td>
            <td></td>
            <td> <br> The password for the user account.  <br> Required only in the creation of a user account.  <br> If given in other operations then the password will be ignored. </td>
        </tr>
                    <tr>
            <td colspan=1 > access_zone</td>
            <td> str  </td>
            <td></td>
            <td> system </td>
            <td></td>
            <td> <br> This option mentions the zone in which a user is created.  <br> For creation, access_zone acts as an attribute for the user.  <br> For all other operations access_zone acts as a filter. </td>
        </tr>
                    <tr>
            <td colspan=1 > provider_type</td>
            <td> str  </td>
            <td></td>
            <td> local </td>
            <td> <ul> <li>local</li>  <li>file</li>  <li>ldap</li>  <li>ads</li> </ul></td>
            <td> <br> This option defines the type which will be used to authenticate the user.  <br> Creation, Modification and Deletion is allowed for local users.  <br> Adding and removing roles is allowed for all users of the system access zone.  <br> Getting user details is allowed for all users.  <br> If the provider_type is 'ads' then domain name of the Active Directory Server has to be mentioned in the user_name. The format for the user_name should be 'DOMAIN_NAME\user_name' or "DOMAIN_NAME\\user_name".  <br> This option acts as a filter for all operations except creation. </td>
        </tr>
                    <tr>
            <td colspan=1 > enabled</td>
            <td> bool  </td>
            <td></td>
            <td></td>
            <td></td>
            <td> <br> Enabled is a bool variable which is used to enable or disable the user account. </td>
        </tr>
                    <tr>
            <td colspan=1 > primary_group</td>
            <td> str  </td>
            <td></td>
            <td></td>
            <td></td>
            <td> <br> A user can be member of multiple groups of which one group has to be assigned as primary group.  <br> This group will be used for access checks and can also be used when creating files.  <br> A user can be added to the group using Group Name. </td>
        </tr>
                    <tr>
            <td colspan=1 > home_directory</td>
            <td> str  </td>
            <td></td>
            <td></td>
            <td></td>
            <td> <br> The path specified in this option acts as a home directory for the user.  <br> The directory which is given should not be already in use.  <br> For a user in a system access zone, the absolute path has to be given.  <br> For users in a non-system access zone, the path relative to the non-system Access Zone's base directory has to be given. </td>
        </tr>
                    <tr>
            <td colspan=1 > shell</td>
            <td> str  </td>
            <td></td>
            <td></td>
            <td></td>
            <td> <br> This option is for choosing the type of shell for the user account. </td>
        </tr>
                    <tr>
            <td colspan=1 > full_name</td>
            <td> str  </td>
            <td></td>
            <td></td>
            <td></td>
            <td> <br> The additional information about the user can be provided using full_name option. </td>
        </tr>
                    <tr>
            <td colspan=1 > email</td>
            <td> str  </td>
            <td></td>
            <td></td>
            <td></td>
            <td> <br> The email id of the user can be added using email option.  <br> The email id can be set at the time of creation and modified later. </td>
        </tr>
                    <tr>
            <td colspan=1 > state</td>
            <td> str  </td>
            <td> True </td>
            <td></td>
            <td> <ul> <li>absent</li>  <li>present</li> </ul></td>
            <td> <br> The state option is used to mention the existence of the user account. </td>
        </tr>
                    <tr>
            <td colspan=1 > role_name</td>
            <td> str  </td>
            <td></td>
            <td></td>
            <td></td>
            <td> <br> The name of the role which a user will be assigned.  <br> User can be added to multiple roles. </td>
        </tr>
                    <tr>
            <td colspan=1 > role_state</td>
            <td> str  </td>
            <td></td>
            <td></td>
            <td> <ul> <li>present-for-user</li>  <li>absent-for-user</li> </ul></td>
            <td> <br> The role_state option is used to mention the existence of the role for a particular user.  <br> It is required when a role is added or removed from user. </td>
        </tr>
                    <tr>
            <td colspan=1 > onefs_host</td>
            <td> str  </td>
            <td> True </td>
            <td></td>
            <td></td>
            <td> <br> IP address or FQDN of the PowerScale cluster. </td>
        </tr>
                    <tr>
            <td colspan=1 > port_no</td>
            <td> str  </td>
            <td></td>
            <td> 8080 </td>
            <td></td>
            <td> <br> Port number of the PowerScale cluster.It defaults to 8080 if not specified. </td>
        </tr>
                    <tr>
            <td colspan=1 > verify_ssl</td>
            <td> bool  </td>
            <td> True </td>
            <td></td>
            <td> <ul> <li>True</li>  <li>False</li> </ul></td>
            <td> <br> boolean variable to specify whether to validate SSL certificate or not.  <br> True - indicates that the SSL certificate should be verified.  <br> False - indicates that the SSL certificate should not be verified. </td>
        </tr>
                    <tr>
            <td colspan=1 > api_user</td>
            <td> str  </td>
            <td> True </td>
            <td></td>
            <td></td>
            <td> <br> username of the PowerScale cluster. </td>
        </tr>
                    <tr>
            <td colspan=1 > api_password</td>
            <td> str  </td>
            <td> True </td>
            <td></td>
            <td></td>
            <td> <br> the password of the PowerScale cluster. </td>
        </tr>
                                            </table>


### Examples
```
  - name: Get User Details using user name
    dellemc_powerscale_user:
      onefs_host: "{{onefs_host}}"
      port_no: "{{port_no}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      access_zone: "{{access_zone}}"
      provider_type: "{{provider_type}}"
      user_name: "{{account_name}}"
      state: "present"

  - name: Create User
    dellemc_powerscale_user:
      onefs_host: "{{onefs_host}}"
      port_no: "{{port_no}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      access_zone: "{{access_zone}}"
      provider_type: "{{provider_type}}"
      user_name: "{{account_name}}"
      password: "{{account_password}}"
      primary_group: "{{primary_group}}"
      enabled: "{{enabled}}"
      email: "{{email}}"
      full_name: "{{full_name}}"
      home_directory: "{{home_directory}}"
      shell: "{{shell}}"
      role_name: "{{role_name}}"
      role_state: "present-for-user"
      state: "present"

  - name: Update User's Full Name and email using user name
    dellemc_powerscale_user:
      onefs_host: "{{onefs_host}}"
      port_no: "{{port_no}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      access_zone: "{{access_zone}}"
      provider_type: "{{provider_type}}"
      user_name: "{{account_name}}"
      email: "{{new_email}}"
      full_name: "{{full_name}}"
      state: "present"

  - name: Disable User Account using User Id
    dellemc_powerscale_user:
      onefs_host: "{{onefs_host}}"
      port_no: "{{port_no}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      access_zone: "{{access_zone}}"
      provider_type: "{{provider_type}}"
      user_id: "{{id}}"
      enabled: "False"
      state: "present"

  - name: Add user to a role using Username
    dellemc_powerscale_user:
      onefs_host: "{{onefs_host}}"
      port_no: "{{port_no}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      user_name: "{{account_name}}"
      provider_type: "{{provider_type}}"
      role_name: "{{role_name}}"
      role_state: "present-for-user"
      state: "present"

  - name: Remove user from a role using User id
    dellemc_powerscale_user:
      onefs_host: "{{onefs_host}}"
      port_no: "{{port_no}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      user_id: "{{id}}"
      role_name: "{{role_name}}"
      role_state: "absent-for-user"
      state: "present"

  - name: Delete User using user name
    dellemc_powerscale_user:
      onefs_host: "{{onefs_host}}"
      port_no: "{{port_no}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      access_zone: "{{access_zone}}"
      provider_type: "{{provider_type}}"
      user_name: "{{account_name}}"
      state: "absent"
```

### Return Values
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
<table>
    <tr>
        <th colspan=4>Key</th>
        <th>Type</th>
        <th>Returned</th>
        <th width="100%">Description</th>
    </tr>
                                                                                    <tr>
            <td colspan=4 > changed </td>
            <td>  bool </td>
            <td> always </td>
            <td> Whether or not the resource has changed </td>
        </tr>
                    <tr>
            <td colspan=4 > user_details </td>
            <td>  complex </td>
            <td> When user exists </td>
            <td> Details of the user. </td>
        </tr>
                            <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=3 > email </td>
                <td> str </td>
                <td>success</td>
                <td> The email of the user. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=3 > enabled </td>
                <td> bool </td>
                <td>success</td>
                <td> Enabled is a bool variable which is used to enable or disable the user account. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=3 > gecos </td>
                <td> str </td>
                <td>success</td>
                <td> The full description of the user. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=3 > gid </td>
                <td> complex </td>
                <td>success</td>
                <td> The details of the primary group for the user. </td>
            </tr>
                                         <tr>
                    <td class="elbow-placeholder">&nbsp;</td>
                    <td class="elbow-placeholder">&nbsp;</td>
                    <td colspan=2 > id </td>
                    <td> str </td>
                    <td>success</td>
                    <td> The id of the primary group. </td>
                </tr>
                                             <tr>
                    <td class="elbow-placeholder">&nbsp;</td>
                    <td class="elbow-placeholder">&nbsp;</td>
                    <td colspan=2 > name </td>
                    <td> str </td>
                    <td>success</td>
                    <td> The name of the primary group. </td>
                </tr>
                                             <tr>
                    <td class="elbow-placeholder">&nbsp;</td>
                    <td class="elbow-placeholder">&nbsp;</td>
                    <td colspan=2 > type </td>
                    <td> str </td>
                    <td>success</td>
                    <td> The resource's type is mentioned. </td>
                </tr>
                                                            <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=3 > home_directory </td>
                <td> str </td>
                <td>success</td>
                <td> The directory path acts as the home directory for the user's account. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=3 > name </td>
                <td> str </td>
                <td>success</td>
                <td> The name of the user. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=3 > provider </td>
                <td> str </td>
                <td>success</td>
                <td> The provider contains the provider type and access zone. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=3 > roles </td>
                <td> list </td>
                <td>success</td>
                <td> The list of all the roles of which user is a member. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=3 > shell </td>
                <td> str </td>
                <td>success</td>
                <td> The type of shell for the user account. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=3 > uid </td>
                <td> complex </td>
                <td>success</td>
                <td> Details about the id and name of the user. </td>
            </tr>
                                         <tr>
                    <td class="elbow-placeholder">&nbsp;</td>
                    <td class="elbow-placeholder">&nbsp;</td>
                    <td colspan=2 > id </td>
                    <td> str </td>
                    <td>success</td>
                    <td> The id of the user. </td>
                </tr>
                                             <tr>
                    <td class="elbow-placeholder">&nbsp;</td>
                    <td class="elbow-placeholder">&nbsp;</td>
                    <td colspan=2 > name </td>
                    <td> str </td>
                    <td>success</td>
                    <td> The name of the user. </td>
                </tr>
                                             <tr>
                    <td class="elbow-placeholder">&nbsp;</td>
                    <td class="elbow-placeholder">&nbsp;</td>
                    <td colspan=2 > type </td>
                    <td> str </td>
                    <td>success</td>
                    <td> The resource's type is mentioned. </td>
                </tr>
                                                                    </table>

### Authors
* P Srinivas Rao (@srinivas-rao5) <ansible.team@dell.com>

--------------------------------
# SMB Module

Manage SMB shares on Dell EMC PowerScale. You can perform the following operations

### Synopsis
 Managing SMB share on PowerScale.
 Create a new SMB share.
 Modify an existing SMB share.
 Get details of an existing SMB share.
 Delete an existing SMB share.

### Parameters
                                                                                                                                                                                                                                                                                                                                                                                                                                                            
<table>
    <tr>
        <th colspan=1>Parameter</th>
        <th width="20%">Type</th>
        <th>Required</th>
        <th>Default</th>
        <th>Choices</th>
        <th width="80%">Description</th>
    </tr>
                                                            <tr>
            <td colspan=1 > share_name</td>
            <td> str  </td>
            <td> True </td>
            <td></td>
            <td></td>
            <td> <br> The name of the SMB share. </td>
        </tr>
                    <tr>
            <td colspan=1 > path</td>
            <td> str  </td>
            <td></td>
            <td></td>
            <td></td>
            <td> <br> The path of the SMB share. This parameter will be mandatory only for the create operation. This is the absolute path for System Access Zone and the relative path for non-System Access Zone. </td>
        </tr>
                    <tr>
            <td colspan=1 > access_zone</td>
            <td> str  </td>
            <td></td>
            <td> System </td>
            <td></td>
            <td> <br> Access zone which contains this share. If not specified it will be considered as a System Access Zone.  <br> For a non-System Access Zone the effective path where the SMB is created will be determined by the base path of the Access Zone and the path provided by the user in the playbook.  <br> For a System Access Zone the effective path will be the absolute path provided by the user in the playbook. </td>
        </tr>
                    <tr>
            <td colspan=1 > new_share_name</td>
            <td> str  </td>
            <td></td>
            <td></td>
            <td></td>
            <td> <br> The new name of the SMB share. </td>
        </tr>
                    <tr>
            <td colspan=1 > description</td>
            <td> str  </td>
            <td></td>
            <td></td>
            <td></td>
            <td> <br> Description about the SMB share. </td>
        </tr>
                    <tr>
            <td colspan=1 > permissions</td>
            <td> list   <br> elements: dict </td>
            <td></td>
            <td></td>
            <td></td>
            <td> <br> Specifies permission for specific user, group, or trustee. Valid options read, write, and full.  <br> This is a list of dictionaries. Each dictionry entry has 3 mandatory values-  <br> a)'user_name'/'group_name'/'wellknown' can have actual name of the trustee like 'user'/'group'/'wellknown'  <br> b)'permission' can be 'read'/''write'/'full'  <br> c)'permission_type' can be 'allow'/'deny'  <br> The fourth entry 'provider_type' is optional (default is 'local')  <br> d)'provider_type' can be 'local'/'file'/'ads'/'ldap' </td>
        </tr>
                    <tr>
            <td colspan=1 > access_based_enumeration</td>
            <td> bool  </td>
            <td></td>
            <td></td>
            <td></td>
            <td> <br> Only enumerates files and folders for the requesting user has access to. </td>
        </tr>
                    <tr>
            <td colspan=1 > access_based_enumeration_root_only</td>
            <td> bool  </td>
            <td></td>
            <td></td>
            <td></td>
            <td> <br> Access-based enumeration on only the root directory of the share. </td>
        </tr>
                    <tr>
            <td colspan=1 > browsable</td>
            <td> bool  </td>
            <td></td>
            <td></td>
            <td></td>
            <td> <br> Share is visible in net view and the browse list. </td>
        </tr>
                    <tr>
            <td colspan=1 > ntfs_acl_support</td>
            <td> bool  </td>
            <td></td>
            <td></td>
            <td></td>
            <td> <br> Support NTFS ACLs on files and directories. </td>
        </tr>
                    <tr>
            <td colspan=1 > directory_create_mask</td>
            <td> str  </td>
            <td></td>
            <td></td>
            <td></td>
            <td> <br> Directory creates mask bits. Octal value for owner, group, and others vs read, write, and execute </td>
        </tr>
                    <tr>
            <td colspan=1 > directory_create_mode</td>
            <td> str  </td>
            <td></td>
            <td></td>
            <td></td>
            <td> <br> Directory creates mode bits. Octal value for owner, group, and others vs read, write, and execute </td>
        </tr>
                    <tr>
            <td colspan=1 > file_create_mask</td>
            <td> str  </td>
            <td></td>
            <td></td>
            <td></td>
            <td> <br> File creates mask bits. Octal value for owner, group, and others vs read, write, and execute </td>
        </tr>
                    <tr>
            <td colspan=1 > file_create_mode</td>
            <td> str  </td>
            <td></td>
            <td></td>
            <td></td>
            <td> <br> File creates mode bits. Octal value for owner, group, and others vs read, write, and execute </td>
        </tr>
                    <tr>
            <td colspan=1 > state</td>
            <td> str  </td>
            <td> True </td>
            <td></td>
            <td> <ul> <li>absent</li>  <li>present</li> </ul></td>
            <td> <br> Defines whether the SMB share should exist or not. </td>
        </tr>
                    <tr>
            <td colspan=1 > onefs_host</td>
            <td> str  </td>
            <td> True </td>
            <td></td>
            <td></td>
            <td> <br> IP address or FQDN of the PowerScale cluster. </td>
        </tr>
                    <tr>
            <td colspan=1 > port_no</td>
            <td> str  </td>
            <td></td>
            <td> 8080 </td>
            <td></td>
            <td> <br> Port number of the PowerScale cluster.It defaults to 8080 if not specified. </td>
        </tr>
                    <tr>
            <td colspan=1 > verify_ssl</td>
            <td> bool  </td>
            <td> True </td>
            <td></td>
            <td> <ul> <li>True</li>  <li>False</li> </ul></td>
            <td> <br> boolean variable to specify whether to validate SSL certificate or not.  <br> True - indicates that the SSL certificate should be verified.  <br> False - indicates that the SSL certificate should not be verified. </td>
        </tr>
                    <tr>
            <td colspan=1 > api_user</td>
            <td> str  </td>
            <td> True </td>
            <td></td>
            <td></td>
            <td> <br> username of the PowerScale cluster. </td>
        </tr>
                    <tr>
            <td colspan=1 > api_password</td>
            <td> str  </td>
            <td> True </td>
            <td></td>
            <td></td>
            <td> <br> the password of the PowerScale cluster. </td>
        </tr>
                                            </table>


### Examples
```
    - name: Create SMB share for non system access zone
      dellemc_powerscale_smb:
        onefs_host: "{{onefs_host}}"
        verify_ssl: "{{verify_ssl}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        share_name: "{{name}}"
        path: "<path>"
        access_zone: "{{non_system_access_zone}}"
        state: "{{state_present}}"

    - name: Create SMB share for system access zone
      dellemc_powerscale_smb:
        onefs_host: "{{onefs_host}}"
        verify_ssl: "{{verify_ssl}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        share_name: "{{name}}"
        path: "<system_az_path>"
        description: "{{description}}"
        permissions:
          - user_name: "{{system_az_user}}"
            permission: "full"
            permission_type: "allow"
          - group_name: "{{system_az_group}}"
            permission: "read"
            permission_type: "allow"
          - wellknown: "everyone"
            permission: "read"
            permission_type: "allow"
      state: "{{state_present}}"

    - name: Modify user permission for SMB share
      dellemc_powerscale_smb:
        onefs_host: "{{onefs_host}}"
        verify_ssl: "{{verify_ssl}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        share_name: "{{name}}"
        path: "<system_az_path>"
        description: "{{description}}"
        permissions:
          - user_name: "{{system_az_user}}"
            permission: "full"
            permission_type: "allow"
          - group_name: "{{system_az_group}}"
            permission: "write"
            permission_type: "allow"
          - wellknown: "everyone"
            permission: "write"
            permission_type: "deny"
        state: "{{state_present}}"

    - name: Delete system access zone SMB share
      dellemc_powerscale_smb:
        onefs_host: "{{onefs_host}}"
        verify_ssl: "{{verify_ssl}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        share_name: "{{name}}"
        state: "{{state_absent}}"

    - name: Get SMB share details
      dellemc_powerscale_smb:
        onefs_host: "{{onefs_host}}"
        verify_ssl: "{{verify_ssl}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        share_name: "{{name}}"
        state: "{{state_present}}"

    - name: Create SMB share for non system access zone
      dellemc_powerscale_smb:
        onefs_host: "{{onefs_host}}"
        verify_ssl: "{{verify_ssl}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        share_name: "{{name}}"
        path: "<non_system_az_path>"
        access_zone: "{{non_system_access_zone}}"
        description: "{{description}}"
        permissions:
          - user_name: "{{non_system_az_user}}"
            permission: "full"
            permission_type: "allow"
          - group_name: "{{non_system_az_group}}"
            permission: "read"
            permission_type: "allow"
          - wellknown: "everyone"
            permission: "read"
            permission_type: "allow"
        state: "{{state_present}}"

    - name: Modify description for an non system access zone SMB share
      dellemc_powerscale_smb:
        onefs_host: "{{onefs_host}}"
        verify_ssl: "{{verify_ssl}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        share_name: "{{name}}"
        access_zone: "{{non_system_access_zone}}"
        description: "new description"
        state: "{{state_present}}"

    - name: Modify name for an existing non system access zone SMB share
      dellemc_powerscale_smb:
        onefs_host: "{{onefs_host}}"
        verify_ssl: "{{verify_ssl}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        share_name: "{{name}}"
        new_share_name: "{{new_name}}"
        access_zone: "{{non_system_access_zone}}"
        description: "new description"
        state: "{{state_present}}"
```

### Return Values
                                                                                                                                                                                                                                                                                                                                                                                                                            
<table>
    <tr>
        <th colspan=2>Key</th>
        <th>Type</th>
        <th>Returned</th>
        <th width="100%">Description</th>
    </tr>
                                                                                    <tr>
            <td colspan=2 > changed </td>
            <td>  bool </td>
            <td> always </td>
            <td> A boolean indicating if the task had to make changes. </td>
        </tr>
                    <tr>
            <td colspan=2 > smb_details </td>
            <td>  complex </td>
            <td> always </td>
            <td> Details of the SMB Share. </td>
        </tr>
                            <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > browsable </td>
                <td> bool </td>
                <td>success</td>
                <td> Share is visible in net view and the browse list </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > description </td>
                <td> str </td>
                <td>success</td>
                <td> Description of the SMB Share </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > directory_create_mask </td>
                <td> int </td>
                <td>success</td>
                <td> Directory create mask bit for SMB Share </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > directory_create_mask(octal) </td>
                <td> str </td>
                <td>success</td>
                <td> Directory create mask bit for SMB Share in octal format </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > directory_create_mode </td>
                <td> int </td>
                <td>success</td>
                <td> Directory create mode bit for SMB Share </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > directory_create_mode(octal) </td>
                <td> str </td>
                <td>success</td>
                <td> Directory create mode bit for SMB Share in octal format </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > file_create_mask </td>
                <td> int </td>
                <td>success</td>
                <td> File create mask bit for SMB Share </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > file_create_mask(octal) </td>
                <td> str </td>
                <td>success</td>
                <td> File create mask bit for SMB Share in octal format </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > file_create_mode </td>
                <td> int </td>
                <td>success</td>
                <td> File create mode bit for SMB Share </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > file_create_mode(octal) </td>
                <td> str </td>
                <td>success</td>
                <td> File create mode bit for SMB Share in octal format </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > id </td>
                <td> str </td>
                <td>success</td>
                <td> Id of the SMB Share </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > name </td>
                <td> str </td>
                <td>success</td>
                <td> Name of the SMB Share </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > path </td>
                <td> str </td>
                <td>success</td>
                <td> Path of the SMB Share </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > permission </td>
                <td> list </td>
                <td>success</td>
                <td> permission on the of the SMB Share for user/group/wellknown </td>
            </tr>
                                        </table>

### Authors
* Arindam Datta (@dattaarindam) <ansible.team@dell.com>

--------------------------------
# Snapshot Module

Manage snapshots on Dell EMC PowerScale.

### Synopsis
 You can perform the following operations
 Managing snapshots on PowerScale.
 Create a filesystem snapshot.
 Modify a filesystem snapshot.
 Get details of a filesystem snapshot.
 Delete a filesystem snapshot.

### Parameters
                                                                                                                                                                                                                                                                                                                                    
<table>
    <tr>
        <th colspan=1>Parameter</th>
        <th width="20%">Type</th>
        <th>Required</th>
        <th>Default</th>
        <th>Choices</th>
        <th width="80%">Description</th>
    </tr>
                                                            <tr>
            <td colspan=1 > snapshot_name</td>
            <td> str  </td>
            <td> True </td>
            <td></td>
            <td></td>
            <td> <br> The name of the snapshot. </td>
        </tr>
                    <tr>
            <td colspan=1 > path</td>
            <td> str  </td>
            <td></td>
            <td></td>
            <td></td>
            <td> <br> Specifies the filesystem path. It is the absolute path for System access zone and it is relative if using non-System access zone. For example, if your access zone is 'Ansible' and it has a base path '/ifs/ansible' and the path specified is '/user1', then the effective path would be '/ifs/ansible/user1'. If your access zone is System, and you have 'directory1' in the access zone, the path provided should be '/ifs/directory1'. </td>
        </tr>
                    <tr>
            <td colspan=1 > access_zone</td>
            <td> str  </td>
            <td></td>
            <td> System </td>
            <td></td>
            <td> <br> The effective path where the Snapshot is created will be determined by the base path of the Access Zone and the path provided by the user in the playbook. </td>
        </tr>
                    <tr>
            <td colspan=1 > new_snapshot_name</td>
            <td> str  </td>
            <td></td>
            <td></td>
            <td></td>
            <td> <br> The new name of the snapshot. </td>
        </tr>
                    <tr>
            <td colspan=1 > expiration_timestamp</td>
            <td> str  </td>
            <td></td>
            <td></td>
            <td></td>
            <td> <br> The timestamp on which the snapshot will expire (UTC format).  <br> Either this or desired retention can be specified, but not both. </td>
        </tr>
                    <tr>
            <td colspan=1 > desired_retention</td>
            <td> str  </td>
            <td></td>
            <td></td>
            <td></td>
            <td> <br> The number of days for which the snapshot can be retained.  <br> Either this or expiration timestamp can be specified, but not both. </td>
        </tr>
                    <tr>
            <td colspan=1 > retention_unit</td>
            <td> str  </td>
            <td></td>
            <td></td>
            <td> <ul> <li>hours</li>  <li>days</li> </ul></td>
            <td> <br> The retention unit for the snapshot.  <br> The default value is hours. </td>
        </tr>
                    <tr>
            <td colspan=1 > alias</td>
            <td> str  </td>
            <td></td>
            <td></td>
            <td></td>
            <td> <br> The alias for the snapshot. </td>
        </tr>
                    <tr>
            <td colspan=1 > state</td>
            <td> str  </td>
            <td> True </td>
            <td></td>
            <td> <ul> <li>absent</li>  <li>present</li> </ul></td>
            <td> <br> Defines whether the snapshot should exist or not. </td>
        </tr>
                    <tr>
            <td colspan=1 > onefs_host</td>
            <td> str  </td>
            <td> True </td>
            <td></td>
            <td></td>
            <td> <br> IP address or FQDN of the PowerScale cluster. </td>
        </tr>
                    <tr>
            <td colspan=1 > port_no</td>
            <td> str  </td>
            <td></td>
            <td> 8080 </td>
            <td></td>
            <td> <br> Port number of the PowerScale cluster.It defaults to 8080 if not specified. </td>
        </tr>
                    <tr>
            <td colspan=1 > verify_ssl</td>
            <td> bool  </td>
            <td> True </td>
            <td></td>
            <td> <ul> <li>True</li>  <li>False</li> </ul></td>
            <td> <br> boolean variable to specify whether to validate SSL certificate or not.  <br> True - indicates that the SSL certificate should be verified.  <br> False - indicates that the SSL certificate should not be verified. </td>
        </tr>
                    <tr>
            <td colspan=1 > api_user</td>
            <td> str  </td>
            <td> True </td>
            <td></td>
            <td></td>
            <td> <br> username of the PowerScale cluster. </td>
        </tr>
                    <tr>
            <td colspan=1 > api_password</td>
            <td> str  </td>
            <td> True </td>
            <td></td>
            <td></td>
            <td> <br> the password of the PowerScale cluster. </td>
        </tr>
                                            </table>


### Examples
```
    - name: Create a filesystem snapshot on PowerScale
      dellemc_powerscale_snapshot:
        onefs_host: "{{onefs_host}}"
        verify_ssl: "{{verify_ssl}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        path: "<path>"
        access_zone: "{{access_zone}}"
        snapshot_name: "{{snapshot_name}}"
        desired_retention: "{{desired_retention}}"
        retention_unit: "{{retention_unit_days}}"
        alias: "{{ansible_snap_alias}}"
        state: "{{present}}"

    - name: Get details of a filesystem snapshot
      dellemc_powerscale_snapshot:
        onefs_host: "{{onefs_host}}"
        verify_ssl: "{{verify_ssl}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        snapshot_name: "{{snapshot_name}}"
        state: "{{present}}"

    - name: Modify filesystem snapshot desired retention
      dellemc_powerscale_snapshot:
        onefs_host: "{{onefs_host}}"
        verify_ssl: "{{verify_ssl}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        snapshot_name: "{{snapshot_name}}"
        desired_retention: "{{desired_retention_new}}"
        retention_unit: "{{retention_unit_days}}"
        state: "{{present}}"

    - name: Modify filesystem snapshot expiration timestamp
      dellemc_powerscale_snapshot:
        onefs_host: "{{onefs_host}}"
        verify_ssl: "{{verify_ssl}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        snapshot_name: "{{snapshot_name}}"
        expiration_timestamp: "{{expiration_timestamp_new}}"
        state: "{{present}}"

    - name: Modify filesystem snapshot alias
      dellemc_powerscale_snapshot:
        onefs_host: "{{onefs_host}}"
        verify_ssl: "{{verify_ssl}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        snapshot_name: "{{snapshot_name}}"
        alias: "{{ansible_snap_alias_new}}"
        state: "{{present}}"

    - name: Delete snapshot alias
      dellemc_powerscale_snapshot:
        onefs_host: "{{onefs_host}}"
        verify_ssl: "{{verify_ssl}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        snapshot_name: "{{snapshot_name}}"
        alias: ""
        state: "{{present}}"

    - name: Rename filesystem snapshot
      dellemc_powerscale_snapshot:
        onefs_host: "{{onefs_host}}"
        verify_ssl: "{{verify_ssl}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        snapshot_name: "{{snapshot_name}}"
        new_snapshot_name: "{{new_snapshot_name}}"
        state: "{{present}}"

    - name: Delete filesystem snapshot
      dellemc_powerscale_snapshot:
        onefs_host: "{{onefs_host}}"
        verify_ssl: "{{verify_ssl}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        snapshot_name: "{{new_snapshot_name}}"
        state: "{{absent}}"
```

### Return Values
                                                                                                                                                                                                                                                                                                                                                                                                        
<table>
    <tr>
        <th colspan=2>Key</th>
        <th>Type</th>
        <th>Returned</th>
        <th width="100%">Description</th>
    </tr>
                                                                                    <tr>
            <td colspan=2 > changed </td>
            <td>  bool </td>
            <td> always </td>
            <td> Whether or not the resource has changed </td>
        </tr>
                    <tr>
            <td colspan=2 > snapshot_details </td>
            <td>  complex </td>
            <td> When snapshot exists. </td>
            <td> The snapshot details. </td>
        </tr>
                            <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > alias </td>
                <td> str </td>
                <td>success</td>
                <td> Snapshot alias. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > created </td>
                <td> int </td>
                <td>success</td>
                <td> The creation timestamp. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > expires </td>
                <td> int </td>
                <td>success</td>
                <td> The expiration timestamp. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > has_locks </td>
                <td> bool </td>
                <td>success</td>
                <td> Whether the snapshot has locks. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > id </td>
                <td> int </td>
                <td>success</td>
                <td> The snapshot ID. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > name </td>
                <td> str </td>
                <td>success</td>
                <td> The name of the snapshot. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > path </td>
                <td> str </td>
                <td>success</td>
                <td> The directory path whose snapshot has been taken. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > pct_filesystem </td>
                <td> float </td>
                <td>success</td>
                <td> The percentage of filesystem used. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > pct_reserve </td>
                <td> float </td>
                <td>success</td>
                <td> The percentage of filesystem reserved. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > size </td>
                <td> int </td>
                <td>success</td>
                <td> The snapshot size. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > state </td>
                <td> str </td>
                <td>success</td>
                <td> The state of the snapshot. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > target_id </td>
                <td> int </td>
                <td>success</td>
                <td> target ID of snapshot whose alias it is. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > target_name </td>
                <td> str </td>
                <td>success</td>
                <td> target name of snapshot whose alias it is. </td>
            </tr>
                                        </table>

### Authors
* Prashant Rakheja (@prashant-dell) <ansible.team@dell.com>

--------------------------------
# SyncIQ Performance Rules Module

Manage SyncIQ performance rules on PowerScale

### Synopsis
 Managing SyncIQ performance rules on PowerScale includes create a SyncIQ performance rule, modify a SyncIQ performance rule, get details of a SyncIQ performance rule, delete a SyncIQ performance rule

### Parameters
                                                                                                                                                                                                                                                                                                                                        
<table>
    <tr>
        <th colspan=2>Parameter</th>
        <th width="20%">Type</th>
        <th>Required</th>
        <th>Default</th>
        <th>Choices</th>
        <th width="80%">Description</th>
    </tr>
                                                            <tr>
            <td colspan=2 > rule_type</td>
            <td> str  </td>
            <td></td>
            <td></td>
            <td> <ul> <li>bandwidth</li>  <li>file_count</li>  <li>cpu</li>  <li>worker</li> </ul></td>
            <td> <br> The type of system resource this rule limits.  <br> This is mandatory parameter while creating/deleting a performance rule  <br> This cannot be modified. </td>
        </tr>
                    <tr>
            <td colspan=2 > sync_rule_id</td>
            <td> str  </td>
            <td></td>
            <td></td>
            <td></td>
            <td> <br> This is an auto generated ID at the time of creation of SyncIQ performance rule.  <br> For get/modify/delete operations sync_rule_id is required.  <br> The ID of a performance rule is not absolute to a particular existing rule configuration. The IDs are auto-sequenced during creation/deletion of a performance rule. </td>
        </tr>
                    <tr>
            <td colspan=2 > limit</td>
            <td> int  </td>
            <td></td>
            <td></td>
            <td></td>
            <td> <br> It tells the amount the specified system resource type is limited by this rule.  <br> Units are kb/s for bandwidth, files/s for file-count, processing percentage used for cpu, or percentage of maximum available workers.  <br> This is a mandatory parameter while creating/deleting a performance rule. </td>
        </tr>
                    <tr>
            <td colspan=2 > description</td>
            <td> str  </td>
            <td></td>
            <td></td>
            <td></td>
            <td> <br> User entered description of the performance rule. </td>
        </tr>
                    <tr>
            <td colspan=2 > enabled</td>
            <td> bool  </td>
            <td></td>
            <td></td>
            <td></td>
            <td> <br> Indicates whether the performance rule is currently in effect during its specified interval  <br> This mandatory while creating/deleting a performance rule. </td>
        </tr>
                    <tr>
            <td colspan=2 > schedule</td>
            <td> dict  </td>
            <td></td>
            <td></td>
            <td></td>
            <td> <br> A schedule defining when during a week this performance rule is in effect.  <br> It is mandatory to enter schedule while creating/deleting a performance rule. </td>
        </tr>
                            <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > begin </td>
                <td> str  </td>
                <td></td>
                <td></td>
                <td></td>
                <td>  <br> Start time for this schedule, during its specified days.  <br> It is of the format hh:mm (24 hour format).  </td>
            </tr>
                    <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > end </td>
                <td> str  </td>
                <td></td>
                <td></td>
                <td></td>
                <td>  <br> End time for this schedule, during its specified days.  <br> It is of the format hh:mm (24 hour format).  </td>
            </tr>
                    <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > days_of_week </td>
                <td> list   <br> elements: str </td>
                <td></td>
                <td></td>
                <td> <ul> <li>monday</li>  <li>tuesday</li>  <li>wednesday</li>  <li>thursday</li>  <li>friday</li>  <li>saturday</li>  <li>sunday</li> </ul></td>
                <td>  <br> The days in a week when the performance rule is effective.  </td>
            </tr>
                            <tr>
            <td colspan=2 > state</td>
            <td> str  </td>
            <td> True </td>
            <td></td>
            <td> <ul> <li>absent</li>  <li>present</li> </ul></td>
            <td> <br> The state option is used to determine whether the performance rule exists or not. </td>
        </tr>
                    <tr>
            <td colspan=2 > onefs_host</td>
            <td> str  </td>
            <td> True </td>
            <td></td>
            <td></td>
            <td> <br> IP address or FQDN of the PowerScale cluster. </td>
        </tr>
                    <tr>
            <td colspan=2 > port_no</td>
            <td> str  </td>
            <td></td>
            <td> 8080 </td>
            <td></td>
            <td> <br> Port number of the PowerScale cluster.It defaults to 8080 if not specified. </td>
        </tr>
                    <tr>
            <td colspan=2 > verify_ssl</td>
            <td> bool  </td>
            <td> True </td>
            <td></td>
            <td> <ul> <li>True</li>  <li>False</li> </ul></td>
            <td> <br> boolean variable to specify whether to validate SSL certificate or not.  <br> True - indicates that the SSL certificate should be verified.  <br> False - indicates that the SSL certificate should not be verified. </td>
        </tr>
                    <tr>
            <td colspan=2 > api_user</td>
            <td> str  </td>
            <td> True </td>
            <td></td>
            <td></td>
            <td> <br> username of the PowerScale cluster. </td>
        </tr>
                    <tr>
            <td colspan=2 > api_password</td>
            <td> str  </td>
            <td> True </td>
            <td></td>
            <td></td>
            <td> <br> the password of the PowerScale cluster. </td>
        </tr>
                                                    </table>

### Notes
* Operations performed in parallel from other interfaces apart from playbook cannot guarantee desirable results.

### Examples
```
  - name: Create SyncIQ performance rule
    dellemc_powerscale_synciqrules:
      onefs_host: "{{onefs_host}}"
      verify_ssl: "{{verify_ssl}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      description: "Create a rule"
      enabled: True
      schedule:
        begin: "00:00"
        end: "13:30"
        days_of_week:
            - "monday"
            - "tuesday"
            - "sunday"
      rule_type: "cpu"
      limit: "80"
      state: "present"

  - name: Modify SyncIQ performance rule
    dellemc_powerscale_synciqpolicy:
      onefs_host: "{{onefs_host}}"
      verify_ssl: "{{verify_ssl}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      sync_rule_id: "cpu-0"
      limit: "85"
      description: "Modify the performance rule"
      state: "present"

  - name: Get SyncIQ performance rule details
    dellemc_powerscale_synciqpolicy:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      sync_rule_id: "cpu-0"
      state: "present"

  - name: Delete SyncIQ performance rule
    dellemc_powerscale_synciqpolicy:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      sync_rule_id: "cpu-0"
      enabled: True
      schedule:
        begin: "00:00"
        end: "13:30"
        days_of_week:
            - "monday"
            - "tuesday"
            - "sunday"
      rule_type: "bandwidth"
      limit: "85"
      state: "absent"
```

### Return Values
                                                                                                                                                                                                                                                                
<table>
    <tr>
        <th colspan=2>Key</th>
        <th>Type</th>
        <th>Returned</th>
        <th width="100%">Description</th>
    </tr>
                                                                                            <tr>
            <td colspan=2 > changed </td>
            <td>  bool </td>
            <td> always </td>
            <td> Whether or not the resource has changed </td>
        </tr>
                    <tr>
            <td colspan=2 > sync_rule_details </td>
            <td>  complex </td>
            <td> When SyncIQ performance rule exists </td>
            <td> Details of the SyncIQ performance rule </td>
        </tr>
                            <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > description </td>
                <td> str </td>
                <td>success</td>
                <td> Description of the performance rule. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > enabled </td>
                <td> bool </td>
                <td>success</td>
                <td> Indicates whether performance rule is enabled </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > id </td>
                <td> str </td>
                <td>success</td>
                <td> ID of the performance rule. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > limit </td>
                <td> int </td>
                <td>success</td>
                <td> Amount the specified system resource type is limited by this rule </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > schedule </td>
                <td> str </td>
                <td>success</td>
                <td> Duration when performance rule is effective </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > type </td>
                <td> str </td>
                <td>success</td>
                <td> Type of performance rule </td>
            </tr>
                                        </table>

### Authors
* Spandita Panigrahi (@panigs7) <ansible.team@dell.com>

--------------------------------
# Accesszone Module

Manages access zones on PowerScale

### Synopsis
 Managing access zones on the PowerScale storage system includes getting details of the access zone and modifying the smb and nfs settings.

### Parameters
                                                                                                                                                                                                                                                                                                                                                                    
<table>
    <tr>
        <th colspan=2>Parameter</th>
        <th width="20%">Type</th>
        <th>Required</th>
        <th>Default</th>
        <th>Choices</th>
        <th width="80%">Description</th>
    </tr>
                                                            <tr>
            <td colspan=2 > az_name</td>
            <td> str  </td>
            <td> True </td>
            <td></td>
            <td></td>
            <td> <br> The name of the access zone. </td>
        </tr>
                    <tr>
            <td colspan=2 > smb</td>
            <td> dict  </td>
            <td></td>
            <td></td>
            <td></td>
            <td> <br> Specifies the default SMB setting parameters of access zone. </td>
        </tr>
                            <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > create_permissions </td>
                <td> str  </td>
                <td></td>
                <td> default acl </td>
                <td> <ul> <li>default acl</li>  <li>Inherit mode bits</li>  <li>Use create mask and mode</li> </ul></td>
                <td>  <br> Sets the default source permissions to apply when a file or directory is created.  </td>
            </tr>
                    <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > directory_create_mask </td>
                <td> str  </td>
                <td></td>
                <td></td>
                <td></td>
                <td>  <br> Specifies the UNIX mask bits(octal) that are removed when a directory is created, restricting permissions.  <br> Mask bits are applied before mode bits are applied.  </td>
            </tr>
                    <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > directory_create_mode </td>
                <td> str  </td>
                <td></td>
                <td></td>
                <td></td>
                <td>  <br> Specifies the UNIX mode bits(octal) that are added when a directory is created, enabling permissions.  </td>
            </tr>
                    <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > file_create_mask </td>
                <td> str  </td>
                <td></td>
                <td></td>
                <td></td>
                <td>  <br> Specifies the UNIX mask bits(octal) that are removed when a file is created, restricting permissions.  </td>
            </tr>
                    <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > file_create_mode </td>
                <td> str  </td>
                <td></td>
                <td></td>
                <td></td>
                <td>  <br> Specifies the UNIX mode bits(octal) that are added when a file is created, enabling permissions.  </td>
            </tr>
                    <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > access_based_enumeration </td>
                <td> bool  </td>
                <td></td>
                <td></td>
                <td></td>
                <td>  <br> Allows access based enumeration only on the files and folders that the requesting user can access.  </td>
            </tr>
                    <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > access_based_enumeration_root_only </td>
                <td> bool  </td>
                <td></td>
                <td></td>
                <td></td>
                <td>  <br> Access-based enumeration on only the root directory of the share.  </td>
            </tr>
                    <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > ntfs_acl_support </td>
                <td> bool  </td>
                <td></td>
                <td></td>
                <td></td>
                <td>  <br> Allows ACLs to be stored and edited from SMB clients.  </td>
            </tr>
                    <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > oplocks </td>
                <td> bool  </td>
                <td></td>
                <td></td>
                <td></td>
                <td>  <br> An oplock allows clients to provide performance improvements by using locally-cached information.  </td>
            </tr>
                            <tr>
            <td colspan=2 > nfs</td>
            <td> dict  </td>
            <td></td>
            <td></td>
            <td></td>
            <td> <br> Specifies the default NFS setting parameters of access zone. </td>
        </tr>
                            <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > commit_asynchronous </td>
                <td> bool  </td>
                <td></td>
                <td></td>
                <td></td>
                <td>  <br> Set to True if NFS commit requests execute asynchronously.  </td>
            </tr>
                    <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > nfsv4_domain </td>
                <td> str  </td>
                <td></td>
                <td></td>
                <td></td>
                <td>  <br> Specifies the domain or realm through which users and groups are associated.  </td>
            </tr>
                    <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > nfsv4_allow_numeric_ids </td>
                <td> bool  </td>
                <td></td>
                <td></td>
                <td></td>
                <td>  <br> If true, sends owners and groups as UIDs and GIDs when look up fails or if the 'nfsv4_no_name' property is set to 1.  </td>
            </tr>
                    <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > nfsv4_no_domain </td>
                <td> bool  </td>
                <td></td>
                <td></td>
                <td></td>
                <td>  <br> If true, sends owners and groups without a domain name.  </td>
            </tr>
                    <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > nfsv4_no_domain_uids </td>
                <td> bool  </td>
                <td></td>
                <td></td>
                <td></td>
                <td>  <br> If true, sends UIDs and GIDs without a domain name.  </td>
            </tr>
                    <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > nfsv4_no_names </td>
                <td> bool  </td>
                <td></td>
                <td></td>
                <td></td>
                <td>  <br> If true, sends owners and groups as UIDs and GIDs.  </td>
            </tr>
                            <tr>
            <td colspan=2 > provider_state</td>
            <td> str  </td>
            <td></td>
            <td></td>
            <td> <ul> <li>add</li>  <li>remove</li> </ul></td>
            <td> <br> Defines whether the auth providers should be added or removed from access zone.  <br> If auth_providers are given, then provider_state should also be specified.  <br> add - indicates that the auth providers should be added to the access zone.  <br> remove - indicates that auth providers should be removed from the access zone. </td>
        </tr>
                    <tr>
            <td colspan=2 > auth_providers</td>
            <td> list   <br> elements: dict </td>
            <td></td>
            <td></td>
            <td></td>
            <td> <br> Specifies the auth providers which needs to be added or removed from access zone.  <br> If auth_providers are given, then provider_state should also be specified. </td>
        </tr>
                            <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > provider_name </td>
                <td> str  </td>
                <td> True </td>
                <td></td>
                <td></td>
                <td>  <br> Specifies the auth provider name which needs to be added or removed from access zone.  </td>
            </tr>
                    <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > provider_type </td>
                <td> str  </td>
                <td> True </td>
                <td></td>
                <td> <ul> <li>local</li>  <li>file</li>  <li>ldap</li>  <li>ads</li> </ul></td>
                <td>  <br> Specifies the auth provider type which needs to be added or removed from access zone.  </td>
            </tr>
                            <tr>
            <td colspan=2 > state</td>
            <td> str  </td>
            <td> True </td>
            <td></td>
            <td> <ul> <li>present</li>  <li>absent</li> </ul></td>
            <td> <br> Defines whether the access zone should exist or not.  <br> present - indicates that the access zone should exist on the system.  <br> absent - indicates that the access zone should not exist on the system. </td>
        </tr>
                    <tr>
            <td colspan=2 > onefs_host</td>
            <td> str  </td>
            <td> True </td>
            <td></td>
            <td></td>
            <td> <br> IP address or FQDN of the PowerScale cluster. </td>
        </tr>
                    <tr>
            <td colspan=2 > port_no</td>
            <td> str  </td>
            <td></td>
            <td> 8080 </td>
            <td></td>
            <td> <br> Port number of the PowerScale cluster.It defaults to 8080 if not specified. </td>
        </tr>
                    <tr>
            <td colspan=2 > verify_ssl</td>
            <td> bool  </td>
            <td> True </td>
            <td></td>
            <td> <ul> <li>True</li>  <li>False</li> </ul></td>
            <td> <br> boolean variable to specify whether to validate SSL certificate or not.  <br> True - indicates that the SSL certificate should be verified.  <br> False - indicates that the SSL certificate should not be verified. </td>
        </tr>
                    <tr>
            <td colspan=2 > api_user</td>
            <td> str  </td>
            <td> True </td>
            <td></td>
            <td></td>
            <td> <br> username of the PowerScale cluster. </td>
        </tr>
                    <tr>
            <td colspan=2 > api_password</td>
            <td> str  </td>
            <td> True </td>
            <td></td>
            <td></td>
            <td> <br> the password of the PowerScale cluster. </td>
        </tr>
                                                    </table>

### Notes
* Creation/Deletion of access zone is not allowed through the Ansible module.

### Examples
```
- name: Get details of access zone including smb and nfs settings
  dellemc_powerscale_accesszone:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      az_name: "{{access zone}}"
      state: "present"

- name: Modify smb settings of access zone
  dellemc_powerscale_accesszone:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      az_name: "{{access zone}}"
      state: "present"
      smb:
        create_permissions: 'default acl'
        directory_create_mask: '777'
        directory_create_mode: '700'
        file_create_mask: '700'
        file_create_mode: '100'
        access_based_enumeration: true
        access_based_enumeration_root_only: false
        ntfs_acl_support: true
        oplocks: true

- name: Modify nfs settings of access zone
  dellemc_powerscale_accesszone:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      az_name: "{{access zone}}"
      state: "present"
      nfs:
        commit_asynchronous: false
        nfsv4_allow_numeric_ids: false
        nfsv4_domain: 'localhost'
        nfsv4_no_domain: false
        nfsv4_no_domain_uids: false
        nfsv4_no_names: false

- name: Modify smb and nfs settings of access zone
  dellemc_powerscale_accesszone:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      az_name: "{{access zone}}"
      state: "present"
      smb:
        create_permissions: 'default acl'
        directory_create_mask: '777'
        directory_create_mode: '700'
        file_create_mask: '700'
        file_create_mode: '100'
        access_based_enumeration: true
        access_based_enumeration_root_only: false
        ntfs_acl_support: true
        oplocks: true
      nfs:
        commit_asynchronous: false
        nfsv4_allow_numeric_ids: false
        nfsv4_domain: 'localhost'
        nfsv4_no_domain: false
        nfsv4_no_domain_uids: false
        nfsv4_no_names: false

- name: Add Auth Providers to the  access zone
  dellemc_powerscale_accesszone:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      az_name: "{{access zone}}"
      provider_state: "add"
      auth_providers:
         - provider_name: "System"
           provider_type: "file"
         - provider_name: "ldap-prashant"
           provider_type: "ldap"
      state: "present"

- name: Remove Auth Providers from the  access zone
  dellemc_powerscale_accesszone:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      az_name: "{{access zone}}"
      provider_state: "remove"
      auth_providers:
         - provider_name: "System"
           provider_type: "file"
      state: "present"
```

### Return Values
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
<table>
    <tr>
        <th colspan=6>Key</th>
        <th>Type</th>
        <th>Returned</th>
        <th width="100%">Description</th>
    </tr>
                                                                                            <tr>
            <td colspan=6 > access_zone_details </td>
            <td>  complex </td>
            <td> When access zone exists </td>
            <td> The access zone details </td>
        </tr>
                            <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=5 > nfs_settings </td>
                <td> complex </td>
                <td>success</td>
                <td> NFS settings of access zone </td>
            </tr>
                                         <tr>
                    <td class="elbow-placeholder">&nbsp;</td>
                    <td class="elbow-placeholder">&nbsp;</td>
                    <td colspan=4 > export_settings </td>
                    <td> complex </td>
                    <td>success</td>
                    <td> Default values for NFS exports </td>
                </tr>
                                                    <tr>
                        <td class="elbow-placeholder">&nbsp;</td>
                        <td class="elbow-placeholder">&nbsp;</td>
                        <td class="elbow-placeholder">&nbsp;</td>
                        <td colspan=3 > commit_asynchronous </td>
                        <td> bool </td>
                        <td>success</td>
                        <td> Set to True if NFS commit requests execute asynchronously </td>
                    </tr>
                                                             <tr>
                    <td class="elbow-placeholder">&nbsp;</td>
                    <td class="elbow-placeholder">&nbsp;</td>
                    <td colspan=4 > zone_settings </td>
                    <td> complex </td>
                    <td>success</td>
                    <td> NFS server settings for this zone </td>
                </tr>
                                                    <tr>
                        <td class="elbow-placeholder">&nbsp;</td>
                        <td class="elbow-placeholder">&nbsp;</td>
                        <td class="elbow-placeholder">&nbsp;</td>
                        <td colspan=3 > nfsv4_allow_numeric_ids </td>
                        <td> bool </td>
                        <td>success</td>
                        <td> If true, sends owners and groups as UIDs and GIDs when look up fails or if the 'nfsv4_no_name' property is set to 1 </td>
                    </tr>
                                    <tr>
                        <td class="elbow-placeholder">&nbsp;</td>
                        <td class="elbow-placeholder">&nbsp;</td>
                        <td class="elbow-placeholder">&nbsp;</td>
                        <td colspan=3 > nfsv4_domain </td>
                        <td> str </td>
                        <td>success</td>
                        <td> Specifies the domain or realm through which users and groups are associated </td>
                    </tr>
                                    <tr>
                        <td class="elbow-placeholder">&nbsp;</td>
                        <td class="elbow-placeholder">&nbsp;</td>
                        <td class="elbow-placeholder">&nbsp;</td>
                        <td colspan=3 > nfsv4_no_domain </td>
                        <td> bool </td>
                        <td>success</td>
                        <td> If true, sends owners and groups without a domain name </td>
                    </tr>
                                    <tr>
                        <td class="elbow-placeholder">&nbsp;</td>
                        <td class="elbow-placeholder">&nbsp;</td>
                        <td class="elbow-placeholder">&nbsp;</td>
                        <td colspan=3 > nfsv4_no_domain_uids </td>
                        <td> bool </td>
                        <td>success</td>
                        <td> If true, sends UIDs and GIDs without a domain name </td>
                    </tr>
                                    <tr>
                        <td class="elbow-placeholder">&nbsp;</td>
                        <td class="elbow-placeholder">&nbsp;</td>
                        <td class="elbow-placeholder">&nbsp;</td>
                        <td colspan=3 > nfsv4_no_names </td>
                        <td> bool </td>
                        <td>success</td>
                        <td> If true, sends owners and groups as UIDs and GIDs </td>
                    </tr>
                                                                            <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=5 > smb_settings </td>
                <td> complex </td>
                <td>success</td>
                <td> SMB settings of access zone </td>
            </tr>
                                         <tr>
                    <td class="elbow-placeholder">&nbsp;</td>
                    <td class="elbow-placeholder">&nbsp;</td>
                    <td colspan=4 > directory_create_mask(octal) </td>
                    <td> str </td>
                    <td>success</td>
                    <td> UNIX mask bits for directory in octal format </td>
                </tr>
                                             <tr>
                    <td class="elbow-placeholder">&nbsp;</td>
                    <td class="elbow-placeholder">&nbsp;</td>
                    <td colspan=4 > directory_create_mode(octal) </td>
                    <td> str </td>
                    <td>success</td>
                    <td> UNIX mode bits for directory in octal format </td>
                </tr>
                                             <tr>
                    <td class="elbow-placeholder">&nbsp;</td>
                    <td class="elbow-placeholder">&nbsp;</td>
                    <td colspan=4 > file_create_mask(octal) </td>
                    <td> str </td>
                    <td>success</td>
                    <td> UNIX mask bits for file in octal format </td>
                </tr>
                                             <tr>
                    <td class="elbow-placeholder">&nbsp;</td>
                    <td class="elbow-placeholder">&nbsp;</td>
                    <td colspan=4 > file_create_mode(octal) </td>
                    <td> str </td>
                    <td>success</td>
                    <td> UNIX mode bits for file in octal format </td>
                </tr>
                                                                    <tr>
            <td colspan=6 > access_zone_modify_flag </td>
            <td>  bool </td>
            <td> on success </td>
            <td> Whether auth providers linked to access zone has changed </td>
        </tr>
                    <tr>
            <td colspan=6 > changed </td>
            <td>  bool </td>
            <td> always </td>
            <td> Whether or not the resource has changed </td>
        </tr>
                    <tr>
            <td colspan=6 > nfs_modify_flag </td>
            <td>  bool </td>
            <td> on success </td>
            <td> Whether or not the default NFS settings of access zone has changed </td>
        </tr>
                    <tr>
            <td colspan=6 > smb_modify_flag </td>
            <td>  bool </td>
            <td> on success </td>
            <td> Whether or not the default SMB settings of access zone has changed </td>
        </tr>
                    </table>

### Authors
* Akash Shendge (@shenda1) <ansible.team@dell.com>

--------------------------------
# SyncIQ Job Module

Manage SyncIQ jobs on PowerScale

### Synopsis
 Managing SyncIQ jobs on PowerScale storage system includes retrieving and modifying details of a SyncIQ job.

### Parameters
                                                                                                                                                                                                                
<table>
    <tr>
        <th colspan=1>Parameter</th>
        <th width="20%">Type</th>
        <th>Required</th>
        <th>Default</th>
        <th>Choices</th>
        <th width="80%">Description</th>
    </tr>
                                                            <tr>
            <td colspan=1 > job_id</td>
            <td> str  </td>
            <td> True </td>
            <td></td>
            <td></td>
            <td> <br> Specifies the id or name of the policy job. </td>
        </tr>
                    <tr>
            <td colspan=1 > job_state</td>
            <td> str  </td>
            <td></td>
            <td></td>
            <td> <ul> <li>run</li>  <li>pause</li>  <li>cancel</li> </ul></td>
            <td> <br> Specifies the state of the job. </td>
        </tr>
                    <tr>
            <td colspan=1 > state</td>
            <td> str  </td>
            <td> True </td>
            <td></td>
            <td> <ul> <li>absent</li>  <li>present</li> </ul></td>
            <td> <br> The state of the SyncIQ job after the task is performed.  <br> present - indicates that the SyncIQ job should exist on the system.  <br> absent - indicates that the SyncIQ job should not exist on the system. </td>
        </tr>
                    <tr>
            <td colspan=1 > onefs_host</td>
            <td> str  </td>
            <td> True </td>
            <td></td>
            <td></td>
            <td> <br> IP address or FQDN of the PowerScale cluster. </td>
        </tr>
                    <tr>
            <td colspan=1 > port_no</td>
            <td> str  </td>
            <td></td>
            <td> 8080 </td>
            <td></td>
            <td> <br> Port number of the PowerScale cluster.It defaults to 8080 if not specified. </td>
        </tr>
                    <tr>
            <td colspan=1 > verify_ssl</td>
            <td> bool  </td>
            <td> True </td>
            <td></td>
            <td> <ul> <li>True</li>  <li>False</li> </ul></td>
            <td> <br> boolean variable to specify whether to validate SSL certificate or not.  <br> True - indicates that the SSL certificate should be verified.  <br> False - indicates that the SSL certificate should not be verified. </td>
        </tr>
                    <tr>
            <td colspan=1 > api_user</td>
            <td> str  </td>
            <td> True </td>
            <td></td>
            <td></td>
            <td> <br> username of the PowerScale cluster. </td>
        </tr>
                    <tr>
            <td colspan=1 > api_password</td>
            <td> str  </td>
            <td> True </td>
            <td></td>
            <td></td>
            <td> <br> the password of the PowerScale cluster. </td>
        </tr>
                                                    </table>

### Notes
* There is delay in the actual state change of the SyncIQ job. The state change of jobs in 'scheduled' state is not supported.

### Examples
```
- name: Get SyncIQ job details
  dellemc_powerscale_synciqjob:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      job_id: "Test_SSL"
      state: "present"

- name: Pause a SyncIQ job when in running state
  dellemc_powerscale_synciqjob:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      job_id: "Test_SSL"
      job_state: "pause"
      state: "present"

- name: Resume a SyncIQ job when in paused state
  dellemc_powerscale_synciqjob:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      job_id: "Test_SSL"
      job_state: "run"
      state: "present"

- name: Cancel a SyncIQ job
  dellemc_powerscale_synciqjob:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      job_id: "Test_SSL"
      job_state: "cancel"
      state: "absent"
```

### Return Values
                                                                                                                                                                                                                                                                                                                                                            
<table>
    <tr>
        <th colspan=2>Key</th>
        <th>Type</th>
        <th>Returned</th>
        <th width="100%">Description</th>
    </tr>
                                                                                            <tr>
            <td colspan=2 > changed </td>
            <td>  bool </td>
            <td> always </td>
            <td> Whether or not the resource has changed </td>
        </tr>
                    <tr>
            <td colspan=2 > job_details </td>
            <td>  complex </td>
            <td> When SyncIQ job exists </td>
            <td> The SyncIQ job details </td>
        </tr>
                            <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > action </td>
                <td> str </td>
                <td>success</td>
                <td> The action to be taken by this job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > id </td>
                <td> str </td>
                <td>success</td>
                <td> A unique identifier for this object. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > policy_id </td>
                <td> str </td>
                <td>success</td>
                <td> The id of the policy from which the job is triggered. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > policy_name </td>
                <td> str </td>
                <td>success</td>
                <td> The name of the policy from which this job is triggered. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > state </td>
                <td> str </td>
                <td>success</td>
                <td> The state of the job. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > sync_type </td>
                <td> str </td>
                <td>success</td>
                <td> The type of sync being performed by this job. </td>
            </tr>
                                        <tr>
            <td colspan=2 > modified_job </td>
            <td>  complex </td>
            <td> When SyncIQ job is modified </td>
            <td> The modified SyncIQ job details </td>
        </tr>
                            <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > id </td>
                <td> str </td>
                <td>success</td>
                <td> A unique identifier for this object. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > state </td>
                <td> str </td>
                <td>success</td>
                <td> The state of the job. </td>
            </tr>
                                        </table>

### Authors
* Jennifer John (@johnj9) <ansible.team@dell.com>

--------------------------------
# NFS Module

Manage NFS exports on a DellEMC PowerScale system

### Synopsis
 Managing NFS exports on an PowerScale system includes creating NFS export for a directory in an access zone, adding or removing clients, modifying different parameters of the export and deleting export.

### Parameters
                                                                                                                                                                                                                                                                                                                                                                            
<table>
    <tr>
        <th colspan=1>Parameter</th>
        <th width="20%">Type</th>
        <th>Required</th>
        <th>Default</th>
        <th>Choices</th>
        <th width="80%">Description</th>
    </tr>
                                                            <tr>
            <td colspan=1 > path</td>
            <td> str  </td>
            <td> True </td>
            <td></td>
            <td></td>
            <td> <br> Specifies the filesystem path. It is the absolute path for System access zone and it is relative if using non-system access zone. For example, if your access zone is 'Ansible' and it has a base path '/ifs/ansible' and the path specified is '/user1', then the effective path would be '/ifs/ansible/user1'. If your access zone is System, and you have 'directory1' in the access zone, the path provided should be '/ifs/directory1'.  <br> The directory on the path must exist - the NFS module will not create the directory.  <br> Ansible module will only support exports with a unique path.  <br> If there are multiple exports present with the same path, fetching details, creation, modification or deletion of such exports will fail. </td>
        </tr>
                    <tr>
            <td colspan=1 > access_zone</td>
            <td> str  </td>
            <td></td>
            <td> System </td>
            <td></td>
            <td> <br> Specifies the zone in which the export is valid.  <br> Access zone once set cannot be changed. </td>
        </tr>
                    <tr>
            <td colspan=1 > clients</td>
            <td> list   <br> elements: str </td>
            <td></td>
            <td></td>
            <td></td>
            <td> <br> Specifies the clients to the export. The type of access to clients in this list is determined by the 'read_only' parameter.  <br> This list can be changed anytime during the lifetime of the NFS export. </td>
        </tr>
                    <tr>
            <td colspan=1 > root_clients</td>
            <td> list   <br> elements: str </td>
            <td></td>
            <td></td>
            <td></td>
            <td> <br> Specifies the clients with root access to the export.  <br> This list can be changed anytime during the lifetime of the NFS export. </td>
        </tr>
                    <tr>
            <td colspan=1 > read_only_clients</td>
            <td> list   <br> elements: str </td>
            <td></td>
            <td></td>
            <td></td>
            <td> <br> Specifies the clients with read-only access to the export, even when the export is read/write.  <br> This list can be changed anytime during the lifetime of the NFS export. </td>
        </tr>
                    <tr>
            <td colspan=1 > read_write_clients</td>
            <td> list   <br> elements: str </td>
            <td></td>
            <td></td>
            <td></td>
            <td> <br> Specifies the clients with both read and write access to the export, even when the export is set to read-only.  <br> This list can be changed anytime during the lifetime of the NFS export. </td>
        </tr>
                    <tr>
            <td colspan=1 > read_only</td>
            <td> bool  </td>
            <td></td>
            <td></td>
            <td></td>
            <td> <br> Specifies whether the export is read-only or read-write. This parameter only has effect on the 'clients' list and not the other three types of clients.  <br> This setting can be modified any time. If it is not set at the time of creation, the export will be of type read/write. </td>
        </tr>
                    <tr>
            <td colspan=1 > sub_directories_mountable</td>
            <td> bool  </td>
            <td></td>
            <td></td>
            <td></td>
            <td> <br> True if all directories under the specified paths are mountable. If not set, sub-directories will not be mountable.  <br> This setting can be modified any time. </td>
        </tr>
                    <tr>
            <td colspan=1 > description</td>
            <td> str  </td>
            <td></td>
            <td></td>
            <td></td>
            <td> <br> Optional description field for the NFS export.  <br> Can be modified by passing a new value. </td>
        </tr>
                    <tr>
            <td colspan=1 > state</td>
            <td> str  </td>
            <td> True </td>
            <td></td>
            <td> <ul> <li>absent</li>  <li>present</li> </ul></td>
            <td> <br> Defines whether the NFS export should exist or not.  <br> present indicates that the NFS export should exist in system.  <br> absent indicates that the NFS export should not exist in system. </td>
        </tr>
                    <tr>
            <td colspan=1 > client_state</td>
            <td> str  </td>
            <td></td>
            <td></td>
            <td> <ul> <li>present-in-export</li>  <li>absent-in-export</li> </ul></td>
            <td> <br> Defines whether the clients can access the NFS export.  <br> present-in-export indicates that the clients can access the NFS export.  <br> absent-in-export indicates that the client cannot access the NFS export.  <br> Required when adding or removing access of clients from the export.  <br> While removing clients, only the specified clients will be removed from the export, others will remain as is. </td>
        </tr>
                    <tr>
            <td colspan=1 > onefs_host</td>
            <td> str  </td>
            <td> True </td>
            <td></td>
            <td></td>
            <td> <br> IP address or FQDN of the PowerScale cluster. </td>
        </tr>
                    <tr>
            <td colspan=1 > port_no</td>
            <td> str  </td>
            <td></td>
            <td> 8080 </td>
            <td></td>
            <td> <br> Port number of the PowerScale cluster.It defaults to 8080 if not specified. </td>
        </tr>
                    <tr>
            <td colspan=1 > verify_ssl</td>
            <td> bool  </td>
            <td> True </td>
            <td></td>
            <td> <ul> <li>True</li>  <li>False</li> </ul></td>
            <td> <br> boolean variable to specify whether to validate SSL certificate or not.  <br> True - indicates that the SSL certificate should be verified.  <br> False - indicates that the SSL certificate should not be verified. </td>
        </tr>
                    <tr>
            <td colspan=1 > api_user</td>
            <td> str  </td>
            <td> True </td>
            <td></td>
            <td></td>
            <td> <br> username of the PowerScale cluster. </td>
        </tr>
                    <tr>
            <td colspan=1 > api_password</td>
            <td> str  </td>
            <td> True </td>
            <td></td>
            <td></td>
            <td> <br> the password of the PowerScale cluster. </td>
        </tr>
                                            </table>


### Examples
```
  - name: Create NFS Export
    dellemc_powerscale_nfs:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      path: "<path>"
      access_zone: "{{access_zone}}"
      read_only_clients:
      - "{{client1}}"
      - "{{client2}}"
      read_only: True
      clients: ["{{client3}}"]
      client_state: 'present-in-export'
      state: 'present'

  - name: Get NFS Export
    dellemc_powerscale_nfs:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      path: "<path>"
      access_zone: "{{access_zone}}"
      state: 'present'

  - name: Add a root client
    dellemc_powerscale_nfs:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      path: "<path>"
      access_zone: "{{access_zone}}"
      root_clients:
      - "{{client4}}"
      client_state: 'present-in-export'
      state: 'present'

  - name: Set sub_directories_mountable flag to True
    dellemc_powerscale_nfs:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      path: "<path>"
      access_zone: "{{access_zone}}"
      sub_directories_mountable: True
      state: 'present'

  - name: Remove a root client
    dellemc_powerscale_nfs:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      path: "<path>"
      access_zone: "{{access_zone}}"
      root_clients:
      - "{{client4}}"
      client_state: 'absent-in-export'
      state: 'present'

  - name: Modify description
    dellemc_powerscale_nfs:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      path: "<path>"
      access_zone: "{{access_zone}}"
      description: "new description"
      state: 'present'

  - name: Set read_only flag to False
    dellemc_powerscale_nfs:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      path: "<path>"
      access_zone: "{{access_zone}}"
      read_only: False
      state: 'present'

  - name: Delete NFS Export
    dellemc_powerscale_nfs:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      path: "<path>"
      access_zone: "{{access_zone}}"
      state: 'absent'
```

### Return Values
                                                                                                                                                                                                                                                                                                                                            
<table>
    <tr>
        <th colspan=2>Key</th>
        <th>Type</th>
        <th>Returned</th>
        <th width="100%">Description</th>
    </tr>
                                                                                    <tr>
            <td colspan=2 > NFS_export_details </td>
            <td>  complex </td>
            <td> always </td>
            <td> The updated NFS Export details. </td>
        </tr>
                            <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > all_dirs </td>
                <td> bool </td>
                <td>success</td>
                <td> sub_directories_mountable flag value. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > clients </td>
                <td> list </td>
                <td>success</td>
                <td> The list of clients for the NFS Export. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > description </td>
                <td> str </td>
                <td>success</td>
                <td> Description for the export. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > id </td>
                <td> int </td>
                <td>success</td>
                <td> The ID of the NFS Export, generated by the array. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > paths </td>
                <td> list </td>
                <td>success</td>
                <td> The filesystem path. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > read_only </td>
                <td> bool </td>
                <td>success</td>
                <td> Specifies whether the export is read-only or read-write. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > read_only_clients </td>
                <td> list </td>
                <td>success</td>
                <td> The list of read only clients for the NFS Export. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > read_write_clients </td>
                <td> list </td>
                <td>success</td>
                <td> The list of read write clients for the NFS Export. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > root_clients </td>
                <td> list </td>
                <td>success</td>
                <td> The list of root clients for the NFS Export. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > zone </td>
                <td> str </td>
                <td>success</td>
                <td> Specifies the zone in which the export is valid. </td>
            </tr>
                                        <tr>
            <td colspan=2 > changed </td>
            <td>  bool </td>
            <td> always </td>
            <td> A boolean indicating if the task had to make changes. </td>
        </tr>
                    </table>

### Authors
* Manisha Agrawal(@agrawm3) <ansible.team@dell.com>

--------------------------------
# SyncIQ Policy Module

Manage SyncIQ policies on PowerScale

### Synopsis
 Managing SyncIQ policies on PowerScale includes create a SyncIQ policy, modify a SyncIQ policy, get details of a SyncIQ policy, creating jobs on SyncIQ policy

### Parameters
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
<table>
    <tr>
        <th colspan=2>Parameter</th>
        <th width="20%">Type</th>
        <th>Required</th>
        <th>Default</th>
        <th>Choices</th>
        <th width="80%">Description</th>
    </tr>
                                                            <tr>
            <td colspan=2 > policy_name</td>
            <td> str  </td>
            <td></td>
            <td></td>
            <td></td>
            <td> <br> The name of the policy.  <br> Required at the time of policy creation, for the rest of the operations either policy_name or policy_id is required. </td>
        </tr>
                    <tr>
            <td colspan=2 > policy_id</td>
            <td> str  </td>
            <td></td>
            <td></td>
            <td></td>
            <td> <br> The policy_id is auto generated at the time of creation.  <br> For get/modify operations either policy_name or policy_id is needed.  <br> Parameters policy_name and policy_id are mutually exclusive. </td>
        </tr>
                    <tr>
            <td colspan=2 > new_policy_name</td>
            <td> str  </td>
            <td></td>
            <td></td>
            <td></td>
            <td> <br> The new name of the policy while renaming an existing policy.  <br> policy_name or policy_id is required together with new_policy_name. </td>
        </tr>
                    <tr>
            <td colspan=2 > action</td>
            <td> str  </td>
            <td></td>
            <td></td>
            <td> <ul> <li>sync</li>  <li>copy</li> </ul></td>
            <td> <br> Indicates type of replication action to be performed on the source </td>
        </tr>
                    <tr>
            <td colspan=2 > state</td>
            <td> str  </td>
            <td> True </td>
            <td></td>
            <td> <ul> <li>absent</li>  <li>present</li> </ul></td>
            <td> <br> The state option is used to determine whether the policy exists or not. </td>
        </tr>
                    <tr>
            <td colspan=2 > description</td>
            <td> str  </td>
            <td></td>
            <td></td>
            <td></td>
            <td> <br> Description of the policy </td>
        </tr>
                    <tr>
            <td colspan=2 > enabled</td>
            <td> bool  </td>
            <td></td>
            <td></td>
            <td></td>
            <td> <br> Indicates whether policy is enabled or disabled </td>
        </tr>
                    <tr>
            <td colspan=2 > run_job</td>
            <td> str  </td>
            <td></td>
            <td></td>
            <td> <ul> <li>on-schedule</li>  <li>when-source-modified</li>  <li>when-snapshot-taken</li> </ul></td>
            <td> <br> Types of scheduling a job on the policy </td>
        </tr>
                    <tr>
            <td colspan=2 > job_delay</td>
            <td> int  </td>
            <td></td>
            <td></td>
            <td></td>
            <td> <br> If run_job is set to when-source-modified, job_delay is the duration to wait before triggering a job once there is modification on source. </td>
        </tr>
                    <tr>
            <td colspan=2 > job_delay_unit</td>
            <td> str  </td>
            <td></td>
            <td> seconds </td>
            <td> <ul> <li>seconds</li>  <li>minutes</li>  <li>hours</li>  <li>days</li> </ul></td>
            <td> <br> Unit for job_delay. </td>
        </tr>
                    <tr>
            <td colspan=2 > rpo_alert</td>
            <td> int  </td>
            <td></td>
            <td></td>
            <td></td>
            <td> <br> If run_job is set to 'on-schedule' is set to a time/date, an alert is created if the specified RPO for this policy is exceeded.  <br> The default value is 0, which will not generate RPO alerts. </td>
        </tr>
                    <tr>
            <td colspan=2 > rpo_alert_unit</td>
            <td> str  </td>
            <td></td>
            <td> minutes </td>
            <td> <ul> <li>minutes</li>  <li>hours</li>  <li>days</li>  <li>weeks</li>  <li>months</li>  <li>years</li> </ul></td>
            <td> <br> Unit for rpo_alert. </td>
        </tr>
                    <tr>
            <td colspan=2 > snapshot_sync_pattern</td>
            <td> str  </td>
            <td></td>
            <td></td>
            <td></td>
            <td> <br> The naming pattern that a snapshot must match to trigger a sync when the schedule is when-snapshot-taken. </td>
        </tr>
                    <tr>
            <td colspan=2 > skip_when_source_unmodified</td>
            <td> bool  </td>
            <td></td>
            <td></td>
            <td></td>
            <td> <br> If true and schedule is set , the policy will not run if no changes have been made to the contents of the source directory since the last job successfully completed.  <br> Option modifiable when run_job is "on_schedule". </td>
        </tr>
                    <tr>
            <td colspan=2 > schedule</td>
            <td> str  </td>
            <td></td>
            <td></td>
            <td></td>
            <td> <br> Schedule set when run_policy is 'on-schedule'  <br> It must be in isidate format.  <br> If the format is not proper an error will be thrown. </td>
        </tr>
                    <tr>
            <td colspan=2 > source_cluster</td>
            <td> dict  </td>
            <td></td>
            <td></td>
            <td></td>
            <td> <br> Defines the details of source_cluster. </td>
        </tr>
                            <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > source_root_path </td>
                <td> str  </td>
                <td></td>
                <td></td>
                <td></td>
                <td>  <br> The root directory on the source cluster where the files will be synced from.  <br> Source root path should begin with /ifs. For example, if we want to create a synciq policy for the directory 'source' in the base path /ifs, then the source_root_path will be '/ifs/source'.  </td>
            </tr>
                    <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > source_exclude_directories </td>
                <td> list   <br> elements: str </td>
                <td></td>
                <td></td>
                <td></td>
                <td>  <br> List of path to the directories that should be excluded while running a policy.  <br> For example, if we want to exclude directory 'exclude1' at location '/ifs/source', then the source_exclude_directories will be '/ifs/source/exclude1'.  </td>
            </tr>
                    <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > source_include_directories </td>
                <td> list   <br> elements: str </td>
                <td></td>
                <td></td>
                <td></td>
                <td>  <br> List of path to the directories that should be included while running a policy  <br> For example, if we want to include directory 'include1' at location '/ifs/source', then the source_exclude_directories will be '/ifs/source/include1'.  </td>
            </tr>
                    <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > source_network </td>
                <td> dict  </td>
                <td></td>
                <td></td>
                <td></td>
                <td>  <br> Run the policy only on nodes in the specified subnet and pool.  </td>
            </tr>
                            <tr>
            <td colspan=2 > target_cluster</td>
            <td> dict  </td>
            <td></td>
            <td></td>
            <td></td>
            <td> <br> Details of the target cluster. </td>
        </tr>
                            <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > target_host </td>
                <td> str  </td>
                <td></td>
                <td></td>
                <td></td>
                <td>  <br> Host IP or FQDN where we want to replicate the source.  </td>
            </tr>
                    <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > target_path </td>
                <td> str  </td>
                <td></td>
                <td></td>
                <td></td>
                <td>  <br> The directory location to have the replicated source data at.  </td>
            </tr>
                    <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > target_certificate_id </td>
                <td> str  </td>
                <td></td>
                <td></td>
                <td></td>
                <td>  <br> The ID of the target cluster certificate being used for encryption  <br> This parameter is not supported by isi_sdk_8_1_1  </td>
            </tr>
                    <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > target_certificate_name </td>
                <td> str  </td>
                <td></td>
                <td></td>
                <td></td>
                <td>  <br> The name of the target cluster certificate being used for encryption  <br> Parameters target_certficate_name and target_certificate_id are mutually exclusive  <br> This parameter is not supported by isi_sdk_8_1_1  </td>
            </tr>
                            <tr>
            <td colspan=2 > target_snapshot</td>
            <td> dict  </td>
            <td></td>
            <td></td>
            <td></td>
            <td> <br> Details of snapshots to be created at the target. </td>
        </tr>
                            <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > target_snapshot_archive </td>
                <td> bool  </td>
                <td></td>
                <td></td>
                <td></td>
                <td>  <br> Indicates whether to take snapshot of the target.  </td>
            </tr>
                    <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > target_snapshot_expiration </td>
                <td> int  </td>
                <td></td>
                <td></td>
                <td></td>
                <td>  <br> Expiration time of snapshot.  <br> Value 0 means no expiration.  </td>
            </tr>
                    <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > exp_time_unit </td>
                <td> str  </td>
                <td></td>
                <td> years </td>
                <td> <ul> <li>years</li>  <li>months</li>  <li>weeks</li>  <li>days</li> </ul></td>
                <td>  <br> Unit of target_snapshot expiration time.  </td>
            </tr>
                            <tr>
            <td colspan=2 > job_params</td>
            <td> dict  </td>
            <td></td>
            <td></td>
            <td></td>
            <td> <br> Specifies the parameters to create a job on SyncIQ policy </td>
        </tr>
                            <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > action </td>
                <td> str  </td>
                <td> True </td>
                <td></td>
                <td> <ul> <li>run</li>  <li>resync_prep</li>  <li>allow_write</li>  <li>allow_write_revert</li> </ul></td>
                <td>  <br> The action to be taken by this job.  </td>
            </tr>
                    <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > wait_for_completion </td>
                <td> bool  </td>
                <td></td>
                <td> False </td>
                <td></td>
                <td>  <br> Specifies if the job should run synchronously or asynchronously. By default the job is created to run asynchronously.  </td>
            </tr>
                    <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > source_snapshot </td>
                <td> str  </td>
                <td></td>
                <td></td>
                <td></td>
                <td>  <br> An optional snapshot to copy/sync from.  </td>
            </tr>
                    <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > workers_per_node </td>
                <td> int  </td>
                <td></td>
                <td></td>
                <td></td>
                <td>  <br> Specifies the desired workers per node. This parameter is valid for allow_write, and allow_write_revert operation. This is an optional parameter and it defaults to 3.  </td>
            </tr>
                            <tr>
            <td colspan=2 > onefs_host</td>
            <td> str  </td>
            <td> True </td>
            <td></td>
            <td></td>
            <td> <br> IP address or FQDN of the PowerScale cluster. </td>
        </tr>
                    <tr>
            <td colspan=2 > port_no</td>
            <td> str  </td>
            <td></td>
            <td> 8080 </td>
            <td></td>
            <td> <br> Port number of the PowerScale cluster.It defaults to 8080 if not specified. </td>
        </tr>
                    <tr>
            <td colspan=2 > verify_ssl</td>
            <td> bool  </td>
            <td> True </td>
            <td></td>
            <td> <ul> <li>True</li>  <li>False</li> </ul></td>
            <td> <br> boolean variable to specify whether to validate SSL certificate or not.  <br> True - indicates that the SSL certificate should be verified.  <br> False - indicates that the SSL certificate should not be verified. </td>
        </tr>
                    <tr>
            <td colspan=2 > api_user</td>
            <td> str  </td>
            <td> True </td>
            <td></td>
            <td></td>
            <td> <br> username of the PowerScale cluster. </td>
        </tr>
                    <tr>
            <td colspan=2 > api_password</td>
            <td> str  </td>
            <td> True </td>
            <td></td>
            <td></td>
            <td> <br> the password of the PowerScale cluster. </td>
        </tr>
                                                    </table>

### Notes
* There is a delay to view the jobs running on the policy.

### Examples
```
  - name: Create SyncIQ policy
    dellemc_powerscale_synciqpolicy:
      onefs_host: "{{onefs_host}}"
      verify_ssl: "{{verify_ssl}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      action: "copy"
      description: "Creating a policy"
      enabled: True
      policy_name: "New_policy"
      run_job: "on-schedule"
      schedule: "every 1 days at 12:00 PM"
      skip_when_source_unmodified: True
      rpo_alert: 100
      source_cluster:
        source_root_path: "<path_to_source>"
        source_exclude_directories: "<path_to_exclude>"
        source_include_directories: "<path_to_include>"
        source_network:
            pool: "pool0"
            subnet: "subnet0"
      target_cluster:
        target_host: "198.10.xxx.xxx"
        target_path: "<path_to_target>"
        target_certificate_id: "7sdgvejkiau7629903048hdjdkljsbwgsuasj7169823kkckll"
      target_snapshot:
        target_snapshot_archive: True
        target_snapshot_expiration: 90
        exp_time_unit: "day"
      state: "present"

  - name: Modify SyncIQ policy
    dellemc_powerscale_synciqpolicy:
      onefs_host: "{{onefs_host}}"
      verify_ssl: "{{verify_ssl}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      policy_name: "New_policy"
      action: "sync"
      description: "Creating a policy"
      enabled: False
      run_job: "when-snapshot-taken"
      snapshot_sync_patten: "^snapshot\\-$latest"
      source_cluster:
        source_root_path: "<path_to_source>"
        source_exclude_directories: "<path_to_exclude>"
        source_include_directories: "<path_to_include>"
        source_network:
            pool: "pool1"
            subnet: "subnet1"
      target_cluster:
        target_host: "198.10.xxx.xxx"
        target_path: "<path_to_target>"
        target_certificate_id: "7sdgvejkiau7629903048hdjdkljsbwgsuasj716iuhywthsjk"
      target_snapshot:
        target_snapshot_archive: False
      state: "present"

  - name: Rename a SyncIQ policy
    dellemc_powerscale_synciqpolicy:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      policy_id: "d63b079d34adf2d2ec3ce92f15bfc730"
      new_policy_name: "Policy_Rename"
      state: "present"

  - name: Get SyncIQ policy details
    dellemc_powerscale_synciqpolicy:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      policy_name: "Policy_rename"
      state: "present"

  - name: Create a job on SyncIQ policy
    dellemc_powerscale_synciqpolicy:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      policy_name: "Test_SSL"
      job_params:
        action: "run"
        source_snapshot: "TestSIQ-snapshot"
        wait_for_completion: False
      state: "present"

  - name: Create a resync_prep job on SyncIQ policy
    dellemc_powerscale_synciqpolicy:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      policy_name: "Test_SSL"
      job_params:
        action: "resync_prep"
        source_snapshot: "TestSIQ-snapshot"
        wait_for_completion: False
      state: "present"

  - name: Allow writes on target of SyncIQ policy
    dellemc_powerscale_synciqpolicy:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      policy_name: "Test_SSL"
      job_params:
        action: "allow_write"
        source_snapshot: "TestSIQ-snapshot"
        workers_per_node: 3
        wait_for_completion: False
      state: "present"

  - name: Disallow writes on target of SyncIQ policy
    dellemc_powerscale_synciqpolicy:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      policy_name: "Test_SSL"
      job_params:
        action: "allow_write_revert"
        source_snapshot: "TestSIQ-snapshot"
        workers_per_node: 3
        wait_for_completion: False
      state: "present"

  - name: Delete SyncIQ policy by policy name
    dellemc_powerscale_synciqpolicy:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      policy_name: "Policy_rename"
      state: "absent"

  - name: Delete SyncIQ policy by policy ID
    dellemc_powerscale_synciqpolicy:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      policy_id: "d63b079d34adf2d2ec3ce92f15bfc730"
      state: "absent"
```

### Return Values
                                                                                                                                                                                                                                                                                                                                                                                                                                            
<table>
    <tr>
        <th colspan=2>Key</th>
        <th>Type</th>
        <th>Returned</th>
        <th width="100%">Description</th>
    </tr>
                                                                                            <tr>
            <td colspan=2 > changed </td>
            <td>  bool </td>
            <td> always </td>
            <td> Whether or not the resource has changed </td>
        </tr>
                    <tr>
            <td colspan=2 > synciq_policy_details </td>
            <td>  complex </td>
            <td> When SyncIQ policy exists </td>
            <td> Details of the SyncIQ policy </td>
        </tr>
                            <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > action </td>
                <td> str </td>
                <td>success</td>
                <td> Type of action for the policy </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > enabled </td>
                <td> bool </td>
                <td>success</td>
                <td> Indicates whether policy is enabled </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > id </td>
                <td> str </td>
                <td>success</td>
                <td> ID of the policy. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > jobs </td>
                <td> list </td>
                <td>success</td>
                <td> List of jobs running on the policy </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > name </td>
                <td> str </td>
                <td>success</td>
                <td> The name of the policy. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > schedule </td>
                <td> str </td>
                <td>success</td>
                <td> Type of schedule chosen to run a policy </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > source_root_path </td>
                <td> str </td>
                <td>success</td>
                <td> The path to the source directory to be replicated </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > target_host </td>
                <td> str </td>
                <td>success</td>
                <td> The IP/FQDN of the host where source is replicated </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > target_path </td>
                <td> str </td>
                <td>success</td>
                <td> The target directory where source is replicated </td>
            </tr>
                                        <tr>
            <td colspan=2 > target_synciq_policy_details </td>
            <td>  complex </td>
            <td> When failover/failback is performed on target cluster </td>
            <td> Details of the target SyncIQ policy </td>
        </tr>
                            <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > failover_failback_state </td>
                <td> str </td>
                <td>success</td>
                <td> The state of the policy with respect to sync failover/failback. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > id </td>
                <td> str </td>
                <td>success</td>
                <td> ID of the policy. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > name </td>
                <td> str </td>
                <td>success</td>
                <td> The name of the policy. </td>
            </tr>
                                        </table>

### Authors
* Spandita Panigrahi (@panigs7) <ansible.team@dell.com>

--------------------------------
# Group Module

Manage Groups on the PowerScale Storage System

### Synopsis
 Managing Groups on the PowerScale Storage System includes create group, delete group,  get group, add users and remove users.

### Parameters
                                                                                                                                                                                                                                                                                            
<table>
    <tr>
        <th colspan=1>Parameter</th>
        <th width="20%">Type</th>
        <th>Required</th>
        <th>Default</th>
        <th>Choices</th>
        <th width="80%">Description</th>
    </tr>
                                                            <tr>
            <td colspan=1 > group_name</td>
            <td> str  </td>
            <td></td>
            <td></td>
            <td></td>
            <td> <br> The name of the group.  <br> Required at the time of group creation, for the rest of the operations either group_name or group_id is required. </td>
        </tr>
                    <tr>
            <td colspan=1 > group_id</td>
            <td> str  </td>
            <td></td>
            <td></td>
            <td></td>
            <td> <br> The group_id is auto generated at the time of creation.  <br> For all other operations either group_name or group_id is needed. </td>
        </tr>
                    <tr>
            <td colspan=1 > access_zone</td>
            <td> str  </td>
            <td></td>
            <td> system </td>
            <td></td>
            <td> <br> This option mentions the zone in which a group is created.  <br> For creation, access_zone acts as an attribute for the group.  <br> For all other operations access_zone acts as a filter. </td>
        </tr>
                    <tr>
            <td colspan=1 > provider_type</td>
            <td> str  </td>
            <td></td>
            <td> local </td>
            <td> <ul> <li>local</li>  <li>file</li>  <li>ldap</li>  <li>ads</li> </ul></td>
            <td> <br> This option defines the type which will be used to authenticate the group members.  <br> Creation, Deletion and Modification is allowed only for local group.  <br> Details of groups of all provider types can be fetched.  <br> If the provider_type is 'ads' then the domain name of the Active Directory Server has to be mentioned in the group_name. The format for the group_name should be 'DOMAIN_NAME\group_name' or "DOMAIN_NAME\\group_name".  <br> This option acts as a filter for all operations except creation. </td>
        </tr>
                    <tr>
            <td colspan=1 > state</td>
            <td> str  </td>
            <td> True </td>
            <td></td>
            <td> <ul> <li>absent</li>  <li>present</li> </ul></td>
            <td> <br> The state option is used to determine whether the group will exist or not. </td>
        </tr>
                    <tr>
            <td colspan=1 > users</td>
            <td> list   <br> elements: dict </td>
            <td></td>
            <td></td>
            <td></td>
            <td> <br> Either user_name or user_id is needed to add or remove the user from the group.  <br> users can be part of multiple groups. </td>
        </tr>
                    <tr>
            <td colspan=1 > user_state</td>
            <td> str  </td>
            <td></td>
            <td></td>
            <td> <ul> <li>present-in-group</li>  <li>absent-in-group</li> </ul></td>
            <td> <br> The user_state option is used to  determine whether the users will exist for a particular group or not.  <br> It is required when users are added or removed from a group. </td>
        </tr>
                    <tr>
            <td colspan=1 > onefs_host</td>
            <td> str  </td>
            <td> True </td>
            <td></td>
            <td></td>
            <td> <br> IP address or FQDN of the PowerScale cluster. </td>
        </tr>
                    <tr>
            <td colspan=1 > port_no</td>
            <td> str  </td>
            <td></td>
            <td> 8080 </td>
            <td></td>
            <td> <br> Port number of the PowerScale cluster.It defaults to 8080 if not specified. </td>
        </tr>
                    <tr>
            <td colspan=1 > verify_ssl</td>
            <td> bool  </td>
            <td> True </td>
            <td></td>
            <td> <ul> <li>True</li>  <li>False</li> </ul></td>
            <td> <br> boolean variable to specify whether to validate SSL certificate or not.  <br> True - indicates that the SSL certificate should be verified.  <br> False - indicates that the SSL certificate should not be verified. </td>
        </tr>
                    <tr>
            <td colspan=1 > api_user</td>
            <td> str  </td>
            <td> True </td>
            <td></td>
            <td></td>
            <td> <br> username of the PowerScale cluster. </td>
        </tr>
                    <tr>
            <td colspan=1 > api_password</td>
            <td> str  </td>
            <td> True </td>
            <td></td>
            <td></td>
            <td> <br> the password of the PowerScale cluster. </td>
        </tr>
                                            </table>


### Examples
```
  - name: Create a Group
    dellemc_powerscale_group:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      access_zone: "{{access_zone}}"
      provider_type: "{{provider_type}}"
      group_name: "{{group_name}}"
      state: "present"

  - name: Create Group with Users
    dellemc_powerscale_group:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      provider_type: "{{provider_type}}"
      access_zone: "{{access_zone}}"
      group_name: "{{group_name}}"
      users:
        - user_name: "{{user_name}}"
        - user_id: "{{user_id}}"
        - user_name: "{{user_name_2}}"
      user_state: "present-in-group"
      state: "present"

  - name: Get Details of the Group using Group Id
    dellemc_powerscale_group:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      provider_type: "{{provider_type}}"
      access_zone: "{{access_zone}}"
      group_id: "{{group_id}}"
      state: "present"

  - name: Delete the Group using Group Name
    dellemc_powerscale_group:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      provider_type: "{{provider_type}}"
      access_zone: "{{access_zone}}"
      group_name: "{{group_name}}"
      state: "absent"

  - name: Add Users to a Group
    dellemc_powerscale_group:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      provider_type: "{{provider_type}}"
      access_zone: "{{access_zone}}"
      group_id: "{{group_id}}"
      users:
        - user_name: "{{user_name}}"
        - user_id: "{{user_id}}"
        - user_name: "{{user_name_2}}"
      user_state: "present-in-group"
      state: "present"

  - name: Remove Users from a Group
    dellemc_powerscale_group:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      provider_type: "{{provider_type}}"
      access_zone: "{{access_zone}}"
      group_id: "{{group_id}}"
      users:
        - user_name: "{{user_name_1}}"
        - user_id: "{{user_id}}"
        - user_name: "{{user_name_2}}"
      user_state: "absent-in-group"
      state: "present"
```

### Return Values
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
<table>
    <tr>
        <th colspan=5>Key</th>
        <th>Type</th>
        <th>Returned</th>
        <th width="100%">Description</th>
    </tr>
                                                                                    <tr>
            <td colspan=5 > changed </td>
            <td>  bool </td>
            <td> always </td>
            <td> Whether or not the resource has changed </td>
        </tr>
                    <tr>
            <td colspan=5 > group_details </td>
            <td>  complex </td>
            <td> When group exists </td>
            <td> Details of the group </td>
        </tr>
                            <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > gid </td>
                <td> complex </td>
                <td>success</td>
                <td> The details of the primary group for the user. </td>
            </tr>
                                         <tr>
                    <td class="elbow-placeholder">&nbsp;</td>
                    <td class="elbow-placeholder">&nbsp;</td>
                    <td colspan=3 > id </td>
                    <td> str </td>
                    <td>success</td>
                    <td> The id of the group. </td>
                </tr>
                                             <tr>
                    <td class="elbow-placeholder">&nbsp;</td>
                    <td class="elbow-placeholder">&nbsp;</td>
                    <td colspan=3 > name </td>
                    <td> str </td>
                    <td>success</td>
                    <td> The name of the group. </td>
                </tr>
                                             <tr>
                    <td class="elbow-placeholder">&nbsp;</td>
                    <td class="elbow-placeholder">&nbsp;</td>
                    <td colspan=3 > type_of_resource </td>
                    <td> str </td>
                    <td>success</td>
                    <td> The resource's type is mentioned. </td>
                </tr>
                                                            <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > members </td>
                <td> complex </td>
                <td>success</td>
                <td> The list of sid's the members of group. </td>
            </tr>
                                         <tr>
                    <td class="elbow-placeholder">&nbsp;</td>
                    <td class="elbow-placeholder">&nbsp;</td>
                    <td colspan=3 > sid </td>
                    <td> complex </td>
                    <td>success</td>
                    <td> The details of the associated resource. </td>
                </tr>
                                                    <tr>
                        <td class="elbow-placeholder">&nbsp;</td>
                        <td class="elbow-placeholder">&nbsp;</td>
                        <td class="elbow-placeholder">&nbsp;</td>
                        <td colspan=2 > id </td>
                        <td> str </td>
                        <td>success</td>
                        <td> The unique security identifier of the resource. </td>
                    </tr>
                                    <tr>
                        <td class="elbow-placeholder">&nbsp;</td>
                        <td class="elbow-placeholder">&nbsp;</td>
                        <td class="elbow-placeholder">&nbsp;</td>
                        <td colspan=2 > name </td>
                        <td> str </td>
                        <td>success</td>
                        <td> The name of the resource. </td>
                    </tr>
                                    <tr>
                        <td class="elbow-placeholder">&nbsp;</td>
                        <td class="elbow-placeholder">&nbsp;</td>
                        <td class="elbow-placeholder">&nbsp;</td>
                        <td colspan=2 > type_of_resource </td>
                        <td> str </td>
                        <td>success</td>
                        <td> The resource's type is mentioned. </td>
                    </tr>
                                                                            <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > name </td>
                <td> str </td>
                <td>success</td>
                <td> The name of the group. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=4 > provider </td>
                <td> str </td>
                <td>success</td>
                <td> The provider contains the provider type and access zone. </td>
            </tr>
                                        </table>

### Authors
* P Srinivas Rao (@srinivas-rao5) <ansible.team@dell.com>

--------------------------------
# File System Module

Manage Filesystems on PowerScale

### Synopsis
 Managing Filesystems on PowerScale Storage System includes Create a new Filesystem, Delete a Filesystem, Get details of a filesystem, Modify a Filesystem (Quota, ACLs).

### Parameters
                                                                                                                                                                                                                                                                                                                                    
<table>
    <tr>
        <th colspan=1>Parameter</th>
        <th width="20%">Type</th>
        <th>Required</th>
        <th>Default</th>
        <th>Choices</th>
        <th width="80%">Description</th>
    </tr>
                                                            <tr>
            <td colspan=1 > path</td>
            <td> str  </td>
            <td> True </td>
            <td></td>
            <td></td>
            <td> <br> This is the directory path. It is the absolute path for System access zone and is relative if using a non-System access zone. For example, if your access zone is 'Ansible' and it has a base path '/ifs/ansible' and the path specified is '/user1', then the effective path would be '/ifs/ansible/user1'. If your access zone is System, and you have 'directory1' in the access zone, the path provided should be '/ifs/directory1'. </td>
        </tr>
                    <tr>
            <td colspan=1 > access_zone</td>
            <td> str  </td>
            <td></td>
            <td> System </td>
            <td></td>
            <td> <br> The access zone. If no Access Zone is specified, the 'System' access zone would be taken by default. </td>
        </tr>
                    <tr>
            <td colspan=1 > owner</td>
            <td> dict  </td>
            <td></td>
            <td></td>
            <td></td>
            <td> <br> The owner of the Filesystem.  <br> This parameter is required while creating a Filesystem.  <br> The following sub-options are supported for Owner. - name(str), - provider_type(str).  <br> If you specify owner, then the corresponding name is mandatory.  <br> The provider_type is optional and it defaults to 'local'.  <br> The supported values for provider_type are 'local', 'file', 'ldap' and 'ads'. </td>
        </tr>
                    <tr>
            <td colspan=1 > group</td>
            <td> dict  </td>
            <td></td>
            <td></td>
            <td></td>
            <td> <br> The group of the Filesystem.  <br> The following sub-options are supported for Group. - name(str), - provider_type(str).  <br> If you specify  a group, then the corresponding name is mandatory.  <br> The provider_type is optional, it defaults to 'local'.  <br> The supported values for provider_type are 'local', 'file', 'ldap' and 'ads'. </td>
        </tr>
                    <tr>
            <td colspan=1 > access_control</td>
            <td> str  </td>
            <td></td>
            <td></td>
            <td></td>
            <td> <br> The ACL value for the directory.  <br> At the time of creation, users can either provide input such as 'private_read' , 'private' , 'public_read', 'public_read_write', 'public' or in POSIX format (eg 0700).  <br> Modification of ACL is only supported from POSIX to POSIX mode. </td>
        </tr>
                    <tr>
            <td colspan=1 > recursive</td>
            <td> bool  </td>
            <td></td>
            <td> True </td>
            <td></td>
            <td> <br> Creates intermediate folders recursively when set to true. </td>
        </tr>
                    <tr>
            <td colspan=1 > quota</td>
            <td> dict  </td>
            <td></td>
            <td></td>
            <td></td>
            <td> <br> The Smart Quota for the filesystem. Only directory Quotas are supported.  <br> The following sub-options are supported for Quota. - include_snap_data(boolean), - include_data_protection_overhead(boolean), - thresholds_on(app_logical_size, fs_logical_size, physical_size) - advisory_limit_size(int), - soft_limit_size(int), - hard_limit_size(int), - cap_unit (MB, GB or TB), - quota_state (present or absent).  <br> The default grace period is 7 days. Modification of grace period is not supported.  <br> The default capacity unit is GB.  <br> The parameter include_data_protection_overhead is supported for SDK 8.1.1  <br> For SDK 9.0.0 the parameter include_data_protection_overhead is deprecated and thresholds_on is used. </td>
        </tr>
                    <tr>
            <td colspan=1 > state</td>
            <td> str  </td>
            <td> True </td>
            <td></td>
            <td> <ul> <li>absent</li>  <li>present</li> </ul></td>
            <td> <br> Defines whether the Filesystem should exist or not.  <br> A filesystem with NFS exports or SMB shares cannot be deleted.  <br> Any Quotas on the Filesystem need to be removed before deleting the filesystem. </td>
        </tr>
                    <tr>
            <td colspan=1 > list_snapshots</td>
            <td> bool  </td>
            <td></td>
            <td> False </td>
            <td></td>
            <td> <br> If set to true, the filesystem's snapshots are returned. </td>
        </tr>
                    <tr>
            <td colspan=1 > onefs_host</td>
            <td> str  </td>
            <td> True </td>
            <td></td>
            <td></td>
            <td> <br> IP address or FQDN of the PowerScale cluster. </td>
        </tr>
                    <tr>
            <td colspan=1 > port_no</td>
            <td> str  </td>
            <td></td>
            <td> 8080 </td>
            <td></td>
            <td> <br> Port number of the PowerScale cluster.It defaults to 8080 if not specified. </td>
        </tr>
                    <tr>
            <td colspan=1 > verify_ssl</td>
            <td> bool  </td>
            <td> True </td>
            <td></td>
            <td> <ul> <li>True</li>  <li>False</li> </ul></td>
            <td> <br> boolean variable to specify whether to validate SSL certificate or not.  <br> True - indicates that the SSL certificate should be verified.  <br> False - indicates that the SSL certificate should not be verified. </td>
        </tr>
                    <tr>
            <td colspan=1 > api_user</td>
            <td> str  </td>
            <td> True </td>
            <td></td>
            <td></td>
            <td> <br> username of the PowerScale cluster. </td>
        </tr>
                    <tr>
            <td colspan=1 > api_password</td>
            <td> str  </td>
            <td> True </td>
            <td></td>
            <td></td>
            <td> <br> the password of the PowerScale cluster. </td>
        </tr>
                                            </table>


### Examples
```
  - name: Create Filesystem with Quota in given access zone
    dellemc_powerscale_filesystem:
     onefs_host: "{{powerscalehost}}"
     port: "{{powerscaleport}}"
     verify_ssl: "{{verify_ssl}}"
     username: "{{user}}"
     password: "{{password}}"
     path: "<path>"
     access_zone: "{{access_zone}}"
     owner:
       name: 'ansible_user'
       provider_type: 'ldap'
     group:
       name: 'ansible_group'
       provider_type: 'ldap'
     access_control: "{{access_control}}"
     quota:
       include_snap_data: False
       include_data_protection_overhead: False
       advisory_limit_size: 2
       soft_limit_size: 5
       hard_limit_size: 10
       cap_unit: "GB"
       quota_state: "present"
     recursive: "{{recursive}}"
     state: "{{state_present}}"

  - name: Create Filesystem in default (system) access zone, without Quota
    dellemc_powerscale_filesystem:
      onefs_host: "{{powerscalehost}}"
      port: "{{powerscaleport}}"
      verify_ssl: "{{verify_ssl}}"
      username: "{{user}}"
      password: "{{password}}"
      path: "<path>"
      owner:
       name: 'ansible_user'
       provider_type: 'ldap'
      state: "{{state_present}}"

  - name: Get filesystem details
    dellemc_powerscale_filesystem:
     onefs_host: "{{powerscalehost}}"
     port: "{{powerscaleport}}"
     verify_ssl: "{{verify_ssl}}"
     username: "{{user}}"
     password: "{{password}}"
     access_zone: "{{access_zone}}"
     path: "<path>"
     state: "{{state_present}}"

  - name: Get filesystem details with snapshots
    dellemc_powerscale_filesystem:
     onefs_host: "{{powerscalehost}}"
     port: "{{powerscaleport}}"
     verify_ssl: "{{verify_ssl}}"
     username: "{{user}}"
     password: "{{password}}"
     access_zone: "{{access_zone}}"
     path: "<path>"
     list_snapshots: "{{list_snapshots_true}}"
     state: "{{state_present}}"

  - name: Modify Filesystem Hard Quota
    dellemc_powerscale_filesystem:
      onefs_host: "{{powerscalehost}}"
      port: "{{powerscaleport}}"
      verify_ssl: "{{verify_ssl}}"
      username: "{{user}}"
      password: "{{password}}"
      path: "<path>"
      access_zone: "{{access_zone}}"
      quota:
        hard_limit_size: 15
        cap_unit: "GB"
        quota_state: "present"
      state: "{{state_present}}"

  - name: Modify Filesystem Owner, Group and ACL
    dellemc_powerscale_filesystem:
      onefs_host: "{{powerscalehost}}"
      port: "{{powerscaleport}}"
      verify_ssl: "{{verify_ssl}}"
      username: "{{user}}"
      password: "{{password}}"
      path: "<path>"
      access_zone: "{{access_zone}}"
      owner:
       name: 'ansible_user'
       provider_type: 'ldap'
      group:
       name: 'ansible_group'
       provider_type: 'ldap'
      access_control: "{{new_access_control}}"
      state: "{{state_present}}"

  - name: Remove Quota from FS
    dellemc_powerscale_filesystem:
     onefs_host: "{{onefs_host}}"
     verify_ssl: "{{verify_ssl}}"
     api_user: "{{api_user}}"
     api_password: "{{api_password}}"
     path: "<path>"
     access_zone: "{{access_zone}}"
     quota:
       quota_state: "absent"
     state: "{{state_present}}"

  - name: Delete filesystem
    dellemc_powerscale_filesystem:
     onefs_host: "{{powerscalehost}}"
     port: "{{powerscaleport}}"
     verify_ssl: "{{verify_ssl}}"
     username: "{{user}}"
     password: "{{password}}"
     access_zone: "{{access_zone}}"
     path: "<path>"
     state: "{{state_absent}}"
```

### Return Values
                                                                                                                                                                                                                                                                                                                                                                                                                                                    
<table>
    <tr>
        <th colspan=2>Key</th>
        <th>Type</th>
        <th>Returned</th>
        <th width="100%">Description</th>
    </tr>
                                                                                    <tr>
            <td colspan=2 > changed </td>
            <td>  bool </td>
            <td> always </td>
            <td> Whether or not the resource has changed </td>
        </tr>
                    <tr>
            <td colspan=2 > filesystem_details </td>
            <td>  complex </td>
            <td> When Filesystem exists. </td>
            <td> The filesystem details. </td>
        </tr>
                            <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > attrs </td>
                <td> dict </td>
                <td>success</td>
                <td> The attributes of the filesystem. </td>
            </tr>
                                        <tr>
            <td colspan=2 > filesystem_snapshots </td>
            <td>  complex </td>
            <td> When list_snapshots is True. </td>
            <td> The filesystem snapshot details. </td>
        </tr>
                            <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > created </td>
                <td> int </td>
                <td>success</td>
                <td> The creation timestamp. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > expires </td>
                <td> int </td>
                <td>success</td>
                <td> The expiration timestamp. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > id </td>
                <td> int </td>
                <td>success</td>
                <td> The id of the snapshot. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > name </td>
                <td> str </td>
                <td>success</td>
                <td> The name of the snapshot. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > path </td>
                <td> str </td>
                <td>success</td>
                <td> The path of the snapshot. </td>
            </tr>
                                        <tr>
            <td colspan=2 > quota_details </td>
            <td>  complex </td>
            <td> When Quota exists. </td>
            <td> The quota details. </td>
        </tr>
                            <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > enforced </td>
                <td> bool </td>
                <td>success</td>
                <td> Whether the Quota is enforced. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > id </td>
                <td> str </td>
                <td>success</td>
                <td> The ID of the Quota. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > type </td>
                <td> str </td>
                <td>success</td>
                <td> The type of Quota. </td>
            </tr>
                                <tr>
                <td class="elbow-placeholder">&nbsp;</td>
                <td colspan=1 > usage </td>
                <td> dict </td>
                <td>success</td>
                <td> The Quota usage. </td>
            </tr>
                                        </table>

### Authors
* Prashant Rakheja (@prashant-dell) <ansible.team@dell.com>

--------------------------------
