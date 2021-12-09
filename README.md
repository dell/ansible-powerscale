# Ansible Modules for Dell EMC PowerScale
The Ansible Modules for Dell EMC PowerScale allow Data Center and IT administrators to use RedHat Ansible to automate and orchestrate the configuration and management of Dell EMC PowerScale arrays.

The Ansible Modules for Dell EMC PowerScale support the following features:
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
- Get attributes and entities of the array.

The tasks can be executed by running simple playbooks written in yaml syntax.

## License
Ansible collection for PowerScale is released and licensed under the GPL-3.0 license. See [LICENSE](LICENSE) for the full terms. Ansible modules and modules utilities that are part of the Ansible collection for PowerScale are released and licensed under the Apache 2.0 license. See [MODULE-LICENSE](MODULE-LICENSE) for the full terms.

## Support
Ansible collection for PowerScale are supported by Dell EMC and are provided under the terms of the license attached to the collection. Please see the [LICENSE](#license) section for the full terms. Dell EMC does not provide any support for the source code modifications. For any Ansible modules issues, questions or feedback, join the [Dell EMC Automation Community](https://www.dell.com/community/Automation/bd-p/Automation).

## Supported Platforms
  * Dell EMC PowerScale OneFS versions 8.x, 9.0.x, 9.1.x and 9.2.x

## Prerequisites
This table provides information about the software prerequisites for the Ansible Modules for Dell EMC PowerScale.

| **Ansible Modules** | **OneFS Version** | **Red Hat Enterprise Linux** | **Python version** | **Python SDK version** | **Ansible** |
|---------------------|-----------------------|------------------------------|--------------------|----------------------------|-------------|
| v1.4.0 | 8.x <br> 9.0.x <br> 9.1.x <br> 9.2.x | 7.6 <br> 7.7 <br> 7.8 <br> 8.2 | 3.5 <br> 3.6 <br> 3.9 | 8.1.1 <br> 9.0.0 | 2.9 <br> 2.10 <br> 2.11 | 

## Idempotency
The modules are written in such a way that all requests are idempotent and hence fault-tolerant. It essentially means that the result of a successfully performed request is independent of the number of times it is executed.

## List of Ansible Modules for Dell EMC PowerScale
  * [File System Module](docs/Product%20Guide.md#file-system-module)
  * [Access Zone Module](docs/Product%20Guide.md#accesszone-module)
  * [Users Module](docs/Product%20Guide.md#user-module)
  * [Groups Module](docs/Product%20Guide.md#group-module)
  * [Snapshot Module](docs/Product%20Guide.md#snapshot-module)
  * [Snapshot Schedule Module](docs/Product%20Guide.md#snapshot-schedule-module)
  * [NFS Module](docs/Product%20Guide.md#nfs-module)
  * [SMB Module](docs/Product%20Guide.md#smb-module)
  * [Smart Quota Module](docs/Product%20Guide.md#smart-quota-module)
  * [Gather Facts Module](docs/Product%20Guide.md#gatherfacts-module)
  * [Active Directory Module](docs/Product%20Guide.md#ads-module)
  * [LDAP Module](docs/Product%20Guide.md#ldap-module)
  * [Node Module](docs/Product%20Guide.md#node-module)
  * [SyncIQ Policy Module](docs/Product%20Guide.md#synciq-policy-module)
  * [SyncIQ Jobs Module](docs/Product%20Guide.md#synciq-job-module)
  * [SyncIQ Performance Rules Module](docs/Product%20Guide.md#synciq-performance-rules-module)
  * [SyncIQ Reports Module](docs/Product%20Guide.md#synciq-reports-module)
  * [SyncIQ Target Reports Module](docs/Product%20Guide.md#synciq-target-reports-module)
  * [Groupnet Module](docs/Product%20Guide.md#networkgroupnet-module)
  * [Subnet Module](docs/Product%20Guide.md#subnet-module)
  * [Network Pool Module](docs/Product%20Guide.md#networkpool-module)
  * [Network Rule Module](docs/Product%20Guide.md#networkrule-module)
  * [Settings Module](docs/Product%20Guide.md#settings-module)

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
  1. Download the latest tar build from either of the available distribution channels [Ansible Galaxy](https://galaxy.ansible.com/dellemc/powerscale) /[Automation Hub](https://console.redhat.com/ansible/automation-hub/repo/published/dellemc/powerscale) and use the following command to install the collection anywhere in your system:

	ansible-galaxy collection install dellemc-powerscale-1.4.0.tar.gz -p <install_path>

  2. Set the environment variable:

	export ANSIBLE_COLLECTIONS_PATHS=$ANSIBLE_COLLECTIONS_PATHS:<install_path>

## Using Collections
  1. In order to use any Ansible module, ensure that the importing of a proper FQCN (Fully Qualified Collection Name) must be embedded in the playbook. Refer to the following example:

	collections:
	- dellemc.powerscale

  2. In order to use an installed collection specific to the task use a proper FQCN (Fully Qualified Collection Name). Refer to the following example:

	tasks:
    - name: Get filesystem details
	  dellemc.powerscale.dellemc_powerscale_filesystem

  3. For generating Ansible documentaion for a specific module, embed the FQCN  before the module name. Refer to the following example:

	ansible-doc dellemc.powerscale.dellemc_powerscale_gatherfacts


## Running Ansible Modules

The Ansible server must be configured with Python library for OneFS to run the Ansible playbooks. The [Documents](./docs) provide information on different Ansible modules along with their functions and syntax. The parameters table in the Product Guide provides information on various parameters which need to be configured before running the modules.

## SSL Certificate Validation

* Export the SSL certificate using KeyStore Explorer tool or from the browser in .crt format.
* Append the SSL certificate to the Certifi package file cacert.pem.
    * For Python 3.5 : cat <> >> /usr/local/lib/python3.5/dist-packages/certifi/cacert.pem
    * For Python 2.7 : cat <> >> /usr/local/lib/python2.7/dist-packages/certifi/cacert.pem

## Results
Each module returns the updated state and details of the entity. 
For example, if you are using the group module, all calls will return the updated details of the group.
Sample result is shown in each module's documentation.
