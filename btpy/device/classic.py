from btpy.device import Device
from bluetooth import discover_devices, find_service


class Service(object):
    name = None
    protocol = None
    port = None
    description = None
    profiles = None
    service_classes = None
    provider = None
    service_id = None

    def __init__(self, service):
        self.name = service["name"]
        self.protocol = service["protocol"]
        self.port = service["port"]
        self.description = service["description"]
        self.profiles = service["profiles"]
        self.service_classes = service["service-classes"]
        self.provider = service["provider"]
        self.service_id = service["service-id"]

    @staticmethod
    def found_to_list(services):
        r = []
        for s in services:
            r.append(Service(s))
        return r


class ClassicDevice(Device):
    name = None
    services = []

    def __init__(self, address, name=None):
        Device.__init__(self, address)
        self.name = name

    @staticmethod
    def scan(duration: int = 3, lookup_names: bool = True, lookup_class: bool = False):
        return ClassicDevice.found_to_list(discover_devices(duration, lookup_names=lookup_names, lookup_class=lookup_class))

    def get_services(self):
        self.services = Service.found_to_list(find_service(address=self.address))

    def to_dict(self):
        services = []
        for s in self.services:
            services.append(s.__dict__)
        d = self.__dict__
        d["services"] = services
        return d

    @staticmethod
    def found_to_list(devices):
        devs = []
        for device in devices:
            devs.append(ClassicDevice(device[0], device[1]))
        return devs
