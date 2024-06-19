<!--
Copyright (c) 2024 Dell Inc., or its subsidiaries. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0
-->

# Installation and execution of Ansible modules for Dell PowerScale

## Installation of sdk
Use this procedure to install SDK:
  
       pip install isilon-sdk
  
## Building collections
  1. Use this command to build the collection from source code:
    
        ansible-galaxy collection build

   For more details on how to build a tar ball, please refer: [Building the collection](https://docs.ansible.com/ansible/latest/dev_guide/developing_collections_distributing.html#building-your-collection-tarball)


## Installing collections
#### Online installation of collections 
  1. Use this command to install the latest collection hosted in galaxy:

	      ansible-galaxy collection install dellemc.powerscale -p <install_path>

  #### Offline installation of collections
  1. Download the latest tar build from either of the available distribution channels [Ansible Galaxy](https://galaxy.ansible.com/dellemc/powerscale) /[Automation Hub](https://console.redhat.com/ansible/automation-hub/repo/published/dellemc/powerscale) and use this command to install the collection anywhere in your system:

	      ansible-galaxy collection install dellemc-powerscale-3.1.0.tar.gz -p <install_path>

  2. Set the environment variable:

	      export ANSIBLE_COLLECTIONS_PATHS=$ANSIBLE_COLLECTIONS_PATHS:<install_path>

## Using collections

  * In order to use any Ansible module, ensure that the importing of proper FQCN (Fully Qualified Collection Name) must be embedded in the playbook.
   Refer to this example:
 
        collections:
        - dellemc.powerscale

  * In order to use an installed collection specific to the task use a proper FQCN (Fully Qualified Collection Name). Refer to this example:

        tasks:
        - name: Get filesystem details
          dellemc.powerscale.filesystem
    
  * For generating Ansible documentation for a specific module, embed the FQCN  before the module name. Refer to this example:
        
        ansible-doc dellemc.powerscale.info


## Ansible modules execution

The Ansible server must be configured with Python library for OneFS to run the Ansible playbooks. The [Documents](https://github.com/dell/ansible-powerscale/blob/main/docs) provide information on different Ansible modules along with their functions and syntax. The parameters table in the Product Guide provides information on various parameters which need to be configured before running the modules.

## SSL certificate validation

* Export the SSL certificate using KeyStore Explorer tool or from the browser in .crt format.
* Append the SSL certificate to the Certifi package file cacert.pem.
      * For Python 3.6 : cat <> >> /usr/local/lib/python3.6/dist-packages/certifi/cacert.pem

## Results
Each module returns the updated state and details of the entity. 
For example, if you are using the group module, all calls will return the updated details of the group.
Sample result is shown in each module's documentation.

## Idempotency
The modules are written in such a way that all requests are idempotent and hence fault-tolerant. It essentially means that the result of a successfully performed request is independent of the number of times it is executed.

## Ansible execution environment

Ansible can also be installed in a container environment. Ansible Builder provides the ability to create reproducible, self-contained environments as container images that can be run as Ansible execution environments.
* Install the ansible builder package using:

         pip3 install ansible-builder

* Ensure the execution-environment.yml is at the root of collection and create the execution environment using:

         ansible-builder build --tag <tag_name> --container-runtime docker

* After the image is built, run the container using:

         docker run -it <tag_name> /bin/bash

* Verify collection installation using command:

         ansible-galaxy collection list

* The playbook can be run on the container using:

         docker run --rm -v $(pwd):/runner <tag_name> ansible-playbook info_tests.yml
