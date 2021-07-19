from argparse import ArgumentParser
from pprint import pprint

from btpy import LEDevice
from btpy import Beacon
from btpy import ClassicDevice


def main():
    ap = ArgumentParser()
    ap.add_argument("-le", "--low-energy", help="scan for low energy devices", action="store_true")
    ap.add_argument("-c", "--classic", help="scan for classic devices", action="store_true")
    ap.add_argument("-b", "--beacon", help="scan for beacons", action="store_true")
    ap.add_argument("-d", "--duration", help="scan timeout", type=int, default=4)
    a = ap.parse_args()

    results = []

    if a.low_energy:
        results += LEDevice.scan(a.duration)

    if a.classic:
        results += ClassicDevice.scan(a.duration)

    if a.beacon:
        results += Beacon.scan(a.duration)

    for result in results:
        pprint(result.__dict__)
