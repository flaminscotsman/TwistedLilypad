from .abstract_result import AbstractResult, AbstractResultCodec


class ResultAsServer(AbstractResult):
    ...


class ResultAsServerCodec(AbstractResultCodec[ResultAsServer]):
    ...
