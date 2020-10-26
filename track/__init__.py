from track.version import VERSION
from track.client import Client
__version__ = VERSION

"""Settings"""
write_key = None
default_client = None
host = None
sync_mode = True
debug = False
timeout = 10


def identify(user_id=None, country_code='+91', phone_number=None, traits={}):
    """Send an identify call for customer"""
    return _proxy('identify', user_id=user_id, country_code=country_code, phone_number=phone_number, traits=traits)


def event(user_id=None, event=None, traits={}):
    """Send an event track call."""
    return _proxy('event', user_id=user_id, event=event, traits=traits)


def _proxy(method, *args, **kwargs):
    """Create an analytics client if one doesn't exist and send to it."""
    global default_client
    if not default_client:
        default_client = Client(
            write_key, host=host, debug=debug, sync_mode=sync_mode, timeout=timeout)

    fn = getattr(default_client, method)
    return fn(*args, **kwargs)
