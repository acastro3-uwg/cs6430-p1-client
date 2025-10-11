from unittest import TestCase
from lib import encode_to_base64


class TestLib(TestCase):
    def test_encoding(self):
        under_test = "ALBNM, PROD001, 12, 2023-01-01"
        expected = b"QUxCTk0sIFBST0QwMDEsIDEyLCAyMDIzLTAxLTAx"
        result = encode_to_base64(under_test)
        self.assertEqual(expected, result)
