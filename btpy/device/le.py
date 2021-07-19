from asyncio import get_event_loop

from btpy.device import Device

from bleak import discover

_le_scan_ret = []


class LEDevice(Device):
    @staticmethod
    def scan(duration: int = 3):
        _le_scan_ret = []

        async def run():
            global _le_scan_ret
            _le_scan_ret = discover()

        get_event_loop().run_until_complete(run())

        r = _le_scan_ret.copy()
        return r
