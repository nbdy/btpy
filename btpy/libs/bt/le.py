from ..Device import Device
try:
    from bluepy.btle import Scanner, DefaultDelegate, Peripheral, BTLEException, BTLEManagementError
except ImportError:
    print("you need some https://github.com/IanHarvey/bluepy")
    print("pip3 install bluepy")
    exit()


class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, is_new_device, is_new_data):
        if is_new_device:
            pass
        if is_new_data:
            pass


class Advertisement(object):
    ad_type = None
    description = None
    value = None

    def __init__(self, **kwargs):
        if "ad_type" in kwargs.keys():
            self.ad_type = kwargs.get("ad_type")
        if "description" in kwargs.keys():
            self.description = kwargs.get("description")
        if "desc" in kwargs.keys():
            self.description = kwargs.get("desc")
        if "val" in kwargs.keys():
            self.value = kwargs.get("val")
        if "value" in kwargs.keys():
            self.value = kwargs.get("value")


class Service(object):
    uuid = None
    name = None
    characteristics = None

    def __init__(self, **kwargs):
        if "uuid" in kwargs.keys():
            self.uuid = kwargs.get("uuid")
        if "characteristics" in kwargs.keys():
            self.characteristics = kwargs.get("characteristics")
        else:
            self.characteristics = []
        if "name" in kwargs.keys():
            self.name = kwargs.get("name")

    @staticmethod
    def from_device(address, addr_type):
        try:
            services = []
            device = Peripheral(address, addr_type)
            for s in device.getServices():
                services.append(Service(
                    uuid=str(s.uuid),
                    name=s.uuid.getCommonName(),
                    characteristics=Characteristic.from_service(s)
                ))
            return services
        except BTLEException:
            print(address, "disconnected. could not read services")
            return []

    def to_dict(self):
        chars = []
        for c in self.characteristics:
            chars.append(c.__dict__)
        s = self.__dict__
        s["characteristics"] = chars
        return s


class Characteristic(object):
    uuid = None
    name = None
    data = None
    handle = None
    properties = None

    def __init__(self, **kwargs):
        if "data" in kwargs.keys():
            self.data = kwargs.get("data")
        if "uuid" in kwargs.keys():
            self.uuid = kwargs.get("uuid")
        if "properties" in kwargs.keys():
            self.properties = kwargs.get("properties")
        if "name" in kwargs.keys():
            self.name = kwargs.get("name")
        if "handle" in kwargs.keys():
            self.handle = kwargs.get("handle")

    @staticmethod
    def from_service(service):
        chars = []
        if service is None:
            return chars
        for c in service.getCharacteristics():
            chars.append(Characteristic(
                supportsRead=c.supportsRead(),
                properties=c.properties,
                uuid=str(c.uuid),
                name=c.uuid.getCommonName(),
                handle=c.getHandle()
            ))
        return chars


class LEDevice(Device):
    name = None
    addressType = None
    rssi = None
    connectable = False
    advertisements = None
    services = None

    def __init__(self, address, name=""):
        Device.__init__(self, address)
        self.name = name
        self.advertisements = []
        self.services = []

    @staticmethod
    def read_services(device):
        if not isinstance(device, LEDevice):
            return device
        try:
            p = Peripheral(device.address, device.addressType)
            for s in device.services:
                for c in s.characteristics:
                    c.data = p.readCharacteristic(c.handle)
        except BTLEException:
            print("could not connect to", device.address)
            pass
        return device

    @staticmethod
    def read_characteristics(device, characteristics):
        try:
            p = Peripheral(device.address, device.addressType)
            for c in characteristics:
                c.data = p.readCharacteristic(c.handle)
        except BTLEException:
            print("could not connect to", device.address)
            pass
        return characteristics

    @staticmethod
    def found_to_list(devices, read_all=False):
        devs = []
        for d in devices:
            _ = LEDevice(d.addr)
            _.addressType = d.addrType
            _.rssi = d.rssi
            _.connectable = d.connectable
            for (at, _d, v) in d.getScanData():
                if _d == "Complete Local Name" or _d == "Short Local Name":
                    _.name = v
                _.advertisements.append(Advertisement(ad_type=at, desc=_d, val=v))
            if _.connectable:
                _.services = Service.from_device(_.address, _.addressType)
                if read_all:
                    _ = LEDevice.read_services(_)
            devs.append(_)
        return devs

    @staticmethod
    def scan(duration=3.0, read_all=False):
        try:
            s = Scanner().withDelegate(ScanDelegate())
            return LEDevice.found_to_list(s.scan(duration), read_all)
        except BTLEManagementError as e:
            print(e.emsg)
            pass
        return []

    def to_dict(self):
        ads = []
        servs = []
        for s in self.services:
            servs.append(s.to_dict())
        for a in self.advertisements:
            ads.append(a.__dict__)
        d = self.__dict__
        d["advertisements"] = ads
        d["services"] = servs
        return d
