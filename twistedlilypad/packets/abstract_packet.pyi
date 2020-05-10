from typing import Generic, TypeVar


class AbstractPacket:
    opcode: int


T = TypeVar('T', bound=AbstractPacket)


class AbstractPacketCodec(Generic[T]):
    @staticmethod
    def decode(payload: bytes) -> T:
        ...

    @staticmethod
    def encode(packet: T) -> bytes:
        ...


class StatusCode:
    SUCCESS = 0x00
    ERROR_GENERIC = 0x01
    ERROR_ROLE = 0x02

    @classmethod
    def pprint(cls, code: StatusCode):
        ...
