from __future__ import annotations

import asyncio
from typing import Optional

from bumble.device import Device as BumbleDevice
from bumble.transport import open_transport_or_link
from bumble.sdp import Client as SdpClient, DataElement
from bumble.core import BT_BR_EDR_TRANSPORT

from btpy.device import Device


class Service(object):
    name = None
    protocol = None
    port = None
    description = None
    profiles = None
    service_classes = None
    provider = None
    service_id = None

    def __init__(self, service):
        self.name = service["name"]
        self.protocol = service["protocol"]
        self.port = service["port"]
        self.description = service["description"]
        self.profiles = service["profiles"]
        self.service_classes = service["service-classes"]
        self.provider = service["provider"]
        self.service_id = service["service-id"]

    @staticmethod
    def found_to_list(services:  list[dict[str, list | None]]) -> list[Service]:
        return [Service(s) for s in services]


class ClassicDevice(Device):
    name: str = None
    services: list[Service] = []

    def __init__(self, address: str, name: Optional[str] = None):
        Device.__init__(self, address)
        self.name = name

    @staticmethod
    def found_to_list(devices: list[tuple[str, str]]) -> list[ClassicDevice]:
        return [ClassicDevice(device[0], device[1]) for device in devices]

    @staticmethod
    def scan(duration: int = 3, lookup_names: bool = True, lookup_class: bool = False, 
             transport_name: str = 'btpy', transport_mac: str = '02:00:00:00:00:00') -> list[ClassicDevice]:
        """Scan for Classic Bluetooth devices using Bumble."""
        async def _scan():
            devices = []
            
            # Open a transport (use usb:0 or any available transport)
            async with await open_transport_or_link('usb:0') as (hci_source, hci_sink):
                device = BumbleDevice.with_hci(
                    transport_name,
                    transport_mac,
                    hci_source,
                    hci_sink
                )
                await device.power_on()
                
                # Set up inquiry result handler
                def on_inquiry_result(address, class_of_device, data, rssi):
                    name = None
                    if lookup_names and data:
                        # Try to get name from inquiry response data
                        name = data.get('name')
                    devices.append((str(address), name or ''))
                
                device.on('inquiry_result', on_inquiry_result)
                
                # Start inquiry (discovery)
                await device.start_discovery()
                await asyncio.sleep(duration)
                await device.stop_discovery()
                
                await device.power_off()
            
            return devices
        
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        discovered = loop.run_until_complete(_scan())
        return ClassicDevice.found_to_list(discovered)

    def get_services(self, transport_name: str = 'btpy', transport_mac: str = '02:00:00:00:00:00') -> list[Service]:
        """Get services from a Classic Bluetooth device using Bumble SDP."""
        async def _get_services():
            services = []
            
            # Open a transport
            async with await open_transport_or_link('usb:0') as (hci_source, hci_sink):
                device = BumbleDevice.with_hci(
                    transport_name,
                    transport_mac,
                    hci_source,
                    hci_sink
                )
                await device.power_on()
                
                # Create SDP client and connect to remote device
                sdp_client = SdpClient(device)
                await sdp_client.connect(self.address)
                
                try:
                    # Search for all services
                    service_records = await sdp_client.search_services([])
                    
                    # Convert SDP records to Service objects
                    for record in service_records:
                        service_dict = {
                            'name': None,
                            'protocol': None,
                            'port': None,
                            'description': None,
                            'profiles': [],
                            'service-classes': [],
                            'provider': None,
                            'service-id': None
                        }
                        
                        # Extract service attributes from the record
                        if hasattr(record, 'attributes'):
                            for attr_id, attr_value in record.attributes.items():
                                if attr_id == 0x0000:  # Service Record Handle
                                    service_dict['service-id'] = str(attr_value)
                                elif attr_id == 0x0001:  # Service Class ID List
                                    service_dict['service-classes'] = [str(v) for v in attr_value] if isinstance(attr_value, list) else []
                                elif attr_id == 0x0004:  # Protocol Descriptor List
                                    # Extract protocol and port information
                                    if isinstance(attr_value, list):
                                        for protocol in attr_value:
                                            if isinstance(protocol, list) and len(protocol) >= 2:
                                                service_dict['protocol'] = str(protocol[0])
                                                service_dict['port'] = int(protocol[1]) if isinstance(protocol[1], int) else None
                                elif attr_id == 0x0005:  # Browse Group List
                                    pass
                                elif attr_id == 0x0009:  # Bluetooth Profile Descriptor List
                                    service_dict['profiles'] = [str(v) for v in attr_value] if isinstance(attr_value, list) else []
                                elif attr_id == 0x0100:  # Service Name
                                    service_dict['name'] = str(attr_value)
                                elif attr_id == 0x0101:  # Service Description
                                    service_dict['description'] = str(attr_value)
                                elif attr_id == 0x0102:  # Provider Name
                                    service_dict['provider'] = str(attr_value)
                        
                        services.append(service_dict)
                
                finally:
                    await sdp_client.disconnect()
                    await device.power_off()
            
            return services
        
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        service_dicts = loop.run_until_complete(_get_services())
        return Service.found_to_list(service_dicts)
