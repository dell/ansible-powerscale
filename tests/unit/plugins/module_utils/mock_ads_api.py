# Copyright: (c) 2022, Dell Technologies

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

"""Mock Ads Api for Ads Test module on PowerScale"""

from __future__ import (absolute_import, division, print_function)
from unittest.mock import MagicMock

__metaclass__ = type


def get_ads_response():
    ads_response = MagicMock()
    ads_response.id = "ads_domain"
    return ads_response


def create_ads_ex_msg():
    return "Add an Active Directory provider failed with"
