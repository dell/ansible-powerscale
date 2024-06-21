# Copyright: (c) 2024, Dell Technologies

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import utils

LOG = utils.get_logger('support_assist')


class SupportAssist:

    '''Class with shared support assist operations'''

    def __init__(self, support_assist_api, module):
        """
        Initialize the support assist class
        :param support_assist_api: The support assist SDK instance
        :param module: Ansible module object
        """
        self.support_assist_api = support_assist_api
        self.module = module

    def get_support_assist_settings(self):
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
                        f" support assist settings details "
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)
