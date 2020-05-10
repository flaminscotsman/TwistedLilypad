from typing import Iterable

def varint_encoder(number: int) -> bytes:
    ...


def varint_prefixed_string_encoder(string: str) -> bytes:
    ...


def varint_prefixed_string_list_encoder(string_list: Iterable[str]) -> bytes:
    ...


def boolean_encoder(boolean: bool) -> bytes:
    ...
