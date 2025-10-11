from pathlib import Path
from lib import encode_to_base64, get_branch_name
from tcp_client import Client


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
    print(branch_name)
    encoded_file = encode_to_base64(file_text)

    client = Client("127.0.0.1", 4242)
    if client.is_connected:
        print("connected to server")
    # client.connect()
    print(encoded_file)


def main() -> None:
    """Entry point into the program."""
    start_data_transfer()


if __name__ == "__main__":
    main()
