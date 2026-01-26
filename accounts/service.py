import grpc
import structlog
from codegen.accounts import service_pb2, service_pb2_grpc

from accounts import service_utils
from accounts.repository import AccountNotFoundError, AccountRepository, DuplicateEmailError
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

    def GetAccount(
        self, request: service_pb2.GetAccountRequest, context: grpc.ServicerContext
    ) -> service_pb2.GetAccountResponse:
        required_fields = ["email"]
        service_utils.validate_required(context, request, required_fields)

        account = self.repo.get_account_by_email(email=request.email)
        if not account:
            context.abort(grpc.StatusCode.NOT_FOUND, "Account not found", email=request.email)
            return service_pb2.GetAccountResponse()

        account_msg = service_pb2.Account(
            account_id=account.id,
            email=account.email,
            first_name=account.first_name,
            last_name=account.last_name,
            is_active=account.is_active,
            is_verified=account.is_verified,
        )
        return service_pb2.GetAccountResponse(
            account=account_msg,
            token=creds_utils.generate_token(
                account.email,
                account.first_name,
                account.last_name,
            ),
        )

    def UpdateAccount(
        self, request: service_pb2.UpdateAccountRequest, context: grpc.ServicerContext
    ) -> service_pb2.UpdateAccountResponse:
        required_fields = ["account_id", "email", "first_name", "last_name", "hashed_password"]
        service_utils.validate_required(context, request, required_fields)

        try:
            updated_account = self.repo.update_account(
                request.account_id,
                request.email,
                request.first_name,
                request.last_name,
                request.hashed_password,
            )
        except AccountNotFoundError as e:
            context.abort(grpc.StatusCode.NOT_FOUND, str(e), account_id=request.account_id)
            return service_pb2.UpdateAccountResponse()
        if not updated_account:
            context.abort(grpc.StatusCode.INTERNAL, "Failed to update account", account_id=request.account_id)
            return service_pb2.UpdateAccountResponse()

        account = service_pb2.Account(
            account_id=updated_account.id,
            email=updated_account.email,
            first_name=updated_account.first_name,
            last_name=updated_account.last_name,
            is_active=updated_account.is_active,
            is_verified=updated_account.is_verified,
        )
        return service_pb2.UpdateAccountResponse(account=account)

    def DeleteAccount(
        self, request: service_pb2.DeleteAccountRequest, context: grpc.ServicerContext
    ) -> service_pb2.DeleteAccountResponse:
        required_fields = ["account_id"]
        service_utils.validate_required(context, request, required_fields)

        try:
            self.repo.delete_account(account_id=request.account_id)
            logger.info("Account deleted", account_id=request.account_id)
            return service_pb2.DeleteAccountResponse(success=True)
        except AccountNotFoundError as e:
            context.abort(grpc.StatusCode.NOT_FOUND, str(e), account_id=request.account_id)
            return service_pb2.DeleteAccountResponse(success=False)
