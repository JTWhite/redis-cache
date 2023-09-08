from inspect import signature, getsource, getfullargspec
from typing import Any, Callable, Optional

from .redis_client import RedisClient
from .serialize import Serialize


class RedisCache:
    def _construct_key(
        func: Callable, args: tuple[Any, ...], kwargs: dict[str, Any], key_prefix: str
    ) -> str:
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
    def _get_result(client, key: str, serializer) -> Any:
        buffer = client.get(key)
        return serializer.deserialize(serializer, buffer)

    @staticmethod
    def _set_result(client, key: str, serializer, func, args, kwargs) -> Any:
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
    ):
        def decorator(func):
            def wrapper(*args, **kwargs):
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
