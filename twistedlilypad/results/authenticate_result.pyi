from .abstract_result import AbstractResult, AbstractResultCodec


class ResultAuthenticate(AbstractResult):
    ...


class ResultAuthenticateCodec(AbstractResultCodec[ResultAuthenticate]):
    ...
