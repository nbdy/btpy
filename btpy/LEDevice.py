from runnable import Runnable
from scapy.layers.bluetooth import BluetoothHCISocket, HCI_Hdr, HCI_Command_Hdr, HCI_Cmd_LE_Set_Scan_Parameters, \
    HCI_Cmd_LE_Set_Scan_Enable, HCI_LE_Meta_Advertising_Reports
from time import sleep
from loguru import logger as log


class LEDevice(Runnable):
    @staticmethod
    def scan(device=0, timeout=2):
        bt = BluetoothHCISocket(device)
        bt.sr(HCI_Hdr() / HCI_Command_Hdr() / HCI_Cmd_LE_Set_Scan_Parameters(type=1))
        bt.sr(HCI_Hdr() / HCI_Command_Hdr() / HCI_Cmd_LE_Set_Scan_Enable(enable=True, filter_dups=False))
        sleep(timeout)
        ads = bt.sniff(lfilter=lambda p: HCI_LE_Meta_Advertising_Reports in p)
        bt.sr(HCI_Hdr() / HCI_Command_Hdr() / HCI_Cmd_LE_Set_Scan_Enable(enable=False))
        log.debug("Disabled BT LE Scan")
        log.debug("Got {0} advertisements", len(ads))
