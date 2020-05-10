from .abstract_result import AbstractResult, AbstractResultCodec


class ResultRedirect(AbstractResult):
    ...


class ResultRedirectCodec(AbstractResultCodec[ResultRedirect]):
    ...
