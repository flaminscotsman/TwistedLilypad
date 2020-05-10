from typing import Generic, TypeVar

class AbstractRequest(object):
    opcode: int


T = TypeVar('T', bound=AbstractRequest)


class AbstractRequestCodec(Generic[T]):
    @staticmethod
    def decode(payload: bytes) -> T:
        ...

    @staticmethod
    def encode(request: T) -> bytes:
        ...
