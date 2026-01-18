import jwt
import unittest
from unittest import mock

from accounts.utils import creds_utils as utils


class UtilsTest(unittest.TestCase):
    @mock.patch("builtins.open", new_callable=mock.mock_open, read_data=b"data")
    def test_load_credentials(self, mock_open):
        credentials = utils.load_credentials()
        self.assertIsInstance(credentials, list)
        self.assertEqual(len(credentials[0]), 2)
        self.assertEqual(credentials[0][0], b"data")
        self.assertEqual(credentials[0][1], b"data")

    @mock.patch.object(utils.logger, "error")
    @mock.patch("builtins.open")
    def test_load_credentials_dir_not_found(self, mock_open, mock_logger_error):
        mock_open.side_effect = FileNotFoundError
        with self.assertRaises(FileNotFoundError) as error:
            utils.load_credentials()
        mock_logger_error.assert_called_with(
            "Certificate files not found",
            error=str(error.exception),
            cert_file=mock.ANY,
            key_file=mock.ANY,
        )

    def test_generate_token(self):
        token = utils.generate_token("mail@mail.com", "First", "Last")
        self.assertIsInstance(token, str)
        decoded = jwt.decode(token, utils.JWT_SECRET, algorithms=[utils.JWT_ALGORITHM])
        self.assertEqual(decoded["email"], "mail@mail.com")
        self.assertEqual(decoded["first_name"], "First")
        self.assertEqual(decoded["last_name"], "Last")
