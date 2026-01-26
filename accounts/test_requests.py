import logging

import grpc
import structlog
from codegen.accounts import service_pb2, service_pb2_grpc

from accounts.utils import creds_utils

logger = structlog.get_logger()


def configure_logger():
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
            structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S", utc=False),
            structlog.dev.ConsoleRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(logging.NOTSET),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=False,
    )


if __name__ == "__main__":
    configure_logger()
    logger = structlog.get_logger()

    logger.info("Starting AccountService client")
    logger.info("Loading credentials for secure channel")
    credentials = grpc.ssl_channel_credentials(creds_utils.load_credentials()[0][1])

    with grpc.secure_channel("localhost:50051", credentials) as channel:
        logger.info("Secure channel established with AccountService")
        stub = service_pb2_grpc.AccountServiceStub(channel)

        # Example request to CreateAccount
        request = service_pb2.CreateAccountRequest(
            email="test@example.com", first_name="Test", last_name="User", hashed_password="hashed_password_example"
        )
        logger.info("Sending Create Account Request:", request=request)
        response = stub.CreateAccount(request)
        logger.info("Create Account Response:", response=response)

        # Example request to GetAccount
        logger.info("Sending Get Account Request:", email="test@example.com")
        request_get = service_pb2.GetAccountRequest(email="test@example.com")
        response_get = stub.GetAccount(request_get)
        logger.info("Get Account Response:", account=response_get)

        # Example request to UpdateAccount
        logger.info("Sending Update Account Request")
        request_update = service_pb2.UpdateAccountRequest(
            account_id=response.account.account_id,
            email="test@mail.com",
            first_name="Updated first name",
            last_name="Updated last name",
            hashed_password="new_hashed_password",
        )
        response_update = stub.UpdateAccount(request_update)
        logger.info("Update Account Response:", response_update=response_update)

        request_get = service_pb2.GetAccountRequest(email=response_update.account.email)
        response_get = stub.GetAccount(request_get)
        logger.info("Get updated account:", response=response_get)

        # Example request to DeleteAccount
        logger.info("Sending Delete Account Request")
        request_delete = service_pb2.DeleteAccountRequest(account_id=response.account.account_id)
        response_delete = stub.DeleteAccount(request_delete)
        logger.info("Delete Account Response:", response_delete=response_delete)
        # Verify Deletion by attempting to GetAccount again
        try:
            request_get = service_pb2.GetAccountRequest(email=request_update.email)
            response_get = stub.GetAccount(request_get)
        except grpc.RpcError as e:
            logger.error("Expected error when getting deleted account:", error=e.details())
    logger.info("AccountService client finished")
