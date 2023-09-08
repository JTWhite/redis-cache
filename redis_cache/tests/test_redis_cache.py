from .. import RedisCache


def test_construct_key():
    def foo(a, b, c):
        return a + b + c

    foo_key = "test,{'a':1,'b':2,'c':3},(),deffoo(a,b,c):returna+b+c"
    assert RedisCache._construct_key(foo, (1, 2, 3), {}, "test") == foo_key
