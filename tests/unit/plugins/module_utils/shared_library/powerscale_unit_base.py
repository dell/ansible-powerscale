# Copyright: (c) 2023-2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type
import copy
import pytest
from mock.mock import MagicMock

from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_api_exception \
    import MockApiException


class PowerScaleUnitBase:

    '''Powerscale Unit Test Base Class'''

    @pytest.fixture(autouse=True)
    def powerscale_module_mock(self, mocker, module_object):
        exception_class_path = 'ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell.utils.ApiException'
        mocker.patch(exception_class_path, new=MockApiException)
        self.powerscale_module_mock = module_object()
        self.powerscale_module_mock.module = MagicMock()
        self.powerscale_module_mock.module.fail_json = MagicMock(
            side_effect=SystemExit)
        self.powerscale_module_mock.module.check_mode = False
        return self.powerscale_module_mock

    def capture_fail_json_call(self, error_msg, module_handler=None, invoke_perform_module=False):
        with pytest.raises(SystemExit):
            if not invoke_perform_module:
                module_handler().handle(self.powerscale_module_mock,
                                        self.powerscale_module_mock.module.params)
            else:
                self.powerscale_module_mock.perform_module_operation()
        self.powerscale_module_mock.module.fail_json.assert_called()
        call_args = self.powerscale_module_mock.module.fail_json.call_args.kwargs
        assert error_msg in call_args['msg']

    def capture_fail_json_method(self, error_msg, module_mock, function_name, *args, **kwargs):
        with pytest.raises(SystemExit):
            func = getattr(module_mock, function_name)
            func(*args, **kwargs)
        self.powerscale_module_mock.module.fail_json.assert_called()
        call_args = self.powerscale_module_mock.module.fail_json.call_args.kwargs
        assert error_msg in call_args['msg']

    def set_module_params(self, get_module_args, params, deep_copy=True):
        if deep_copy:
            get_module_args = copy.deepcopy(get_module_args)
        get_module_args.update(params)
        self.powerscale_module_mock.module.params = get_module_args
