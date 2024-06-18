#!/usr/bin/python
# Copyright: (c) 2024, Dell Technologies

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

"""Ansible module for managing support assist settings on PowerScale"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
module: support_assist
version_added: '3.1.0'
short_description: Manage support assist settings on a PowerScale Storage System
description:
- Managing support assist settings on a PowerScale system includes retrieving details of
  support assist settings and modifying support assist settings.

extends_documentation_fragment:
  - dellemc.powerscale.powerscale

author:
  - Trisha Datta (@trisha-dell) <ansible.team@dell.com>
options:
  automatic_case_creation:
    description: True indicates automatic case creation is enabled.
    type: bool
  connection:
    description: Support assist connection details.
    type: dict
    suboptions:
      gateway_endpoints:
        description: List of gateway endpoints.
        type: list
        elements: dict
        suboptions:
          gateway_host:
            description: Hostname or IP address of the gateway endpoint.
            type: str
          gateway_port:
            description: Port number of the gateway endpoint.
            type: int
            default: 9443
          priority:
            description: Priority of the gateway endpoint.
            type: int
            default: 1
          use_proxy:
            description: Use proxy.
            type: bool
            default: false
          validate_ssl:
            description: Validate SSL.
            type: bool
            default: false
          enabled:
            description: Enable the gateway endpoint.
            type: bool
            default: true
          state:
            description: State of the gateway endpoint.
            type: str
            choices: ['absent', 'present']
            default: 'present'
      mode:
        description: Connection mode.
        type: str
        choices: ['direct', 'gateway']
      network_pools:
        description: List of network pools.
        type: list
        elements: dict
        suboptions:
          pool_name:
            description: Name of the network pool.
            type: str
          state:
            description: State of the network pool.
            type: str
            choices: ['absent', 'present']
            default: 'present'
  connection_state:
    description: Set connectivity state.
    type: str
    choices: ['enabled', 'disabled']
  contact:
    description: Information on the remote support contact
    type: dict
    suboptions:
      primary:
        description: Primary contact details.
        type: dict
        suboptions:
          first_name:
            description: First name of the primary contact.
            type: str
          last_name:
            description: Last name of the primary contact.
            type: str
          email:
            description: Email address of the primary contact.
            type: str
          phone:
            description: Phone number of the primary contact.
            type: str
      secondary:
        description: Secondary contact details.
        type: dict
        suboptions:
          first_name:
            description: First name of the secondary contact.
            type: str
          last_name:
            description: Last name of the secondary contact.
            type: str
          email:
            description: Email address of the secondary contact.
            type: str
          phone:
            description: Phone number of the secondary contact.
            type: str
  telemetry:
    description: Enable telemetry.
    type: dict
    suboptions:
      offline_collection_period:
        description:
        - Change the offline collection period for when the connection to gateway is down.
        - The range is 0 to 86400.
        type: int
      telemetry_enabled:
        description: Change the status of telemetry.
        type: bool
      telemetry_persist:
        description: Change if files are kept after upload.
        type: bool
      telemetry_threads:
        description:
        - Change the number of threads for telemetry gathers.
        - The range is 1 to 64.
        type: int
  enable_download:
    description: True indicates downloads are enabled
    type: bool
  enable_remote_support:
    description: Allow remote support.
    type: bool
  enable_service:
    description: Enable/disable SupportAssist service.
    type: bool
  accepted_terms:
    description: Whether to accept or reject the terms and conditions for remote support.
    type: bool
notes:
- The I(check_mode) and idempotency is supported.
- This module is supported for PowerScale One FS version 9.5 and above.
'''

EXAMPLES = r'''
- name: Get support assist setiings
  dellemc.powerscale.support_assist:
    onefs_host: "{{ onefs_host }}"
    port_no: "{{ port_no }}"
    api_user: "{{ api_user }}"
    api_password: "{{ api_password }}"
    verify_ssl: "{{ verify_ssl }}"

- name: Update support assist settings
  dellemc.powerscale.support_assist:
    onefs_host: "{{ onefs_host }}"
    port_no: "{{ port_no }}"
    api_user: "{{ api_user }}"
    api_password: "{{ api_password }}"
    verify_ssl: "{{ verify_ssl }}"
    enable_download: false
    enable_remote_support: false
    automatic_case_creation: false
    connection:
      gateway_endpoints:
        - enabled: true
          gateway_host: "XX.XX.XX.XX"
          gateway_port: 9443
          priority: 1
          use_proxy: false
          validate_ssl: false
          state: present
      network_pools:
        - pool_name: "subnet0:pool0"
          state: absent
        - pool_name: "subnet0:pool1"
    connection_state: "enabled"
    contact:
      primary:
        first_name: "John"
        last_name: "Doe"
        email: "john.doe@example.com"
        phone: "1234567890"
      secondary:
        first_name: "Jane"
        last_name: "Doe"
        email: "jane.doe@example.com"
        phone: "1234567891"
    telemetry:
      offline_collection_period: 60
      telemetry_enabled: true
      telemetry_persist: true
      telemetry_threads: 10

- name: Accept support assist terms
  dellemc.powerscale.support_assist:
    onefs_host: "{{ onefs_host }}"
    port_no: "{{ port_no }}"
    api_user: "{{ api_user }}"
    api_password: "{{ api_password }}"
    verify_ssl: "{{ verify_ssl }}"
    accepted_terms: true
'''

RETURN = r'''
changed:
    description: A boolean indicating if the task had to make changes.
    returned: always
    type: bool
    sample: "false"
support_assist_details:
    description: The updated support assist settings details.
    type: dict
    returned: always
    contains:
      automatic_case_creation:
        description: True indicates automatic case creation is enabled.
        type: bool
      connection:
        description: The server connections.
        type: complex
        contains:
          gateway_endpoints:
            description: List of gateway endpoints.
            type: list
            contains:
              enabled:
                description: True indicates gateway endpoint is enabled.
                type: bool
              host:
                description: Specify the gateway host.
                type: str
              port:
                description: Specify the gateway port.
                type: int
              priority:
                description: Specify the gateway priority.
                type: int
              use_proxy:
                description: Specify whether to use proxy.
                type: bool
              validate_ssl:
                description: Specify whether to validate SSL.
                type: bool
          mode:
            description: Specify the mode.
            type: str
          network_pools:
            description: List of network pools.
            type: list
            contains:
              pool:
                description: The network pool name.
                type: str
              subnet:
                description: The network pool subnet.
                type: str
      connection_state:
        description: Specify the connection state.
        type: str
      contact:
        description: Specify the contact details.
        type: complex
        contains:
          primary:
            description: Specify the primary contact details.
            type: complex
            contains:
              first_name:
                description: First name of the primary contact.
                type: str
              last_name:
                description: Last name of the primary contact.
                type: str
              email:
                description: Email address of the primary contact.
                type: str
              phone:
                description: Phone number of the primary contact.
                type: str
          secondary:
            description: Specify the secondary contact details.
            type: complex
            contains:
              first_name:
                description: First name of the secondary contact.
                type: str
              last_name:
                description: Last name of the secondary contact.
                type: str
              email:
                description: Email address of the secondary contact.
                type: str
              phone:
                description: Phone number of the secondary contact.
                type: str
      enable_download:
        description: True indicates downloads are enabled.
        type: bool
      enable_remote_support:
        description: Whether remoteAccessEnabled is enabled.
        type: bool
      onefs_software_id:
        description: The software ID used by SupportAssist
        type: str
      supportassist_enabled:
        description: Whether SupportAssist is enabled.
        type: bool
      telemetry:
        description: Telemetry settings.
        type: complex
        contains:
          offline_collection_period:
            description: Specify the offline collection period.
            type: int
          telemetry_enabled:
            description: Specify whether telemetry is enabled.
            type: bool
          telemetry_persist:
            description: Specify whether telemetry is persisted.
            type: bool
          telemetry_threads:
            description: Specify the number of telemetry threads.
            type: int
    sample: {
      "automatic_case_creation": false,
      "connection": {
          "gateway_endpoints": [
                {
                    "enabled": true,
                    "host": "XX.XX.XX.XX",
                    "port": 9443,
                    "priority": 1,
                    "use_proxy": false,
                    "validate_ssl": false
                },
                {
                    "enabled": true,
                    "host": "XX.XX.XX.XY",
                    "port": 9443,
                    "priority": 2,
                    "use_proxy": false,
                    "validate_ssl": false
                }
            ],
            "mode": "gateway",
            "network_pools": [
                {
                    "pool": "pool1",
                    "subnet": "subnet0"
                }
            ]
        },
      "connection_state": "disabled",
      "contact": {
          "primary": {
              "email": "p7VYg@example.com",
              "first_name": "Eric",
              "last_name": "Nam",
              "phone": "1234567890"
           },
           "secondary": {
              "email": "kangD@example.com",
              "first_name": "Daniel",
              "last_name": "Kang",
              "phone": "1234567891"
            }
        },
      "enable_download": false,
      "enable_remote_support": false,
      "onefs_software_id": "ELMISL1019H4GY",
      "supportassist_enabled": true,
      "telemetry": {
          "offline_collection_period": 60,
          "telemetry_enabled": true,
          "telemetry_persist": true,
          "telemetry_threads": 10
        }
    }
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell.shared_library.powerscale_base \
    import PowerScaleBase
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import utils
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell.shared_library.support_assist \
    import SupportAssist
import copy

LOG = utils.get_logger('support_assist')


class SupportAssist(PowerScaleBase):
    """Class with support assist settings operations"""

    def __init__(self):
        """ Define all parameters required by the support assist settings module"""

        ansible_module_params = {
            'argument_spec': self.get_support_assist_parameters(),
            'supports_check_mode': True,
        }
        super().__init__(AnsibleModule, ansible_module_params)

        # Result is a dictionary that contains changed status and support assist
        # settings details
        self.result.update({
            "support_assist_details": {}
        })

    def get_support_assist_details(self):
        """
        Get details of support assist settings
        """
        msg = "Getting support assist settings details"
        LOG.info(msg)
        try:
            support_assist_obj = self.support_assist_api.get_supportassist_settings().to_dict()
            if support_assist_obj:
                msg = f"support assist settings details are: {support_assist_obj}"
                LOG.info(msg)
                return support_assist_obj

        except Exception as e:
            error_msg = f"Got error {utils.determine_error(e)} while getting" \
                        f" support assist setings details "
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def modify_support_assist(self, modify_dict):
        """
        Modify the support assist settings based on modify dict
        :param modify_dict: dict containing parameters to be modfied
        """
        try:
            msg = "Modify support assist settings with parameters"
            LOG.info(msg)
            if not self.module.check_mode:
                self.support_assist_api.update_supportassist_settings(
                    supportassist_settings=modify_dict)
                LOG.info("Successfully modified the support assist settings.")
            return True

        except Exception as e:
            error_msg = f"Modify support assist settings failed with " \
                        f"error: {utils.determine_error(e)}"
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def accept_support_assist_terms(self, support_assist_params):
        """
        Accept or reject the support assist terms
        :param support_assist_params: dict containing input parameters
        """
        try:
            msg = "Accept or reject support assist terms"
            LOG.info(msg)
            if not self.module.check_mode:
                terms_dict = {'accepted': support_assist_params['accepted_terms']}
                self.support_assist_api.update_supportassist_terms(
                    supportassist_terms=terms_dict)
                LOG.info("Successfully accepted/rejected the support assist terms.")
            return True

        except Exception as e:
            error_msg = f"Accept or reject support assist terms failed with " \
                        f"error: {utils.determine_error(e)}"
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def add_or_modify_gateway_endpoint(self, settings_params, settings_details, new_endpoint, gateway_list):
        """
        Add a gateway_endpoint to the gateway_endpoints dictionary in the connection dictionary if it doesn't already exist,
        or modify it if it does by gateway_host
        """
        new_endpoint['host'] = new_endpoint['gateway_host']
        new_endpoint['port'] = new_endpoint['gateway_port']
        del new_endpoint['gateway_host'], new_endpoint['gateway_port'], new_endpoint['state']
        flag = False
        for endpoints in range(len(settings_details['connection']['gateway_endpoints'])):
            if settings_details['connection']['gateway_endpoints'][endpoints]['host'] == \
                    new_endpoint['host']:
                flag = True
                if settings_details['connection']['gateway_endpoints'][endpoints] != \
                        new_endpoint:
                    gateway_list[endpoints] = new_endpoint
        if flag is False:
            gateway_list.append(new_endpoint)
        return gateway_list

    def remove_gateway_endpoint(self, settings_params, new_endpoint, gateway_list):
        """
        Remove a gateway_endpoint from the gateway_endpoints list in the connection dictionary
        """
        new_endpoint['host'] = new_endpoint['gateway_host']
        new_endpoint['port'] = new_endpoint['gateway_port']
        del new_endpoint['gateway_host'], new_endpoint['gateway_port'], new_endpoint['state']
        remainder_list = copy.deepcopy(gateway_list)
        for endpoints in range(len(gateway_list)):
            if gateway_list[endpoints]['host'] == new_endpoint['host']:
                remainder_list.remove(gateway_list[endpoints])
        return remainder_list

    def prepare_existing_network_pool_list(self, settings_details):
        """
        Prepare a list of existing network pools
        """
        existing_pool_list = []
        for pool in range(len(settings_details['connection']['network_pools'])):
            pool_name = settings_details['connection']['network_pools'][pool]['subnet'] + ":" \
                + settings_details['connection']['network_pools'][pool]['pool']
            existing_pool_list.append(pool_name)
        return existing_pool_list

    def add_or_remove_network_pools(self, settings_params, settings_details, connection_dict):
        """
        Add or remove a network pool parameter to/from the connection
        """
        pool_list = self.prepare_existing_network_pool_list(settings_details=settings_details)
        connection = settings_params['connection']
        existing_network_pools = copy.deepcopy(pool_list)
        for pool in range(len(settings_params['connection']['network_pools'])):
            if connection.get('network_pools')[pool]['state'] == 'present' and \
                    connection.get('network_pools')[pool]['pool_name'] not in existing_network_pools:
                pool_list.append(connection.get('network_pools')[pool]['pool_name'])
            if connection.get('network_pools')[pool]['state'] == 'absent' and \
                    connection.get('network_pools')[pool]['pool_name'] in existing_network_pools:
                pool_list.remove(connection.get('network_pools')[pool]['pool_name'])
        if set(existing_network_pools) != set(pool_list):
            if pool_list == []:
                error_msg = "Network pool list cannot be empty."
                LOG.error(error_msg)
                self.module.fail_json(msg=error_msg)
            connection_dict['network_pools'] = pool_list
        return connection_dict

    def update_gateway_endpoints(self, settings_params, settings_details, connection_dict):
        """
        Update the gateway_endpoints list in the connection dictionary
        """
        gateway_params = copy.deepcopy(settings_params['connection']['gateway_endpoints'])
        gateway_list = copy.deepcopy(settings_details['connection']['gateway_endpoints'])
        for new_endpoint in gateway_params:
            if new_endpoint.get('state') == 'present':
                gateway_list = self.add_or_modify_gateway_endpoint(settings_params=settings_params,
                                                                   settings_details=settings_details,
                                                                   new_endpoint=new_endpoint,
                                                                   gateway_list=gateway_list)
            elif new_endpoint.get('state') == 'absent':
                gateway_list = self.remove_gateway_endpoint(settings_params=settings_params,
                                                            new_endpoint=new_endpoint,
                                                            gateway_list=gateway_list)
        if gateway_list != settings_details['connection']['gateway_endpoints']:
            connection_dict['gateway_endpoints'] = gateway_list
        return connection_dict

    def is_support_assist_connection_modify_required(self, settings_params, settings_details, modify_dict):
        """
        Check whether modification is required in support assist connection settings
        """
        connection_dict = {}
        if settings_params.get('connection'):
            connection = settings_params['connection']
            if connection.get('gateway_endpoints'):
                connection_dict = self.update_gateway_endpoints(settings_params=settings_params,
                                                                settings_details=settings_details,
                                                                connection_dict=connection_dict)
            if connection.get('mode') and settings_params['connection']['mode'] != settings_details['connection']['mode']:
                connection_dict['mode'] = settings_params['connection']['mode']
            if connection.get('network_pools'):
                connection_dict = self.add_or_remove_network_pools(settings_params=settings_params,
                                                                   settings_details=settings_details,
                                                                   connection_dict=connection_dict)
            if connection_dict != {}:
                modify_dict['connection'] = connection_dict
        return modify_dict

    def is_support_assist_telemetry_modify_required(self, settings_params, settings_details, modify_dict):
        """
        Check whether modification is required in support assist telemetry settings
        """
        telemetry_keys = ["offline_collection_period", "telemetry_enabled",
                          "telemetry_persist", "telemetry_threads"]
        telemetry = settings_params.get('telemetry')
        telemetry_dict = {}

        if telemetry is not None:
            if telemetry['telemetry_enabled'] is True:
                for key in telemetry_keys:
                    if telemetry.get(key) is not None and \
                            settings_details['telemetry'].get(key) != telemetry[key]:
                        telemetry_dict[key] = telemetry[key]
            if telemetry['telemetry_enabled'] is False and \
                    settings_details['telemetry']['telemetry_enabled'] is not False:
                telemetry_dict['telemetry_enabled'] = telemetry['telemetry_enabled']
        if telemetry_dict != {}:
            modify_dict["telemetry"] = telemetry_dict
        return modify_dict

    def is_support_assist_modify_required(self, settings_params, settings_details):
        """
        Check whether modification is required in support assist settings
        """
        modify_dict = {}
        support_assist_keys = ["enable_download", "enable_remote_support",
                               "automatic_case_creation", "connection_state"]
        for key in support_assist_keys:
            if settings_params.get(key) is not None and \
                    settings_details[key] != settings_params[key]:
                modify_dict[key] = settings_params[key]

        if settings_params['enable_service'] is not None and \
                settings_params['enable_service'] != settings_details['supportassist_enabled']:
            modify_dict['enable_service'] = settings_params['enable_service']

        return modify_dict

    def validate_phone(self, phone):
        if phone is not None and not phone.isnumeric():
            error_msg = "The contact phone is invalid"
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def is_support_assist_contact_modify_required(self, settings_params, settings_details, modify_dict):
        """
        Check whether modification is required in support assist settings
        """
        contact = {}
        if settings_params['contact']:
            if settings_params['contact']['primary']:
                if settings_params['contact']['primary'] != settings_details['contact']['primary']:
                    self.validate_phone(phone=settings_params['contact']['primary']['phone'])
                    contact['primary'] = settings_params['contact']['primary']
            if settings_params['contact']['secondary']:
                if settings_params['contact']['secondary'] != settings_details['contact']['secondary']:
                    self.validate_phone(phone=settings_params['contact']['secondary']['phone'])
                    contact['secondary'] = settings_params['contact']['secondary']
        if contact != {}:
            modify_dict['contact'] = contact

        return modify_dict

    def get_support_assist_parameters(self):
        return dict(
            accepted_terms=dict(type='bool'),
            automatic_case_creation=dict(type='bool'),
            connection=dict(
                type='dict', options=dict(
                    gateway_endpoints=dict(
                        type='list', elements='dict', options=dict(
                            enabled=dict(type='bool', default=True),
                            gateway_host=dict(type='str'),
                            gateway_port=dict(type='int', default=9443),
                            priority=dict(type='int', default=1),
                            use_proxy=dict(type='bool', default=False),
                            validate_ssl=dict(type='bool', default=False),
                            state=dict(type='str', choices=['present', 'absent'], default='present'))
                    ),
                    mode=dict(type='str', choices=['direct', 'gateway']),
                    network_pools=dict(type='list', elements='dict', options=dict(
                        pool_name=dict(type='str'),
                        state=dict(type='str', choices=['present', 'absent'], default='present')))
                )
            ),
            connection_state=dict(type='str', choices=['enabled', 'disabled']),
            enable_download=dict(type='bool'),
            enable_remote_support=dict(type='bool'),
            enable_service=dict(type='bool'),
            contact=dict(
                type='dict', options=dict(
                    primary=dict(
                        type='dict', options=dict(
                            email=dict(type='str'),
                            first_name=dict(type='str'),
                            last_name=dict(type='str'),
                            phone=dict(type='str'))
                    ),
                    secondary=dict(
                        type='dict', options=dict(
                            email=dict(type='str'),
                            first_name=dict(type='str'),
                            last_name=dict(type='str'),
                            phone=dict(type='str'))
                    )
                )
            ),
            telemetry=dict(
                type='dict', options=dict(
                    offline_collection_period=dict(type='int'),
                    telemetry_enabled=dict(type='bool'),
                    telemetry_persist=dict(type='bool'),
                    telemetry_threads=dict(type='int')
                ))
        )


class SupportAssistExitHandler:
    def handle(self, support_assist_obj, support_assist_details):
        support_assist_obj.result["support_assist_details"] = support_assist_details
        support_assist_obj.module.exit_json(**support_assist_obj.result)


class SupportAssistAcceptTermsHandler:
    def handle(self, support_assist_obj, support_assist_params, support_assist_details):
        if support_assist_params['accepted_terms'] is not None:
            support_assist_obj.result["changed"] = support_assist_obj.accept_support_assist_terms(
                support_assist_params=support_assist_params)

        SupportAssistExitHandler().handle(support_assist_obj, support_assist_details)


class SupportAssistModifyHandler:
    def handle(self, support_assist_obj, support_assist_params, support_assist_details):
        modify_params = support_assist_obj.is_support_assist_modify_required(settings_params=support_assist_params,
                                                                             settings_details=support_assist_details)
        modify_params = support_assist_obj.is_support_assist_telemetry_modify_required(settings_params=support_assist_params,
                                                                                       settings_details=support_assist_details,
                                                                                       modify_dict=modify_params)

        modify_params = support_assist_obj.is_support_assist_connection_modify_required(settings_params=support_assist_params,
                                                                                        settings_details=support_assist_details,
                                                                                        modify_dict=modify_params)

        modify_params = support_assist_obj.is_support_assist_contact_modify_required(settings_params=support_assist_params,
                                                                                     settings_details=support_assist_details,
                                                                                     modify_dict=modify_params)

        if modify_params:
            changed = support_assist_obj.modify_support_assist(
                modify_dict=modify_params)
            support_assist_details = support_assist_obj.get_support_assist_details()
            support_assist_obj.result["changed"] = changed
            support_assist_obj.result["support_assist_details"] = support_assist_details

        SupportAssistAcceptTermsHandler().handle(support_assist_obj, support_assist_params, support_assist_details)


class SupportAssistHandler:
    def handle(self, support_assist_obj, support_assist_params):
        support_assist_details = support_assist_obj.get_support_assist_details()
        SupportAssistModifyHandler().handle(
            support_assist_obj=support_assist_obj, support_assist_params=support_assist_params,
            support_assist_details=support_assist_details)


def main():
    """ perform action on PowerScale Support Assist and perform action on it
        based on user input from playbook."""
    obj = SupportAssist()
    SupportAssistHandler().handle(obj, obj.module.params)


if __name__ == '__main__':
    main()
