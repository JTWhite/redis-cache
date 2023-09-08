import json
import pickle 

from .redis_client import RedisClient

rc = RedisClient()


class RedisCache:


    


def construct_key(key_prefix: str, key: str):
    return '-'.join([key_prefix, key]).strip('-')

def deserialize(serializer: str, buffer: bytes):

    if serializer == 'json':
        return json.loads(buffer)
    elif serializer == 'pickle':
        return pickle.loads(buffer)
    return buffer

def serialize(serializer: str, data):
    if serializer == 'json':
        return json.dumps(data)
    elif serializer == 'pickle':
        return pickle.dumps(data)
    return data


def cache(timeout: int, key_prefix: str='', serializer: str='json'):
    def decorator(func):
        def wrapper(*args, **kwargs):

            # construct key from args
            key = construct_key(
                key_prefix=key_prefix,
                key = kwargs.get('key') if 'key' in kwargs else args[0],
            )

            # TODO GET KEYS FROM QUERIES... OR VARIOUS OTHER INPUTS
            
            #check if query cached
            if rc.exists(key):
                print('cache exists')
                buffer = rc.get(key)
                return deserialize(serializer, buffer)
                
            else:
                print('cache does not exist')
                #get data from sql db and cache it
                result = func(*args, **kwargs)
                rc.set(key, serialize(serializer, result))
            return result
        return wrapper
    return decorator