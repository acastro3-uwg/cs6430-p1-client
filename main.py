from pathlib import Path
from lib import encode_to_base64, get_branch_name
from tcp_client import Client
from logging import getLogger, basicConfig, INFO, FileHandler, StreamHandler
from pathlib import Path
import argparse


loger = getLogger(__name__)


def start_data_transfer(path: Path) -> None:
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

    file_text = path.read_text()
    branch_name = get_branch_name(file_text)
    if branch_name is not None:
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
    else:
        print("File doesn't contain branch code")


def main(path: Path) -> None:
    """Entry point into the program."""
    basicConfig(
        format="%(asctime)s %(name)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=INFO,
        handlers=[FileHandler("project.log"), StreamHandler()],
    )

    start_data_transfer(path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="client", usage="%(prog)s [options]")
    parser.add_argument(
        "filepath",
        type=Path,
        nargs="?",
        default=".",
        help="Path to the weekly report or its containing directory.",
    )
    args = parser.parse_args()
    arg_path = Path(args.filepath.resolve())

    final_path = None

    if arg_path.exists():
        if not arg_path.is_dir():
            final_path = arg_path
        else:
            filepath = arg_path / "branch_weekly_sales.txt"
            if filepath.exists():
                final_path = filepath

    if final_path is not None:
        main(final_path)
    else:
        print("no valid file detected.")
