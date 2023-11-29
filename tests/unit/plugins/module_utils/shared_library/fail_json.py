# Copyright: (c) 2023, Dell Technologies

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

"""Mock fail json for PowerScale Test modules"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type


class FailJsonException(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None


def fail_json(msg, **kwargs):
    raise FailJsonException(msg)
