from sys import argv
from os.path import isdir
from os import makedirs
from atexit import register
from datetime import datetime

from btpy.libs.bt.le import LEDevice
from btpy.libs.Static import Static
from btpy.libs.bt.beacon import Beacon
from btpy.libs.bt.classic import ClassicDevice


class Scanner(object):
    _do_run = False
    out = "out/"
    duration = 5

    def ctrl_c(self):
        self._do_run = False

    @staticmethod
    def scan(le=True, beacon=True, classic=True):
        devs = []
        if le:
            devs += LEDevice.scan(read_all=True)
        if classic:
            devs += ClassicDevice.scan()
        if beacon:
            devs += Beacon.scan()
        return devs

    @staticmethod
    def scan_until_found(le=True, beacon=True, classic=True):
        devs = []
        while len(devs) == 0:
            devs = Scanner.scan(le, beacon, classic)
        return devs

    @staticmethod
    def scan_for(seconds=10, le=True, beacon=True, classic=True):
        devs = []
        t = datetime.now()
        while (datetime.now() - t).microseconds < (seconds * 1000):
            devs += Scanner.scan(le, beacon, classic)
        return devs

    def __init__(self):
        register(self.ctrl_c)
        self.parse_args()
        self.check_args()
        self._do_run = True

    def check_args(self):
        if not isdir(self.out):
            makedirs(self.out)
            print("created directory", self.out)
        if self.duration < 1 or self.duration > 20:
            print("scan duration of", str(self.duration), "seems off")

    def parse_args(self):
        i = 0
        while i < len(argv):
            if argv[i] == "-o" or argv[i] == "--out":
                self.out = argv[i + 1]
            elif argv[i] == "-d" or argv[i] == "--duration":
                self.duration = int(argv[i + 1])
            elif argv[i] == "--help":
                print("usage: python", __file__, "{arguments}")
                for ak in self.__dict__.keys():
                    if not ak.startswith('_'):
                        print("-" + ak[0], "\t", "--" + ak)
                exit()
            i += 1

    @staticmethod
    def print_devices(devices):
        for dev in devices:
            if isinstance(dev, ClassicDevice):
                dev.get_services()
                print("-" * 42)
                print("classic", dev.address, dev.name)
                print("\tservices:", len(dev.services))
            if isinstance(dev, Beacon):
                print("-" * 42)
                print("beacon", dev.address, dev.power, dev.rssi)
            if isinstance(dev, LEDevice):
                print("-" * 42)
                print("le", dev.address, dev.name)
                print("\tservices:", len(dev.services), "\tads:", len(dev.advertisements))

    def run(self):
        print("running")
        while self._do_run:
            devices = self.scan_until_found()
            Scanner.print_devices(devices)
            Static.save_multiple(devices, self.out)


if __name__ == '__main__':
    Scanner().run()
