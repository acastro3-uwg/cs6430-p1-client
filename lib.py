import base64
from typing import Optional
from re import compile, MULTILINE

branch_pattern = compile(r"^([^,]+).*.\d{4}-\d{0,2}-\d{0,2}", MULTILINE)


def encode_to_base64(txt: str) -> bytes:
    """Accept a string, encode it in Base64, and return the encoded string.

    Args:
        txt (str): String to encode

    Returns:
        bytes: The encoded string
    """
    return base64.b64encode(txt.encode("ascii"))


def get_branch_name(txt: str) -> Optional[str]:
    """Find branch name given a CSV file following the format:

    Branch code, product code, quantity sold, date sold
    ALBNM, PROD001, 12, 2023-01-01

    Args:
        txt (str): File content

    Returns:
        str: The branch name
    """
    match = branch_pattern.search(txt)

    result = None
    if match is not None:
        result = match.group(1)

    return result
