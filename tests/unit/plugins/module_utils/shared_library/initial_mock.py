# Copyright: (c) 2023, Dell Technologies

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type
from mock.mock import MagicMock
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import utils

utils.get_logger = MagicMock()
utils.isi_sdk = MagicMock()
utils.ISI_SDK_VERSION_9 = MagicMock(return_value=True)
PREREQS_VALIDATE = {
    "all_packages_found": True
}
utils.validate_module_pre_reqs = MagicMock(return_value=PREREQS_VALIDATE)
from ansible.module_utils import basic
basic.AnsibleModule = MagicMock()
