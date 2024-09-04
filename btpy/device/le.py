from __future__ import annotations

from asyncio import get_event_loop, new_event_loop, set_event_loop

from bleak import BleakScanner, BLEDevice, AdvertisementData

from btpy.device import Device

_le_scan_event_loop = None


def _create_event_loop():
    global _le_scan_event_loop
    if _le_scan_event_loop is None:
        _le_scan_event_loop = new_event_loop()
        set_event_loop(_le_scan_event_loop)


class LEDevice(Device):
    name: str
    rssi: int

    def __init__(self, address: str, name: str, rssi: int):
        Device.__init__(self, address)
        self.name = name
        self.rssi = rssi

    @staticmethod
    def scan(duration: int = 3) -> list[LEDevice]:
        _create_event_loop()
        ret = []

        async def callback(device: BLEDevice, data: AdvertisementData):
            ret.append(LEDevice(device.address, device.name, device.rssi))

        async def run(d: int):
            scanner = BleakScanner(callback)
            await scanner.discover(d)

        get_event_loop().run_until_complete(run(duration))

        return ret
