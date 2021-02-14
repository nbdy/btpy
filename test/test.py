from time import sleep
import bluetooth
from bluetooth.ble import DiscoveryService, GATTRequester


def ble():
    s = DiscoveryService()
    
    devs = s.discover(2)

    for a, n in devs.items():
        print(a, n)
        g.connect(True)


def main():
    devs = bluetooth.discover_devices(duration=5, lookup_names=True,
                                      flush_cache=True)

    for a, n in devs:
        print(a, n)
        for i in  bluetooth.find_service(address=a):
            print(i["protocol"], i["port"])
            if i["protocol"] == "RFCOMM":
                s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
                s.connect((i["host"], i["port"]))
                s.send("AT")
                print(s.recv(128))
                s.close()
            elif i["protocol"] == "L2CAP":
                s = bluetooth.BluetoothSocket(bluetooth.L2CAP)
                s.connect((i["host"], i["port"]))
                s.send("AT")
                print(s.recv(128))
                s.close()


if __name__ == '__main__':
    main()
    # ble()
