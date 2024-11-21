import ipaddress
import os
from configparser import ConfigParser, ParsingError
from pathlib import Path


class ConfigLoader:
    config_path: str
    config: ConfigParser

    def __init__(self, config_path="config.ini"):
        self.config_path = config_path
        self.config = ConfigParser()

    def load(self):
        try:
            if not Path(self.config_path).is_file():
                raise FileNotFoundError(f"{self.config_path} file does not exist.")
            self._load_config_file()
            self._validate_config()

            return self.config
        except Exception as e:
            print(f"Error: {e}")

        return None

    def _load_config_file(self):
        err_msg: str

        try:
            self.config.read(self.config_path, encoding="utf-8")
            return
        except PermissionError:
            err_msg = f"Unable to access {self.config_path}."
        except UnicodeDecodeError:
            err_msg = f"Failed to decode {self.config_path}. Is it encoded in UTF-8?"
        except ParsingError:
            err_msg = f"Failed to parse {self.config_path}. Check the file format."
        except OSError as e:
            err_msg = f"Unexpected I/O error - {e}"

        raise Exception(err_msg)

    def _validate_config(self):
        self._validate_config_sections()
        self._validate_config_options()
        self._validate_config_values()

    def _validate_config_sections(self):
        expected_sections = ["PalServer", "Unix"]
        actual_sections = self.config.sections()
        if actual_sections != expected_sections:
            raise ValueError(
                f"Invalid configuration sections. Expected {expected_sections}, got {actual_sections}."
            )

    def _validate_config_options(self):
        palserver_options = [
            "program_path",
            "program_args",
            "ip",
            "port",
            "rcon_port",
            "rcon_pwd",
        ]
        unix_options = ["root_pwd"]

        actual_palserver_options = self.config.options("PalServer")
        actual_unix_options = self.config.options("Unix")

        if actual_palserver_options != palserver_options:
            raise ValueError(
                f"Invalid options in 'PalServer'. Expected {palserver_options}, got {actual_palserver_options}."
            )
        if actual_unix_options != unix_options:
            raise ValueError(
                f"Invalid options in 'Unix'. Expected {unix_options}, got {actual_unix_options}."
            )

    def _validate_config_values(self):
        palserver_config = self.config["PalServer"]
        unix_config = self.config["Unix"]

        if not self._is_program_exist(palserver_config["program_path"]):
            raise ValueError("Program not found at the path.")

        if not self._is_ip_address(palserver_config["ip"]):
            raise ValueError("Server address is not in IP address format.")

        if not self._is_port_number(palserver_config["port"]):
            raise ValueError("Not a valid server port number.")

        if not self._is_port_number(palserver_config["rcon_port"]):
            raise ValueError("Not a valid RCON port number.")

        if not self._is_pwd_ascii(palserver_config["rcon_pwd"]):
            raise ValueError("Rcon password should contain only ASCII characters.")

        if os.name != "nt" and not len(unix_config["root_pwd"]) > 0:
            raise ValueError("Root password not set.")

    @staticmethod
    def _is_program_exist(path: str):
        try:
            Path(path).is_file()
            return True
        except:
            return False

    @staticmethod
    def _is_ip_address(ip: str):
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            return False

    @staticmethod
    def _is_port_number(port: str):
        try:
            p = int(port)
            if 0 <= p <= 65535:
                return True
            return False
        except ValueError:
            return False

    @staticmethod
    def _is_pwd_ascii(pwd: str):
        try:
            pwd.encode("ascii")
            return True
        except UnicodeEncodeError:
            return False
