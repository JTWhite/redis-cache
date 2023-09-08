from redis import Redis


class RedisClient:
    def __init__(self, host="localhost", port=6379, db=0):
        self.redis = Redis(host=host, port=port, db=db)

    def set(self, key, value):
        self.redis.set(key, value)

    def get(self, key):
        return self.redis.get(key)

    def delete(self, key):
        self.redis.delete(key)

    def exists(self, key):
        return self.redis.exists(key)

    def expire(self, key, timeout):
        self.redis.expire(key, timeout)

    def flushdb(self):
        self.redis.flushdb()

    def keys(self):
        return self.redis.keys()

    def __repr__(self):
        return f"RedisClient(host={self.redis.connection_pool.connection_kwargs['host']}, port={self.redis.connection_pool.connection_kwargs['port']}, db={self.redis.connection_pool.connection_kwargs['db']})"

    def __str__(self):
        return f"RedisClient(host={self.redis.connection_pool.connection_kwargs['host']}, port={self.redis.connection_pool.connection_kwargs['port']}, db={self.redis.connection_pool.connection_kwargs['db']})"
