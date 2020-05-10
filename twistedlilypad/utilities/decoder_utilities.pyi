from typing import Tuple


def varint_parser(data: bytes) -> Tuple[int, bytes]:
    ...


def varint_parser_with_length(data: bytes) -> Tuple[int, bytes, int]:
    ...


def varint_prefixed_string_parser(data: bytes) -> Tuple[str, bytes]:
    ...
