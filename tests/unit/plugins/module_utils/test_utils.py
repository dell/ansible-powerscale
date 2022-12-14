# Copyright: (c) 2021, Dell Technologies

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

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
