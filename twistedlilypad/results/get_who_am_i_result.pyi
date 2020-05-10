from .abstract_result import AbstractResult, AbstractResultCodec


class ResultGetWhoAmI(AbstractResult):
    def __init__(self, identifier: str):
        self.identifier = identifier


class ResultGetWhoAmICodec(AbstractResultCodec[ResultGetWhoAmI]):
    ...
