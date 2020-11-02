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
    auth = HTTPBasicAuth(username=write_key, password="")
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': f'interakt-track-python/{VERSION}'
    }
    url = remove_trailing_slash(host or DEFAULT_HOST) + path
    logger.debug(f'Making request: {body}')
    response = _session.post(url=url, headers=headers,
                             auth=auth, json=body, timeout=timeout)
    if response.status_code == 200:
        logger.debug("Data uploaded successfully")
        return response

    try:
        payload = response.json()
        logger.debug(f'Received response: {payload}')
        raise APIError(payload.get("result"),
                       response.status_code, payload.get("message"))
    except ValueError:
        raise APIError('Unknown', response.status_code, response.text)


class APIError(Exception):

    def __init__(self, status, status_code, message):
        self.message = message
        self.status = status
        self.status_code = status_code

    def __str__(self):
        msg = "[interakt-track] StatusCode({0}): {1} (Success={2})"
        return msg.format(self.status_code, self.message, self.status)
