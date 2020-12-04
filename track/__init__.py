from track.version import VERSION
from track.client import Client
__version__ = VERSION

"""Settings"""
api_key = None
default_client = None
host = None
sync_mode = False
debug = False
timeout = 10
max_retries = 3
on_error = None
max_queue_size = 10000


def user(user_id=None, country_code='+91', phone_number=None, traits={}):
    """Send an identify call for customer"""
    return _proxy('user', user_id=user_id, country_code=country_code,
                  phone_number=phone_number, traits=traits)


def event(user_id=None, event=None, traits={}, country_code="+91", phone_number=None):
    """Send an event track call."""
    return _proxy('event', user_id=user_id, event=event, traits=traits,
                  country_code=country_code, phone_number=phone_number)


def flush():
    """Tell the client to flush."""
    _proxy('flush')


def join():
    """Block program until the client clears the queue"""
    _proxy('join')


def shutdown():
    """Flush all messages and cleanly shutdown the client"""
    _proxy('shutdown')


def _proxy(method, *args, **kwargs):
    """Create an analytics client if one doesn't exist and send to it."""
    global default_client
    if not default_client:
        default_client = Client(
            api_key=api_key,
            host=host,
            debug=debug,
            sync_mode=sync_mode,
            timeout=timeout,
            max_queue_size=max_queue_size,
            on_error=on_error,
            max_retries=max_retries
        )

    fn = getattr(default_client, method)
    return fn(*args, **kwargs)
