import logging
import sys
import structlog
from structlog.dev import ConsoleRenderer
from concurrent import futures

import grpc

from codegen.accounts import service_pb2_grpc

from accounts.db import get_session
from accounts.repository import AccountRepository
from accounts.service import AccountService
from accounts.utils import creds_utils


def configure_structlog(local: bool = False) -> None:
    log_level = logging.DEBUG if local else logging.INFO
    console = ConsoleRenderer() if local else structlog.processors.JSONRenderer()
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.add_log_level,
            structlog.processors.dict_tracebacks,
            console if console else structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(log_level),
        logger_factory=structlog.PrintLoggerFactory(file=sys.stdout),
        cache_logger_on_first_use=True,
    )


def serve():
    local = len(sys.argv) > 1 and sys.argv[1] == "local"
    configure_structlog(local=local)
    logger = structlog.get_logger()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    repo = AccountRepository(get_session())
    service_pb2_grpc.add_AccountServiceServicer_to_server(
        AccountService(repo),
        server,
    )
    credentials = grpc.ssl_server_credentials(creds_utils.load_credentials())
    server.add_secure_port("[::]:50051", credentials)
    server.start()
    logger.info("AccountService started", port=50051)

    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        logger.info("AccountService stopping")
        server.stop(0)


if __name__ == "__main__":
    serve()
