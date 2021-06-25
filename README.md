# Ansible Modules for Dell EMC PowerScale
The Ansible Modules for Dell EMC PowerScale allow Data Center and IT administrators to use RedHat Ansible to automate and orchestrate the configuration and management of Dell EMC PowerScale arrays.

The capabilities of the Ansible modules are managing users, groups, node, active directory, ldap, access zones, file system, nfs exports, smb shares, snapshots, snapshot schedules and smart quotas, and to gather facts from the array. The tasks can be executed by running simple playbooks written in yaml syntax.

## Support
  * Ansible modules for PowerScale are supported by Dell EMC and are provided under the terms of the license attached to the source code.
  * For any setup, configuration issues, questions or feedback, join the [Dell EMC Automation community](https://www.dell.com/community/Automation/bd-p/Automation).
  * For any Dell EMC storage issues, please contact Dell support at: https://www.dell.com/support.
  * Dell EMC does not provide support for any source code modifications.

## Supported Platforms
  * Dell EMC PowerScale Arrays version 8.0 and above.

## Prerequisites
  * Ansible 2.9, 2.10
  * Python 3.5, 3.6, 3.7
  * Red Hat Enterprise Linux 7.6, 7.7, 7.8, 8.2
  * Python SDK for PowerScale (version 8.1.1 and 9.0.0)

## Idempotency
The modules are written in such a way that all requests are idempotent and hence fault-tolerant. It essentially means that the result of a successfully performed request is independent of the number of times it is executed.

## List of Ansible Modules for Dell EMC PowerScale
  * File System Module
  * Access Zone Module
  * Users Module
  * Groups Module
  * Snapshot Module
  * Snapshot Schedule Module
  * NFS Module
  * SMB Module
  * Smart Quota Module
  * Gather Facts Module
  * Active Directory Module
  * LDAP Module
  * Node Module

## Installation of SDK
Based on which PowerScale version is being used, install sdk as  follows:

* For PowerScale version < 9.1.0, install python [sdk](https://pypi.org/project/isi-sdk-8-1-1/) named 'isi-sdk-8-1-1' as below: 
  
        pip install isi_sdk_8_1_1
  
* For PowerScale version 9.1.0, install python [sdk](https://pypi.org/project/isi-sdk-9-0-0/) named 'isi-sdk-9-0-0' as below:
        
        pip install isi_sdk_9_0_0


## Installing Collections

  * Download the tar build and run the following command to install the collection anywhere in your system:
        
        ansible-galaxy collection install dellemc-powerscale-1.2.0.tar.gz -p <install_path>
  
  * Set the environment variable:
        
        export ANSIBLE_COLLECTIONS_PATHS=$ANSIBLE_COLLECTIONS_PATHS:<install_path>

## Using Collections

  * In order to use any Ansible module, ensure that the importation of the proper FQCN (Fully Qualified Collection Name) is embedded in the playbook. For example,
 <br>collections:
 <br>&nbsp;&nbsp;&nbsp; - dellemc.powerscale
  * To generate Ansible documentation for a specific module, embed the FQCN before the module name. For example,
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; *ansible-doc dellemc.powerscale.dellemc_powerscale_gatherfacts*

## Running Ansible Modules

The Ansible server must be configured with Python library for OneFS to run the Ansible playbooks. The [Documents](https://github.com/dell/ansible-powerscale/tree/1.2.0/docs) provide information on different Ansible modules along with their functions and syntax. The parameters table in the Product Guide provides information on various parameters which need to be configured before running the modules.

## SSL Certificate Validation

* Export the SSL certificate using KeyStore Explorer tool or from the browser in .crt format.
* Append the SSL certificate to the Certifi package file cacert.pem.
    * For Python 3.5 : cat <> >> /usr/local/lib/python3.5/dist-packages/certifi/cacert.pem
    * For Python 2.7 : cat <> >> /usr/local/lib/python2.7/dist-packages/certifi/cacert.pem

## Results
Each module returns the updated state and details of the entity. 
For example, if you are using the group module, all calls will return the updated details of the group.
Sample result is shown in each module's documentation.
