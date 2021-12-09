# Copyright: (c) 2021, DellEMC

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

"""Mock SDKResponse for Unit tests for PowerScale modules"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type
ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'
                    }


class MockSDKResponse:
    def __init__(self, data=None, status_code=200):
        self.data = data
        self.status_code = status_code

    def to_dict(self):
        return self.data
