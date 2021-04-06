from argparse import ArgumentParser

from btpy.LEDevice import LEDevice
from btpy.ClassicDevice import ClassicDevice


def main():
    ap = ArgumentParser()
    ap.add_argument("-c", "--classic", help="Scan classic", action="store_true")
    ap.add_argument("-l", "--low-energy", help="LE scan", action="store_true")
    a = ap.parse_args()

    if not a.classic and not a.low_energy:
        print("Mkay")
        exit()

    if a.classic:
        print("Classic scan")
        ClassicDevice.scan()

    if a.low_energy:
        print("LE scan")
        LEDevice.scan()


if __name__ == "__main__":
    main()
