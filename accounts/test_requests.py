import grpc

from accounts.utils import creds_utils
from codegen.accounts import service_pb2_grpc, service_pb2


if __name__ == "__main__":
    credentials = grpc.ssl_channel_credentials(creds_utils.load_credentials()[0][1])
    with grpc.secure_channel("localhost:50051", credentials) as channel:
        stub = service_pb2_grpc.AccountServiceStub(channel)

        # Example request to CreateAccount
        request = service_pb2.CreateAccountRequest(
            email="test@example.com", first_name="Test", last_name="User", hashed_password="hashed_password_example"
        )
        response = stub.CreateAccount(request)
        print("Response:", response)
