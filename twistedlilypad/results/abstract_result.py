class AbstractResult(object):
    opcode = -1


class AbstractResultCodec(object):
    @staticmethod
    def decode(payload):
        raise NotImplementedError

    @staticmethod
    def encode(packet):
        raise NotImplementedError