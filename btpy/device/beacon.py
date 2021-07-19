from time import sleep
from typing import List

from btpy.device import Device

from beacontools import BeaconScanner


class Beacon(Device):
    rssi: int
    packet: any
    extra_info: any

    def __init__(self, address: str, rssi: int, packet, extra_info):
        Device.__init__(self, address)
        self.rssi = rssi
        self.packet = packet
        self.extra_info = extra_info

    @staticmethod
    def scan(duration: int = 3) -> List[Device]:
        r = []

        def callback(address, rssi, packet, additional_info):
            r.append(Beacon(address, rssi, packet, additional_info))

        scanner = BeaconScanner(callback)
        scanner.start()
        sleep(duration)
        scanner.stop()
        return r
