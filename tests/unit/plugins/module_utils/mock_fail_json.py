# Copyright: (c) 2023, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Mock fail json for PowerScale Test modules"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type


class FailJsonException(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None


def fail_json(msg):
    raise FailJsonException(msg)
