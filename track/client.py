from track.utils import require, stringify
from track.request import post
from track.const import ApiPaths
import logging
import numbers
ID_TYPES = (numbers.Number, str)


class Client(object):
    logger = logging.getLogger('interakt')

    def __init__(self, write_key=None, host=None, debug=False, sync_mode=True, timeout=10):
        """Create a new interakt client"""
        require('write_key', write_key, str)
        self.write_key = write_key
        self.debug = debug
        self.host = host
        self.sync_mode = sync_mode
        self.timeout = timeout
        if debug:
            self.logger.setLevel(logging.DEBUG)

    def identify(self, user_id=None, country_code='+91', phone_number=None, traits={}):
        """Tie a user to their actions and record traits about them."""
        if not user_id and not phone_number:
            raise AssertionError("Either user_id or phone_number is required")
        if user_id:
            require('user_id', user_id, ID_TYPES)
        if phone_number:
            require('phone_number', phone_number, str)
        require('traits', traits, dict)
        msg = {
            'userId': stringify(val=user_id),
            'countryCode': country_code,
            'phoneNumber': phone_number,
            'traits': traits
        }
        return self.__send_request(path=ApiPaths.Identify.value, msg=msg)

    def event(self, user_id=None, event=None, traits={}):
        """To record user events"""
        traits = traits or {}
        require('user_id', user_id, ID_TYPES)
        require('traits', traits, dict)
        require('event', event, str)
        msg = {
            'userId': stringify(val=user_id),
            'event': event,
            'traits': traits
        }
        return self.__send_request(path=ApiPaths.Event.value, msg=msg)

    def __send_request(self, path, msg):
        return post(self.write_key, host=self.host, path=path, body=msg, timeout=self.timeout)
