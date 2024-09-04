from __future__ import annotations

from typing import Optional

from bluetooth import discover_devices, find_service

from btpy.device import Device


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
    def found_to_list(services:  list[dict[str, list | None]]) -> list[Service]:
        return [Service(s) for s in services]


class ClassicDevice(Device):
    name: str = None
    services: list[Service] = []

    def __init__(self, address: str, name: Optional[str] = None):
        Device.__init__(self, address)
        self.name = name

    @staticmethod
    def found_to_list(devices: list[tuple[str, str]]) -> list[ClassicDevice]:
        return [ClassicDevice(device[0], device[1]) for device in devices]

    @staticmethod
    def scan(duration: int = 3, lookup_names: bool = True, lookup_class: bool = False) -> list[ClassicDevice]:
        return ClassicDevice.found_to_list(
            discover_devices(duration, lookup_names=lookup_names, lookup_class=lookup_class)
        )

    def get_services(self) -> list[Service]:
        return Service.found_to_list(find_service(address=self.address))
