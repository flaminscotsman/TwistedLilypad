from typing import Generic, TypeVar

class AbstractResult(object):
    opcode: int


T = TypeVar('T', bound=AbstractResult)

class AbstractResultCodec(Generic[T]):
    @staticmethod
    def decode(payload: bytes) -> T:
        ...

    @staticmethod
    def encode(packet: T) -> bytes:
        ...
