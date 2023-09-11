from typing import Any
from redis import Redis


class RedisClient:
    """Redis client for caching"""

    def __init__(self, host: str = "localhost", port: int = 6379, db: int = 0):
        self.redis = Redis(host=host, port=port, db=db)

    def set(self, key: str, value: Any) -> None:
        """set key value pair in redis

        Args:
            key (str): key index for value
            value (Any): value to be stored
        """

        self.redis.set(key, value)

    def get(self, key: str) -> bytes:
        """get value from redis

        Args:
            key (str): key index for value

        Returns:
            bytes: value stored in redis
        """

        return self.redis.get(key)

    def delete(self, key: str) -> None:
        """delete key value pair from redis

        Args:
            key (str): key index for value
        """

        self.redis.delete(key)

    def exists(self, key: str) -> bool:
        """check if key exists in redis

        Args:
            key (str): key index for value

        Returns:
            bool: True if key exists, False otherwise
        """

        return self.redis.exists(key)

    def expire(self, key: str, timeout: int) -> None:
        """set expiry time for key

        Args:
            key (str): key index for value
            timeout (int): expiry time in seconds
        """

        self.redis.expire(key, timeout)

    def flushdb(self) -> None:
        """delete all keys in redis"""

        self.redis.flushdb()

    def keys(self) -> list[str]:
        """get all keys in redis

        Returns:
            list[str]: list of keys in redis
        """

        return self.redis.keys()

    def __repr__(self) -> str:
        """__repr__ method

        Returns:
            str: representation of RedisClient
        """

        return ','.join([
            f"RedisClient(host={self.redis.connection_pool.connection_kwargs['host']}",
            f"port={self.redis.connection_pool.connection_kwargs['port']}",
            f"db={self.redis.connection_pool.connection_kwargs['db']})",
        ])

    def __str__(self) -> str:
        """__str__ method

        Returns:
            str: representation of RedisClient
        """

        return ','.join([
            f"RedisClient(host={self.redis.connection_pool.connection_kwargs['host']}",
            f"port={self.redis.connection_pool.connection_kwargs['port']}",
            f"db={self.redis.connection_pool.connection_kwargs['db']})",
        ])