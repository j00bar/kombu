"""
kombu.utils.encoding
====================

Unicode utilities.

:copyright: (c) 2009 - 2011 by Ask Solem.
:license: BSD, see LICENSE for more details.

"""
from __future__ import absolute_import

import sys
import traceback

__all__ = ["default_encoding", "safe_str", "safe_repr"]


if sys.version_info >= (3, 0):
    def str_to_bytes(s):
        if isinstance(s, str):
            return s.encode()
        return s

    def bytes_to_str(s):
        if isinstance(s, bytes):
            return s.decode()
        return s

else:  # noqa
    def str_to_bytes(s):
        return s

    def bytes_to_str(s):
        return s


def default_encoding():
    if sys.platform.startswith("java"):
        return "utf-8"
    return sys.getfilesystemencoding()


def safe_str(s, errors="replace"):
    if not isinstance(s, basestring):
        return safe_repr(s, errors)
    return _safe_str(s, errors)


def _safe_str(s, errors="replace"):
    encoding = default_encoding()
    try:
        if isinstance(s, unicode):
            return s.encode(encoding, errors)
        return unicode(s, encoding, errors)
    except Exception, exc:
        return "<Unrepresentable %r: %r %r>" % (
                type(s), exc, "\n".join(traceback.format_stack()))


def safe_repr(o, errors="replace"):
    try:
        return repr(o)
    except Exception:
        return _safe_str(o, errors)