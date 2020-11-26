import logging
from phonenumbers.phonenumberutil import region_code_for_country_code

logger = logging.getLogger('interakt')


def require(name, field, data_type):
    """Require that the named `field` has the right `data_type`"""
    if not isinstance(field, data_type):
        msg = '{0} must have {1}, got: {2}'.format(name, data_type, type(field))
        raise AssertionError(msg)


def verify_country_code(country_code: str):
    """Verifies country code of the phone number"""
    country_code = country_code.replace("+", "")
    if not country_code.isdigit():
        raise AssertionError(f"Invalid country_code {country_code}")

    region_code = region_code_for_country_code(int(country_code))
    if region_code == "ZZ":
        raise AssertionError(f"Invalid country_code {country_code}")


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
