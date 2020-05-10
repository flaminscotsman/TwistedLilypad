from .abstract_result import AbstractResult, AbstractResultCodec


class ResultAsProxy(AbstractResult):
    ...


class ResultAsProxyCodec(AbstractResultCodec[ResultAsProxy]):
    ...
