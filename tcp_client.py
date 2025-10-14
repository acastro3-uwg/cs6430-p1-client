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
        """Is the Client connected to the host.

        Returns:
            bool: True if connected, otherwise False.
        """
        return self._is_connected

    def connect(self) -> None:
        """Attempt to connect to the remote host."""
        if not self.is_connected:
            try:
                self._socket = self._create_socket()
                self._socket.connect(self._addr)
                self._is_connected = True
            except error:
                self._is_connected = False

    def disconnect(self) -> None:
        """Disconnect from the remote host."""
        if self.is_connected and self._socket is not None:
            self._socket.shutdown(SHUT_RDWR)
            self._socket.close()
            self._socket = None
            self._is_connected = False

    def _create_socket(self) -> socket:
        return socket(AF_INET, SOCK_STREAM)

    def send(self, data: bytes) -> None:
        """Send data to the connected remote.

        Args:
            data (bytes): The bytes to send.

        Raises:
            NotConnectedError: Raised if not connected to a host.
        """
        if self.is_connected and self._socket is not None:
            try:
                self._socket.sendall(data)
            except Exception:
                self._is_connected = False
                raise
        else:
            raise NotConnectedError("Socket not connected.")

    def recv(self, buff: int = 1024) -> bytes:
        """Receive data from host. Blocks forever.

        Args:
            buff (int, optional): Size of the buffer to use. Defaults to 1024.

        Raises:
            NotConnectedError: Raised if not connected to a host.

        Returns:
            bytes: The received bytes.
        """
        if self.is_connected and self._socket is not None:
            try:
                return self._socket.recv(buff)
            except Exception:
                self._is_connected = False
                raise
        else:
            raise NotConnectedError("Socket not connected.")
