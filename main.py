from pathlib import Path
from lib import encode_to_base64, get_branch_name
from tcp_client import Client
from logging import getLogger, basicConfig, INFO, FileHandler, StreamHandler


loger = getLogger(__name__)


def start_data_transfer() -> None:
    """Client algorithm
    1. read input
    1. start socket connection
    1. print connected
    1. send branch code
    1. log ok from server
    1. send encoded file
    1. print received
    1. log ok from server
    """

    path = Path().cwd() / "branch_weekly_sales.txt"
    file_text = path.read_text()
    branch_name = get_branch_name(file_text)
    encoded_file = encode_to_base64(file_text)

    client = Client("127.0.0.1", 4242)
    client.connect()
    if client.is_connected:
        loger.info("connected to server")
        client.send(f"bcode~{branch_name}".encode("ascii"))
        reply = client.recv(1024)
        loger.info(f"received: {reply.decode()}")
        if reply.decode() == "OK":
            client.send(b"~" + encoded_file + b"~")
            reply = client.recv(1024)
            loger.info(f"received: {reply.decode()}")
    else:
        print("no connection")


def main() -> None:
    """Entry point into the program."""
    basicConfig(
        format="%(asctime)s %(name)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=INFO,
        handlers=[FileHandler("project.log"), StreamHandler()],
    )

    start_data_transfer()


if __name__ == "__main__":
    main()
