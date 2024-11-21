import socket
import struct


AUTH_REQUEST_TYPE = 3
EXEC_COMMAND_TYPE = 2
AUTH_FAILED_ID = -1
REQUEST_ENCODING_TYPE = "ascii"
RESPONSE_DECODING_TYPE = "utf-8"
PACKET_TRAILER = "\x00\x00".encode(REQUEST_ENCODING_TYPE)
HEADER_SIZE = 8
TRAILER_SIZE = 2
ID_INDEX = 0
HEADER_INDEX = 1
BODY_INDEX = 2


class RconSocket:
    _host: str
    _port: int

    def __init__(self, host: str, port: int):
        self._host = host
        self._port = port
        self.socket = None

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self._host, self._port))

    def disconnect(self):
        if self.socket:
            self.socket.close()
            self.socket = None

    def send(self, data: bytes):
        if not self.socket:
            raise ConnectionError("Socket is not connected.")
        packet = struct.pack("<i", len(data) + 4) + data
        self.socket.sendall(packet)

    def receive(self):
        if not self.socket:
            raise ConnectionError("Socket is not connected.")
        data_length = struct.unpack("<i", self.socket.recv(4))[0]
        return self.socket.recv(data_length)

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.disconnect()


class Rcon:
    _socket: RconSocket
    _password: str
    _req_id: int

    def __init__(self, socket: RconSocket, password: str):
        self._socket = socket
        self._password = password
        self._req_id = 0

    def can_connect(self):
        try:
            with self._socket:
                return True
        except:
            return False

    def is_authenticated(self):
        auth_id = self._authenticate()
        if auth_id == AUTH_FAILED_ID:
            return False
        return True

    def send_command(self, command: str):
        with self._socket:
            self._execute(AUTH_REQUEST_TYPE, self._password)
            response = self._execute(EXEC_COMMAND_TYPE, command)
            return response[BODY_INDEX]

    def _authenticate(self):
        with self._socket:
            response = self._execute(AUTH_REQUEST_TYPE, self._password)
            return response[ID_INDEX]

    def _execute(self, req_type: int, data: str):
        self._send(req_type, data)
        return self._receive()

    def _send(self, req_type: int, data: str):
        packet = (
            struct.pack("<ii", self.req_id, req_type)
            + data.encode(REQUEST_ENCODING_TYPE)
            + PACKET_TRAILER
        )
        self._socket.send(packet)

    def _receive(self):
        data = self._socket.receive()

        header: tuple[int, int] = struct.unpack("<ii", data[:HEADER_SIZE])
        body = ""
        if len(data) > HEADER_SIZE + TRAILER_SIZE:
            body = data[HEADER_SIZE:-TRAILER_SIZE].decode(RESPONSE_DECODING_TYPE)

        return (*header, body)

    @property
    def req_id(self):
        self._req_id += 1
        return self._req_id
