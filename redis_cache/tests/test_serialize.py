import pytest

from redis_cache.serialize import Serialize

def test_serialize_json():

    json_serialize = Serialize(serialize_encoder='json')
    deserialised_object = {'foo': 'bar'}
    serialised_object = b'\x80\x04\x95\x0b\x00\x00\x00\x00\x00\x00\x00}\x94\x8c\x03foo\x94\x8c\x03bar\x94s.'
    assert json_serialize.serialize(deserialised_object) == serialised_object
    assert json_serialize.deserialize(serialised_object) == deserialised_object


def test_serialize_pickle():

    pickle_serialize = Serialize(serialize_encoder='pickle')
    deserialised_object = {'foo': 'bar'}
    serialised_object = b'\x80\x04\x95\x0b\x00\x00\x00\x00\x00\x00\x00}\x94\x8c\x03foo\x94\x8c\x03bar\x94s.'
    assert pickle_serialize.serialize(deserialised_object) == serialised_object
    assert pickle_serialize.deserialize(serialised_object) == deserialised_object


def test_serialize_invalid_serializer():

    with pytest.raises(ValueError):
        Serialize(serialize_encoder='invalid_serializer')
    
def test_serialize_setter():

    serialize = Serialize('json')
    assert serialize.serialize_encoder == 'json'
    serialize = Serialize('pickle')
    assert serialize.serialize_encoder == 'pickle'
    
    