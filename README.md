# Ansible Modules for Dell EMC PowerScale
The Ansible Modules for Dell EMC PowerScale allow Data Center and IT administrators to use RedHat Ansible to automate and orchestrate the configuration and management of Dell EMC PowerScale arrays.

The capabilities of the Ansible modules are managing users, groups, node, active directory, ldap, access zones, file system, nfs exports, smb shares, snapshots, snapshot schedules and smart quotas, syncIQ policies, syncIQ performance rules, syncIQ reports, syncIQ target reports, syncIQ jobs and to gather facts from the array. The tasks can be executed by running simple playbooks written in yaml syntax.

## License
Ansible collection for PowerScale is released and licensed under the GPL-3.0 license. See [LICENSE](https://www.gnu.org/licenses/gpl-3.0.txt) for the full terms. Ansible modules and modules utilities that are part of the Ansible collection for PowerScale are released and licensed under the Apache 2.0 license. See [MODULE-LICENSE](https://www.apache.org/licenses/LICENSE-2.0.txt) for the full terms.

## Support
Ansible collection for PowerScale are supported by Dell EMC and are provided under the terms of the license attached to the collection. Please see the [LICENSE](#license) section for the full terms. Dell EMC does not provide any support for the source code modifications. For any Ansible modules issues, questions or feedback, join the [Dell EMC Automation Community](https://www.dell.com/community/Automation/bd-p/Automation).

## Supported Platforms
  * Dell EMC PowerScale OneFS versions 8.x, 9.0.x, 9.1.x and 9.2.x

## Prerequisites
This table provides information about the software prerequisites for the Ansible Modules for Dell EMC PowerScale.

| **Ansible Modules** | **OneFS Version** | **Red Hat Enterprise Linux** | **Python version** | **Python SDK version** | **Ansible** |
|---------------------|-----------------------|------------------------------|--------------------|----------------------------|-------------|
| v1.3.0 | 8.x <br> 9.0.x <br> 9.1.x <br> 9.2.x | 7.6 <br> 7.7 <br> 7.8 <br> 8.2 | 3.5 <br> 3.6 | 8.1.1 <br> 9.0.0 | 2.9 <br> 2.10 <br> 2.11 | 

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
  * SyncIQ Policy Module
  * SyncIQ Jobs Module
  * SyncIQ Performance Rules Module
  * SyncIQ Reports Module
  * SyncIQ Target Reports Module

## Installation of SDK
Based on which PowerScale OneFS version is being used, install sdk as  follows:

* For PowerScale OneFS version < 9.0.0, install python [sdk](https://pypi.org/project/isi-sdk-8-1-1/) named 'isi-sdk-8-1-1' as below: 
  
        pip install isi_sdk_8_1_1
  
* For PowerScale OneFS version 9.0.0 and above, install python [sdk](https://pypi.org/project/isi-sdk-9-0-0/) named 'isi-sdk-9-0-0' as below:
        
        pip install isi_sdk_9_0_0

## Building Collections
  1. Use the following command to build the collection from source code:
    
    ansible-galaxy collection build

   For more details on how to build a tar ball, please refer: [Building the collection](https://docs.ansible.com/ansible/latest/dev_guide/developing_collections_distributing.html#building-your-collection-tarball)


## Installing Collections
#### Online Installation of Collections 
  1. Use the following command to install the latest collection hosted in galaxy:

	ansible-galaxy collection install dellemc.powerscale -p <install_path>

  #### Offline Installation of Collections
  1. Download the latest tar build from any of the available distribution channel [Ansible Galaxy](https://galaxy.ansible.com/dellemc/powerscale) /[Automation Hub](https://console.redhat.com/ansible/automation-hub/repo/published/dellemc/powerscale) and use the following command to install the collection anywhere in your system:

	ansible-galaxy collection install dellemc-powerscale-1.3.0.tar.gz -p <install_path>

  2. Set the environment variable:

	export ANSIBLE_COLLECTIONS_PATHS=$ANSIBLE_COLLECTIONS_PATHS:<install_path>

## Using Collections
  1. In order to use any Ansible module, ensure that the importing of a proper FQCN (Fully Qualified Collection Name) must be embedded in the playbook. Refer to the followig example:

	collections:
	- dellemc.powerscale

  2. In order to use an installed collection specific to the task use a proper FQCN (Fully Qualified Collection Name). Refer to the following example:

	tasks:
    - name: Get filesystem details
	  dellemc.powerscale.dellemc_powerscale_filesystem

  3. For generating Ansible documentaion for a specific module, embed the FQCN  before the module name. Refer to the following example:

	ansible-doc dellemc.powerscale.dellemc_powerscale_gatherfacts


## Running Ansible Modules

The Ansible server must be configured with Python library for OneFS to run the Ansible playbooks. The [Documents](https://github.com/dell/ansible-powerscale/tree/1.3.0/docs) provide information on different Ansible modules along with their functions and syntax. The parameters table in the Product Guide provides information on various parameters which need to be configured before running the modules.

## SSL Certificate Validation

* Export the SSL certificate using KeyStore Explorer tool or from the browser in .crt format.
* Append the SSL certificate to the Certifi package file cacert.pem.
    * For Python 3.5 : cat <> >> /usr/local/lib/python3.5/dist-packages/certifi/cacert.pem
    * For Python 2.7 : cat <> >> /usr/local/lib/python2.7/dist-packages/certifi/cacert.pem

## Results
Each module returns the updated state and details of the entity. 
For example, if you are using the group module, all calls will return the updated details of the group.
Sample result is shown in each module's documentation.
