import pickle
import json
from typing import Any


class Serialize:
    def __init__(self, serialize_encoder: str = "json"):
        self.serialize_encoder = serialize_encoder

    @property
    def serializer_methods(self) -> dict[str, callable]:
        return {"pickle": pickle, "json": json}

    @property
    def serialize_encoder(self):
        return self._serialize_encoder

    @serialize_encoder.setter
    def serialize_encoder(self, encode: str):
        if encode not in self.serializer_methods:
            raise ValueError(
                f"Serializer must be either {self.serializer_methods.keys()}"
            )
        self._serialize_encoder = encode

    def deserialize(self, buffer: bytes) -> Any:
        serializer = self.serializer_methods.get(self.serializer)
        return serializer.loads(buffer)

    def serialize(self, data) -> bytes:
        serializer = self.serializer_methods.get(self.serialize_encoder)
        return serializer.dumps(data)
