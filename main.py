

from cache.cache import cache

boo = {'boo': 'bar'}

@cache(timeout=60, key_prefix='test', serializer=None)
def select(key):
    ... 
    return boo.get(key)


o = select('boo', cache=False)

print(o)

