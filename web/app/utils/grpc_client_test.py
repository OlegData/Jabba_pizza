import types
import unittest
from unittest import mock

from web.app.utils import grpc_client

fake_module_grpc = types.ModuleType("fake_pb2_grpc")
setattr(fake_module_grpc, "TestServiceStub", mock.Mock())


class GrpcClientTest(unittest.TestCase):
    @mock.patch("web.app.utils.grpc_client.grpc.secure_channel")
    @mock.patch("web.app.utils.grpc_client.os.path.exists")
    @mock.patch("web.app.utils.grpc_client.open", new_callable=mock.mock_open, read_data=b"cert-data")
    def test_call_successful(self, mock_open, mock_path_exists, mock_secure_channel):
        mock_path_exists.return_value = True
        mock_stub_instance = mock.Mock()
        mock_method = mock.Mock(return_value="response-data")
        setattr(mock_stub_instance, "TestMethod", mock_method)

        setattr(fake_module_grpc, "TestServiceStub", mock.Mock(return_value=mock_stub_instance))

        client = grpc_client.GrpcClient(
            service_name="TestService",
            pb2_grpc_module=fake_module_grpc,
            addr="localhost:50051",
            cert_path="/path/to/cert",
        )

        request = mock.Mock()
        response = client.call("TestMethod", request)

        mock_open.assert_called_once_with("/path/to/cert", "rb")
        mock_secure_channel.assert_called_once()
        mock_method.assert_called_once_with(request)
        self.assertEqual(response, "response-data")

    def test_init_with_invalid_module_raises_value_error(self):
        with self.assertRaises(ValueError) as context:
            grpc_client.GrpcClient(
                service_name="TestService",
                pb2_grpc_module="invalid_module_type",
            )
        self.assertIn("Failed to import grpc_module", str(context.exception))

    @mock.patch("web.app.utils.grpc_client.os.path.exists")
    def test_channel_with_missing_cert_raises_file_not_found(self, mock_path_exists):
        mock_path_exists.return_value = False

        mock_stub_instance = mock.Mock()

        setattr(fake_module_grpc, "TestServiceStub", mock.Mock(return_value=mock_stub_instance))

        client = grpc_client.GrpcClient(
            service_name="TestService",
            pb2_grpc_module=fake_module_grpc,
            cert_path="/invalid/path/to/cert",
        )

        with self.assertRaises(FileNotFoundError) as context:
            client._channel()
        self.assertIn("Certificate file not found", str(context.exception))
