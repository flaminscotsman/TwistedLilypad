from .abstract_request import AbstractRequest, AbstractRequestCodec


class RequestGetDetails(AbstractRequest):
    ...


class RequestGetDetailsCodec(AbstractRequestCodec[RequestGetDetails]):
    @staticmethod
    def encode(request: RequestGetDetails) -> bytes:
        ...

    @staticmethod
    def decode(payload: bytes) -> RequestGetDetails:
        ...

