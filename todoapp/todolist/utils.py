from todoapp.redis import RedisCache


def set_redis(key, value, timeout=None):
    redis = RedisCache()

    return redis.set_key(key, value, timeout)


def get_redis(key):
    redis = RedisCache()

    return redis.get_key(key)
