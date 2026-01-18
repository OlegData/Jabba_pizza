import unittest
from unittest import mock
import grpc

from accounts.service_utils import validate_required


class ServiceUtilsTest(unittest.TestCase):
    def test_validate_required(self):
        mock_content = mock.Mock()
        Request = type("Request", (), {"field1": "value", "field2": "value"})()
        required_fields = ["field1", "field2"]
        validate_required(mock_content, Request, required_fields)
        mock_content.abort.assert_not_called()

    def test_validate_required_missing_field(self):
        mock_content = mock.Mock()
        Request = type("Request", (), {"field1": "value"})()
        required_fields = ["field1", "field2"]
        validate_required(mock_content, Request, required_fields)
        mock_content.abort.assert_called_once_with(
            grpc.StatusCode.INVALID_ARGUMENT,
            "Field2 is required",
        )
