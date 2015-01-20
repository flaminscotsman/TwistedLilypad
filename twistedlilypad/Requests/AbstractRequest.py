class AbstractRequest(object):
    opcode = -1


class AbstractRequestCodec(object):
    @staticmethod
    def decode(payload):
        raise NotImplementedError

    @staticmethod
    def encode(packet):
        raise NotImplementedError