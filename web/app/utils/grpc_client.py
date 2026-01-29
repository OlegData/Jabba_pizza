import os
import types

import grpc
import structlog

logger = structlog.get_logger()


class GrpcClient:
    """gRPC client utility.
    Provides a generic gRPC client class to call methods on a specified service.
    from accounts import service_pb2, service_pb2_grpc
    client = GrpcClient(pb2_grpc_module=service_pb2_grpc)
    req = service_pb2.CreateAccountRequest(...)
    resp = client.call("CreateAccount", req)
    """

    def __init__(
        self,
        service_name: str,
        pb2_grpc_module: types.ModuleType,
        addr: str = None,
        cert_path: str = None,
    ):
        self.service_name = service_name
        self.addr = addr or os.getenv("GRPC_ADDR", "localhost:50051")
        self.cert_path = cert_path or os.getenv(
            "GRPC_CERT_PATH", os.path.join(os.path.dirname(__file__), "..", "certs", "server.crt")
        )
        if isinstance(pb2_grpc_module, types.ModuleType):
            self.pb2_grpc_module = pb2_grpc_module
        else:
            logger.error("Failed to import grpc_module", module=pb2_grpc_module)
            raise ValueError(f"Failed to import grpc_module: {pb2_grpc_module}")

    def _channel(self):
        if not os.path.exists(self.cert_path):
            logger.error("Certificate file not found", path=self.cert_path)
            raise FileNotFoundError(f"Certificate file not found: {self.cert_path}")
        with open(self.cert_path, "rb") as f:
            credentials = grpc.ssl_channel_credentials(root_certificates=f.read())
        return grpc.secure_channel(self.addr, credentials)

    def _stub(self, channel):
        cls = getattr(self.pb2_grpc_module, f"{self.service_name}Stub", None)
        if cls is None:
            logger.error("Unknown service", service=self.service_name)
            raise ValueError(f"Unknown service: {self.service_name}")
        return cls(channel)

    def call(self, method: str, request):
        with self._channel() as channel:
            stub = self._stub(channel)
            rpc = getattr(stub, method, None)
            if rpc is None:
                raise ValueError(f"Unknown method {method} on {self.service_name}")
            try:
                return rpc(request)
            except grpc.RpcError as e:
                code, detail = e.code(), e.details()
                logger.error(
                    "gRPC call failed",
                    service=self.service_name,
                    method=method,
                    code=code,
                    detail=detail,
                )
                raise RuntimeError(
                    f"gRPC call {self.service_name}.{method} failed: {e.code().name} - {e.details()}"
                ) from e
