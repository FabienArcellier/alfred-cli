# pylint: disable=pointless-string-statement

from typing import NewType

"""
path of object (directory or file) in filesystem
/root
"""
path = NewType('path', str)  # pylint: disable=invalid-name
