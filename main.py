

from redis_cache import RedisCache

from redis_cache.serialize import Serialize




boo = {'boo': 'bar'}

@RedisCache.cache(timeout=60, key_prefix='test', serialize_encoder='json')
def select(key):
    ... 
    return boo.get(key)


o = select('boo')

print(o)

