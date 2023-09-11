import pickle
import json
from typing import Any, Callable


class Serialize:
    """Serialize data to bytes and deserialize bytes to data"""

    def __init__(self, serialize_encoder: str = "json"):
        self.serialize_encoder = serialize_encoder

    @property
    def serializer_methods(self) -> dict[str, Callable]:
        """Available serializer methods

        Returns:
            dict[str, Callable]: Dictionary of serializer methods
        """
        return {"pickle": pickle, "json": json}

    @property
    def serialize_encoder(self) -> str:
        """Obtains the selected serializer encoding method

        Returns:
            str: Selected serializer encoding method
        """
        return self._serialize_encoder

    @serialize_encoder.setter
    def serialize_encoder(self, encode: str) -> None:
        """Sets the serializer encoding method

        Args:
            encode (str): Chosen serializer encoding method

        Raises:
            ValueError: If the chosen serializer encoding
                method is not available
        """
        if encode not in self.serializer_methods:
            raise ValueError(
                f"Serializer must be either {self.serializer_methods.keys()}"
            )
        self._serialize_encoder = encode

    def deserialize(self, buffer: bytes) -> Any:
        """Deserializes bytes based on the chosen
            serializer encoding method

        Args:
            buffer (bytes): Bytes to be deserialized

        Returns:
            Any: Deserialized bytes
        """
        serializer = self.serializer_methods.get(self.serializer)
        return serializer.loads(buffer)

    def serialize(self, data: Any) -> bytes:
        """Serializes data based on the chosen
            serializer encoding method

        Args:
            data (Any): Data to be serialized

        Returns:
            bytes: Serialized data
        """
        serializer = self.serializer_methods.get(self.serialize_encoder)
        return serializer.dumps(data)
