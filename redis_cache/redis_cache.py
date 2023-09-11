from inspect import signature, getsource, getfullargspec
from typing import Any, Callable

from .redis_client import RedisClient
from .serialize import Serialize


class RedisCache:
    """Redis cache decorator"""

    def _construct_key(
        func: Callable, args: tuple[Any, ...], kwargs: dict[str, Any], key_prefix: str
    ) -> str:
        """constructs a key for redis key-value store

        Args:
            func (Callable): decorated method
            args (tuple[Any, ...]): arguments passed to decorated method
            kwargs (dict[str, Any]): keyword arguments passed to decorated method
            key_prefix (str): prefix for redis key

        Returns:
            str: redis key
        """

        try:
            varnames = getfullargspec(func).args
        except ValueError:
            varnames = list(signature(func).parameters)

        key_vars = {
            varnames[i]: args[i] for i in range(len(args)) if i < len(args)
        } | kwargs
        arg_vars = args[len(key_vars) :] if len(args) > len(varnames) else tuple()
        soruce_code = getsource(func).replace("\n", "").replace(" ", "")

        return ",".join([key_prefix, str(key_vars), str(arg_vars), soruce_code]).strip(
            ","
        )

    @staticmethod
    def _get_result(client: RedisClient, key: str, serializer: Serialize) -> Any:
        """obtains the cahced result from redis

        Args:
            client (RedisClient): redis clinet
            key (str): redis key
            serializer (Serialize): serializer object

        Returns:
            Any: cached result
        """

        buffer = client.get(key)
        return serializer.deserialize(serializer, buffer)

    @staticmethod
    def _set_result(
        client: RedisClient,
        key: str,
        serializer: Serialize,
        func: Callable,
        args: tuple[Any],
        kwargs: dict[str, Any],
    ) -> Any:
        """sets the result of the decorated method to redis

        Args:
            client (RedisClient): redis client
            key (str): redis key
            serializer (Serialize): serializer object
            func (Callable): decorated method
            args (tuple[Any]): arguments passed to decorated method
            kwargs (dict[str, Any]): keyword arguments passed to decorated method

        Returns:
            Any: result of decorated method
        """

        result = func(*args, **kwargs)
        client.set(key, serializer.serialize(result))
        return result

    @classmethod
    def cache(
        cls,
        client: RedisClient = RedisClient(),
        timeout: int = 60,
        key_prefix: str = "",
        serialize_encoder: str = "json",
    ) -> Callable:
        """decorator for caching the result of a method

        Args:
            client (RedisClient, optional): redis client connection. Defaults to RedisClient().
            timeout (int, optional): expiry time for cache. Defaults to 60.
            key_prefix (str, optional): prefix cache key. Defaults to "".
            serialize_encoder (str, optional): serializer method (json, or pickle). Defaults to "json".

        Returns:
            Callable: decorated method
        """

        def decorator(func) -> Callable:
            def wrapper(*args, **kwargs) -> Any:
                serializer = Serialize(serialize_encoder)
                key = cls._construct_key(
                    func=func,
                    args=args,
                    kwargs=kwargs,
                    key_prefix=key_prefix,
                )

                return (
                    cls._get_result(client, key, serializer)
                    if client.exists(key)
                    else cls._set_result(client, key, serializer, func, args, kwargs)
                )

            return wrapper

        return decorator
