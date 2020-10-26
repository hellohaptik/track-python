import logging

from requests import sessions
from requests.auth import HTTPBasicAuth

from track.utils import remove_trailing_slash
from track.version import VERSION
from track.const import DEFAULT_HOST

_session = sessions.session()
logger = logging.getLogger('interakt')


def post(write_key, host=None, path=None, body=None, timeout=10):
    """Post the msg to the API"""
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': f'interakt-track-python/{VERSION}',
        'Authorization': write_key
    }
    url = remove_trailing_slash(host or DEFAULT_HOST) + path
    logger.debug(f'Making request: {body}')
    response = _session.post(url=url, headers=headers,
                             json=body, timeout=timeout)
    payload = response.json()
    logger.debug(f'Received response: {payload}')
    return response
