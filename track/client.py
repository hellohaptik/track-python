import atexit
import logging
import numbers

from track.const import ApiPaths
from track.consumer import Consumer
from track.request import post
from track.utils import require, stringify

try:
    import queue
except ImportError:
    import Queue as queue

ID_TYPES = (numbers.Number, str)


class Client(object):
    logger = logging.getLogger('interakt')

    def __init__(self, write_key=None, host=None, debug=False,
                 sync_mode=True, timeout=10, max_queue_size=10000,
                 on_error=None, max_retries=3, flush_interval=0.5):
        """Create a new interakt client"""
        require('write_key', write_key, str)

        self.queue = queue.Queue(maxsize=max_queue_size)
        self.write_key = write_key
        self.debug = debug
        self.host = host
        self.sync_mode = sync_mode
        self.timeout = timeout
        self.on_error = on_error
        if debug:
            self.logger.setLevel(logging.DEBUG)

        if sync_mode:
            self.consumer = None
        else:
            atexit.register(self.join)
            self.consumer = Consumer(
                queue=self.queue, write_key=write_key,
                host=host, on_error=on_error, retries=max_retries,
                timeout=timeout, flush_interval=flush_interval
            )
            self.consumer.start()

    def identify(self, user_id=None, country_code='+91', phone_number=None, traits={}):
        """Tie a user to their actions and record traits about them."""
        if not user_id and not phone_number:
            raise AssertionError("Either user_id or phone_number is required")
        if user_id:
            require('user_id', user_id, ID_TYPES)
        if phone_number:
            require('phone_number', phone_number, str)
        require('traits', traits, dict)
        body = {
            'userId': stringify(val=user_id),
            'countryCode': country_code,
            'phoneNumber': phone_number,
            'traits': traits
        }
        return self.__queue_request(path=ApiPaths.Identify.value, body=body)

    def event(self, user_id=None, event=None, traits={}):
        """To record user events"""
        traits = traits or {}
        require('user_id', user_id, ID_TYPES)
        require('traits', traits, dict)
        require('event', event, str)
        body = {
            'userId': stringify(val=user_id),
            'event': event,
            'traits': traits
        }
        return self.__queue_request(path=ApiPaths.Event.value, body=body)

    def flush(self):
        """Forces a flush from the internal queue to the server"""
        queue = self.queue
        size = queue.qsize()
        queue.join()
        # Note that this message may not be precise, because of threading.
        self.logger.debug('Successfully flushed about %s items.', size)

    def join(self):
        """Ends the consumer thread once the queue is empty.
        Blocks execution until finished
        """
        self.consumer.pause()
        try:
            self.consumer.join()
        except RuntimeError:
            # consumer thread has not started
            pass

    def shutdown(self):
        """Flush all messages and cleanly shutdown the client"""
        self.flush()
        self.join()

    def __queue_request(self, path, body):
        # Directly call api in sync mode and return response
        if self.sync_mode:
            return post(self.write_key, host=self.host, path=path, body=body, timeout=self.timeout)

        queue_msg = {
            'path': path,
            'body': body
        }
        try:
            self.queue.put(queue_msg, block=False)
            self.logger.debug(f'Enqueued msg for {path}')
            return True, queue_msg
        except queue.Full:
            self.logger.warning('track-python queue is full')
            return False, queue_msg
