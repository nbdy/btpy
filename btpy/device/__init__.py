from datetime import datetime
from dataclasses import dataclass


@dataclass
class Device:
    address: str
    timestamp: datetime

    def __init__(self, address: str):
        self.address = address
        self.timestamp = datetime.now()
