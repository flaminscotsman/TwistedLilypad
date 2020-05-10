from .abstract_result import AbstractResult, AbstractResultCodec


class ResultMessage(AbstractResult):
    ...


class ResultMessageCodec(AbstractResultCodec[ResultMessage]):
    ...
