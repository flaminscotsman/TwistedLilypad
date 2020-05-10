class AbstractPacket(object):
    opcode = -1


class AbstractPacketCodec(object):
    @staticmethod
    def decode(payload):
        raise NotImplementedError

    @staticmethod
    def encode(packet):
        raise NotImplementedError


class StatusCode:
    SUCCESS = 0x00
    ERROR_GENERIC = 0x01
    ERROR_ROLE = 0x02

    @classmethod
    def pprint(cls, code):
        if code == cls.SUCCESS:
            return 'SUCCESS'
        elif code == cls.ERROR_GENERIC:
            return 'ERROR_GENERIC'
        elif code == cls.ERROR_ROLE:
            return 'ERROR_ROLE'
        else:
            return 'unknown status code'