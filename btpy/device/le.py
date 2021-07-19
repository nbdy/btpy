from asyncio import get_event_loop, new_event_loop, set_event_loop

from btpy.device import Device

from bleak import discover

_le_scan_ret = []
_le_scan_event_loop = None


class LEDevice(Device):
    @staticmethod
    def scan(duration: int = 3):
        global _le_scan_event_loop
        if _le_scan_event_loop is None:
            _le_scan_event_loop = new_event_loop()
            set_event_loop(_le_scan_event_loop)

        _le_scan_ret = []

        async def run():
            global _le_scan_ret
            _le_scan_ret = await discover()

        get_event_loop().run_until_complete(run())

        r = _le_scan_ret.copy()
        return r
