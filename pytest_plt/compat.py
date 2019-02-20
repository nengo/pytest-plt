import sys

PY2 = sys.version_info[0] == 2


def is_string(obj):
    if PY2:
        # pylint: disable=undefined-variable
        string_types = (str, unicode)  # noqa: F821
    else:
        string_types = (str,)
    return isinstance(obj, string_types)
