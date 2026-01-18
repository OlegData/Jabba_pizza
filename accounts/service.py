import structlog
import grpc

from codegen.accounts import service_pb2, service_pb2_grpc

from accounts import service_utils
from accounts.repository import AccountRepository, DuplicateEmailError
from accounts.utils import creds_utils

logger = structlog.get_logger()


class AccountService(service_pb2_grpc.AccountServiceServicer):
    def __init__(self, repo: AccountRepository):
        self.repo = repo

    def CreateAccount(
        self, request: service_pb2.CreateAccountRequest, context: grpc.ServicerContext
    ) -> service_pb2.CreateAccountResponse:
        required_fields = ["email", "first_name", "last_name", "hashed_password"]
        service_utils.validate_required(context, request, required_fields)

        try:
            account = self.repo.create_account(
                email=request.email,
                first_name=request.first_name,
                last_name=request.last_name,
                hashed_password=request.hashed_password,
            )
            logger.info("Account created", account_id=account.id)
        except DuplicateEmailError as e:
            context.abort(grpc.StatusCode.ALREADY_EXISTS, str(e))
            return service_pb2.CreateAccountResponse()

        account_msg = service_pb2.Account(
            account_id=account.id,
            email=account.email,
            first_name=account.first_name,
            last_name=account.last_name,
            is_active=account.is_active,
            is_verified=account.is_verified,
        )
        return service_pb2.CreateAccountResponse(
            account=account_msg,
            token=creds_utils.generate_token(
                account.email,
                account.first_name,
                account.last_name,
            ),
        )
