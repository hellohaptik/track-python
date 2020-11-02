import logging
from threading import Thread
from track.request import post, APIError
import backoff

try:
    from queue import Empty
except ImportError:
    from Queue import Empty


class Consumer(Thread):
    """Consumes the messages from the client's queue."""
    logger = logging.getLogger('interakt')

    def __init__(self, queue, write_key, host=None,
                 on_error=None, retries=3, timeout=10,
                 flush_interval=0.5):
        Thread.__init__(self)
        self.running = True
        self.queue = queue
        self.write_key = write_key
        self.host = host
        self.on_error = on_error
        self.retries = retries
        self.timeout = timeout
        self.flush_interval = flush_interval

    def run(self):
        """Runs the consumer."""
        self.logger.debug('consumer is running...')
        while self.running:
            self.upload()

        self.logger.debug('consumer exited.')

    def pause(self):
        """Pause the consumer."""
        self.running = False

    def upload(self):
        queue = self.queue
        queue_msg = None
        try:
            queue_msg = queue.get(block=True, timeout=self.flush_interval)
        except Empty:
            self.logger.debug("queue is empty now")

        if not queue_msg:
            self.logger.debug("Nothing left in queue exiting")
            return False
        try:
            self.request(queue_msg=queue_msg)
            success = True
        except Exception as e:
            self.logger.error(f"Error uploading: {e}")
            success = False
            if self.on_error:
                self.on_error(e, queue_msg)
        finally:
            self.queue.task_done()
        return success

    def request(self, queue_msg):
        """Attempt to upload the queue_msg and retry before raising an error """

        def fatal_exception(exc):
            if isinstance(exc, APIError):
                # retry on server errors and client errors
                # with 429 status code (rate limited),
                # don't retry on other client errors
                return (400 <= exc.status_code < 500) and exc.status_code != 429
            else:
                # retry on all other errors (eg. network)
                return False

        @backoff.on_exception(
            backoff.expo,
            Exception,
            max_tries=self.retries + 1,
            giveup=fatal_exception)
        def send_request():
            post(write_key=self.write_key, host=self.host,
                 path=queue_msg['path'], body=queue_msg['body'], timeout=self.timeout)

        send_request()
