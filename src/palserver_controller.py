import subprocess
from configparser import ConfigParser
from subprocess import Popen
from psutil import Process
import psutil
from src.palserver_sniffer import PalServerPacketSniffer
from src.rcon import Rcon, RconSocket
from src.util import wait_timer


class PalServerController:
    _run_params: list[str]
    _rcon: Rcon
    _sniffer: PalServerPacketSniffer

    def __init__(self, config: ConfigParser):
        program_path = config["PalServer"]["program_path"]
        program_args = config["PalServer"]["program_args"]
        server_ip = config["PalServer"]["ip"]
        server_port = int(config["PalServer"]["port"])
        rcon_port = int(config["PalServer"]["rcon_port"])
        rcon_pwd = config["PalServer"]["rcon_pwd"]
        root_pwd = config["Unix"]["root_pwd"]

        self._run_params = [program_path, program_args]
        self._rcon = Rcon(RconSocket(server_ip, rcon_port), rcon_pwd)
        self._sniffer = PalServerPacketSniffer(server_port, root_pwd)

    def has_players(self):
        players_output = self._rcon.send_command("showPlayers")
        if len(players_output.strip().split("\n")) < 2:
            return False
        else:
            return True

    def get_players(self):
        if not self.has_players():
            return [""]

        players_output = self._rcon.send_command("showPlayers")
        return players_output.strip().split("\n")[1:]

    def start_server(self):
        Popen(
            self._run_params,
            creationflags=subprocess.DETACHED_PROCESS,
        )
        wait_timer("server to start")

    def pause_server(self):
        server_ps = self.find_palserver_process()
        if server_ps:
            server_ps.suspend()

    def resume_server(self):
        server_ps = self.find_palserver_process()
        if server_ps:
            server_ps.resume()
            wait_timer("players to connect")

    def restart_server(self):
        self._rcon.send_command("DoExit")
        wait_timer("shutdown")
        self.start_server()

    def is_server_running(self):
        return self._rcon.can_connect()

    def capture_server_packet(self):
        return self._sniffer.capture()

    @staticmethod
    def find_palserver_process():
        for process in psutil.process_iter(attrs=["pid", "name"]):
            name = process.name()
            if "PalServer" in name and "Shipping" in name:
                return process

        return None
