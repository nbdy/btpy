from .Static import Static


class Device(object):
    address = None
    timestamp = None

    def __init__(self, address):
        self.address = address
        self.timestamp = Static.make_timestamp()

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def scan(duration):
        return []
