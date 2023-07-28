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


def get_ads_response_for_spn():
    return [{
        'id': 'ads_domain',
        'spns': [
            'abc',
            'def',
            'ghi',
        ],
        'recommended_spns': [
            'abc',
            'def',
            'ghi',
            'klm'
        ],
        'extra_expected_spns': []
    }]


def get_provider_summary():
    provider_summary = MagicMock()
    provider_summary.forest = 'ads_domain'
    provider_summary.type = 'ads'
    provider_summary.name = 'ads_domain'
    return [
        provider_summary
    ]
