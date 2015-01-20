import hashlib


def _sha1Hex(string):
    return hashlib.sha1(string).hexdigest()


def saltPassword(password, salt):
    return _sha1Hex(_sha1Hex(salt) + _sha1Hex(password))