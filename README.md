# Redis Cache 


## Description
This is a simple Redis Cache implementation using Python and Redis.

## Requirements
- Python 3.6+
- Redis 5.0+

## Installation
- Clone this repository
- Install the requirements
- Run the application

## Usage

For basic usage, you can use the decorator `@RedisCache.cache` to cache the return of a function.

```python
from redis_cache import RedisCache

@RedisCache.cache(timeout=60)
def get_data() -> str:
    return "Hello World"
```

By default, the cache uses a json serializer, but for more complex object you have the option to choose better json or pickle serializers.

```python
class Student:
    def __init__(self, name, age):
        self.name: str = name
        self.age: int = age

@RedisCache.cache(timeout=60, serializer='pickle')
def get_data(name: str, age: int) -> str:
    return Student(name, 20)
```

