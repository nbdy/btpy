from ..Device import Device
from ..Service import Service
from bluetooth import discover_devices, find_service


class ClassicDevice(Device):
    name = None
    services = []

    def __init__(self, address, name=None):
        Device.__init__(self, address)
        self.name = name

    @staticmethod
    def scan(duration=3):
        return ClassicDevice.found_to_list(discover_devices(duration=duration,
                                                            lookup_names=True))

    def get_services(self):
        self.services = Service.found_to_list(find_service(address=self.address))

    def to_dict(self):
        servs = []
        for s in self.services:
            servs.append(s.__dict__)
        d = self.__dict__
        d["services"] = servs
        return d

    @staticmethod
    def found_to_list(devices):
        devs = []
        for device in devices:
            devs.append(ClassicDevice(device[0], device[1]))
        return devs
