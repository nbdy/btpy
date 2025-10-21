# btpy

A comprehensive Python library for Bluetooth communication, providing unified interfaces for Bluetooth Low Energy (BLE), Classic Bluetooth, and Beacon devices.

## Features

- **Bluetooth Low Energy (BLE)**: Scan and interact with BLE devices using [bleak](https://github.com/hbldh/bleak)
- **Beacon Support**: Detect and parse beacon advertisements using [beacontools](https://github.com/citruz/beacontools)
- **Classic Bluetooth**: Work with classic Bluetooth devices via [bumble](https://github.com/google/bumble)
- **Simple API**: Easy-to-use interface for common Bluetooth operations
- **Cross-platform**: Works on Linux, macOS, and Windows (where supported by underlying libraries)

## Requirements

- Python >= 3.10
- Compatible operating system (Linux, macOS, or Windows)

## Installation

### Using pip

```shell
pip3 install btpy
```

### Using uv

```shell
uv pip install btpy
```

Or add to your project:

```shell
uv add btpy
```

## Usage

The library provides three main device classes for different Bluetooth types:

### Scanning for BLE Devices

```python
from btpy import LEDevice

# Scan for BLE devices for 4 seconds
le_results = LEDevice.scan(4)
```

### Scanning for Beacons

```python
from btpy import Beacon

# Scan for beacons for 5 seconds
beacon_results = Beacon.scan(5)
```

### Scanning for Classic Bluetooth Devices

```python
from btpy import ClassicDevice

# Scan for classic Bluetooth devices for 6 seconds
classic_results = ClassicDevice.scan(6)
```

### Combined Example

```python
from btpy import LEDevice, Beacon, ClassicDevice

# Perform all scans
le_results = LEDevice.scan(4)
beacon_results = Beacon.scan(5)
classic_results = ClassicDevice.scan(6)

print(f"Found {len(le_results)} BLE devices")
print(f"Found {len(beacon_results)} beacons")
print(f"Found {len(classic_results)} classic devices")
```

## Documentation

For more detailed documentation, please visit the [Wiki](https://github.com/nbdy/btpy/wiki).

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests on the [GitHub repository](https://github.com/nbdy/btpy).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## TODO

- [ ] Add comprehensive tests