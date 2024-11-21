import ctypes
import os
import subprocess
import sys
from scapy.all import sniff
from scapy.packet import Packet


class PalServerPacketSniffer:
    _port: int
    _root_pwd: str

    def __init__(self, palserver_port: int, root_pwd: str):
        self._port = palserver_port
        self._root_pwd = root_pwd

    def capture(self):
        if os.name == "nt":
            return self._capture_windows_packet()
        else:
            return self._capture_unix_packet()

    def _capture_windows_packet(self):
        packet: Packet = sniff(filter=f"udp dst port {self._port}", count=1, store=1)[0]

        return packet.sprintf("%.time% IP %IP.src%:%UDP.sport% > %IP.dst%:%UDP.dport%")

    def _capture_unix_packet(self):
        result = subprocess.run(
            f"echo {self._root_pwd} | sudo -S tcpdump -n -c 1 udp and dst port {self._port}",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            text=True,
        )

        return result.stdout.strip()


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


if os.name == "nt" and not is_admin():
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, " ".join(sys.argv), None, 1
    )
    sys.exit()
