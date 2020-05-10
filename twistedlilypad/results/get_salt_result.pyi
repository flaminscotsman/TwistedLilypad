from .abstract_result import AbstractResult, AbstractResultCodec


class ResultGetSalt(AbstractResult):
    def __init__(self, salt: str):
        self.salt = salt


class ResultGetSaltCodec(AbstractResultCodec[ResultGetSalt]):
    ...
