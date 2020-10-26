import logging

logger = logging.getLogger('interakt')


def require(name, field, data_type):
    """Require that the named `field` has the right `data_type`"""
    if not isinstance(field, data_type):
        msg = '{0} must have {1}, got: {2}'.format(name, data_type, field)
        raise AssertionError(msg)


def remove_trailing_slash(host):
    if host.endswith('/'):
        return host[:-1]
    return host


def stringify(val):
    if val is None:
        return None
    if isinstance(val, str):
        return val
    return str(val)
