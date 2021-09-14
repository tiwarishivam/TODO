import traceback
import logging

from django.core.cache import caches

logger = logging.getLogger(__name__)


class RedisCache(object):
    def __init__(self):
        self.DEFAULT_TIMEOUT = 60*60*60
        self.cache = caches['default']

    def get_key(self, key):
        try:
            val = self.cache.get(key)
            return 200, val
        except Exception as e:
            print(traceback.format_exc())
            logger_error.error("Error is: \n{}".format(traceback.format_exc()))
            return 500, None

    def set_key(self, key, value, timeout=None):
        if not timeout:
            timeout = self.DEFAULT_TIMEOUT
        try:
            self.cache.set(key, value, timeout)
            return 200, None
        except Exception as e:
            print(traceback.format_exc())
            logger_error.error("Error is: \n{}".format(traceback.format_exc()))
            return 500, None

    def has_key(self, key):
        try:
            is_there = self.cache.has_key(key)
            return 200, is_there
        except Exception as e:
            print(traceback.format_exc())
            logger.error("Error is: \n{}".format(traceback.format_exc()))
            return 500, None