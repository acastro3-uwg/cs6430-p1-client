from socket import socket, SOCK_STREAM, AF_INET, SHUT_RDWR, error
from typing import Optional
from logging import getLogger


logger = getLogger(__name__)


class NotConnectedError(Exception): ...


class Client:
    def __init__(self, ip: str, port: int) -> None:
        self._socket: Optional[socket] = None
        self._addr = (ip, port)
        self._is_connected = False

    @property
    def is_connected(self) -> bool:
        return self._is_connected

    def connect(self) -> None:
        if not self.is_connected:
            try:
                self._socket = self._create_socket()
                self._socket.connect(self._addr)
                self._is_connected = True
            except error:
                self._is_connected = False

    def disconnect(self) -> None:
        if self.is_connected and self._socket is not None:
            self._socket.shutdown(SHUT_RDWR)
            self._socket.close()
            self._socket = None
            self._is_connected = False

    def _create_socket(self) -> socket:
        return socket(AF_INET, SOCK_STREAM)

    def send(self, data: bytes) -> None:
        if self.is_connected and self._socket is not None:
            try:
                self._socket.sendall(data)
            except Exception:
                self._is_connected = False
                raise
        else:
            raise NotConnectedError("Socket not connected.")

    def recv(self, buff: int = 1024) -> bytes:
        if self.is_connected and self._socket is not None:
            try:
                return self._socket.recv(buff)
            except Exception:
                self._is_connected = False
                raise
        else:
            raise NotConnectedError("Socket not connected.")
