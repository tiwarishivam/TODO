from todoapp.redis import RedisCache


def set_redis(key, value, timeout=None):  # for setting key value in Redis
    redis = RedisCache()

    return redis.set_key(key, value, timeout)


def get_redis(key):   # for getting value from Redis
    redis = RedisCache()

    return redis.get_key(key)
