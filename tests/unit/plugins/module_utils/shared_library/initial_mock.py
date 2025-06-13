# Copyright: (c) 2023-2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type
from mock.mock import MagicMock
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import utils

utils.get_logger = MagicMock()
utils.isi_sdk = MagicMock()
utils.isi_sdk.major = 9
utils.isi_sdk.minor = 7
utils.ISI_SDK_VERSION_9 = MagicMock(return_value=True)
PREREQS_VALIDATE = {
    "all_packages_found": True
}
utils.validate_module_pre_reqs = MagicMock(return_value=PREREQS_VALIDATE)
from ansible.module_utils import basic
basic.AnsibleModule = MagicMock()
