import datetime
import logging
import uuid
from sys import stdout
from time import sleep

import redis

HOST = 'redis-master.default.svc.cluster.local'
# HOST = 'localhost'
PORT = 6379
TOTAL_CONNECTION_ATTEMPTS = 5
LOCK_STATUS_KEY = 'lock_key'

logging.basicConfig(stream=stdout, format="%(asctime)s - %(filename)s:%(lineno)d: %(message)s")
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

error_logger = logging.getLogger(__name__)
error_logger.setLevel(logging.ERROR)


class RedisClient:
    def __init__(self):
        self._client_uuid = str(uuid.uuid4())
        self._redis_client = None

        self.connect_to_server()

        if self._redis_client is not None:
            logger.info('Connected to redis')

    def _is_connection_healthy(self):
        if self._redis_client is None:
            error_logger.error('Redis client not connected to server')
            self.connect_to_server()

            if self._redis_client is None:
                return False

        return True

    def connect_to_server(self):
        attempts = 0
        time_to_wait = 1

        while self._redis_client is None and attempts < TOTAL_CONNECTION_ATTEMPTS:
            try:
                self._redis_client = redis.Redis(host=HOST, port=PORT)
                logger.info(self._redis_client.ping())
            except Exception as e:
                error_logger.error('Error connecting to redis server', e)

            attempts += 1
            sleep(time_to_wait)
            time_to_wait += 3

    def acquire_lock(self, max_timeout=1):
        start_time = datetime.datetime.now()
        time_to_sleep = 1

        while start_time + datetime.timedelta(hours=max_timeout) > datetime.datetime.now():
            lock_status = self._redis_client.get(LOCK_STATUS_KEY)
            if lock_status is None:
                self._redis_client.set(LOCK_STATUS_KEY, self._client_uuid)
                return True
            sleep(time_to_sleep)
            time_to_sleep += 3

        return False

    def release_lock(self):
        attempts = 0
        time_to_wait = 1

        while attempts < 3:
            try:
                self._redis_client.delete(LOCK_STATUS_KEY)
                return
            except Exception as e:
                error_logger.error(f'Error while deleting redis key for UUID: {self._redis_client}')

            attempts += 1
            sleep(time_to_wait)
            time_to_wait += 3

    def set_data(self, key, value):
        if not self._is_connection_healthy():
            return False

        try:
            self._redis_client.set(key, value)
            return True
        except Exception as e:
            error_logger.error(f'Not able to set {key} : {value}', e)

        return False

    def get_data(self, key):
        if not self._is_connection_healthy():
            return False

        try:
            value = self._redis_client.get(key)
            if value is not None:
                return int(value)

            return value
        except Exception as e:
            error_logger.error(f'Not able to find value for {key}')

        return None

# r = RedisClient()
# r.set_data('NAME1', 10)
# print(r.get_data('NAME1'))
# print(r.get_data('ABC'))
