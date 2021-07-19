## btpy
this is a wrapper around
- [bleak](https://github.com/hbldh/bleak) for low-energy support
- [beacontools](https://github.com/citruz/beacontools) for beacon support
- [bluez](http://www.bluez.org/) for classic support

### how to ...
#### .. install
```shell
pip3 install btpy
# or (this is not guaranteed to be stable)
pip3 install git+https://github.com/nbdy/btpy
```

#### ... to use it
```python
from btpy import LEDevice, Beacon, ClassicDevice

le_results = LEDevice.scan(4)

beacon_results = Beacon.scan(5)

classic_results = ClassicDevice.scan(6)
```

##### TODO
- [ ] Tests