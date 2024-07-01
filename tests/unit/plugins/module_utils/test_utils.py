# Copyright: (c) 2021-2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Utils for PowerScale Test modules"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import random
import string


def get_desc(length):
    desc = ''
    while (length > 0):
        desc += random.choice(string.ascii_letters)
        length -= 1
    return desc
