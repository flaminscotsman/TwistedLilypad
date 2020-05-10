from .abstract_result import AbstractResult, AbstractResultCodec


class ResultGetDetails(AbstractResult):
    def __init__(self, ip: str, port: int, motd: str, version: str):
        self.ip = ip
        self.port = port
        self.motd = motd
        self.version = version


class ResultGetDetailsCodec(AbstractResultCodec[ResultGetDetails]):
    ...
