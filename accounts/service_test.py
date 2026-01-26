import unittest
from types import SimpleNamespace
from unittest import mock

import grpc

from accounts.models.users import User
from accounts.repository import AccountNotFoundError, DuplicateEmailError
from accounts.service import AccountService


class AccountServiceTest(unittest.TestCase):
    def setUp(self):
        self.repo = mock.Mock()
        self.account_service = AccountService(repo=self.repo)
        self.context = mock.Mock(spec=grpc.ServicerContext)
        self.request = SimpleNamespace(
            email="test@example.com",
            first_name="Test",
            last_name="User",
            hashed_password="super-secret",
        )

    @mock.patch("accounts.utils.creds_utils.generate_token")
    @mock.patch("accounts.service_utils.validate_required")
    def test_CreateAccount_returns_account_response(self, mock_validate_required, mock_generate_token):
        created_account = {
            "account_id": 1,
            "email": self.request.email,
            "first_name": self.request.first_name,
            "last_name": self.request.last_name,
            "hashed_password": self.request.hashed_password,
        }
        mock_generate_token.return_value = "signed-token"
        self.repo.create_account.return_value = User(
            id=1,
            email=self.request.email,
            first_name=self.request.first_name,
            last_name=self.request.last_name,
            hashed_password=self.request.hashed_password,
            is_active=True,
            is_verified=False,
        )

        response = self.account_service.CreateAccount(request=self.request, context=self.context)

        mock_validate_required.assert_called_once_with(
            self.context,
            self.request,
            ["email", "first_name", "last_name", "hashed_password"],
        )
        self.repo.create_account.assert_called_once()
        kwargs = self.repo.create_account.call_args.kwargs
        self.assertEqual(kwargs["email"], self.request.email)
        self.assertEqual(kwargs["hashed_password"], self.request.hashed_password)
        self.assertEqual(response.account.account_id, created_account["account_id"])
        self.assertEqual(response.account.email, created_account["email"])
        self.assertEqual(response.token, "signed-token")
        mock_generate_token.assert_called_once_with("test@example.com", "Test", "User")

    def test_CreateAccount_duplicate_email_aborts(self):
        self.repo.create_account.side_effect = DuplicateEmailError("Email already exists")

        self.account_service.CreateAccount(request=self.request, context=self.context)

        self.context.abort.assert_called_once_with(
            grpc.StatusCode.ALREADY_EXISTS,
            "Email already exists",
        )
        self.repo.create_account.assert_called_once()

    def test_CreateAccount_missing_required_field_aborts(self):
        self.request.email = ""

        error = grpc.RpcError()
        error.code = lambda: grpc.StatusCode.INVALID_ARGUMENT
        error.details = lambda: "Field email is required"
        self.context.abort.side_effect = error
        with self.assertRaises(grpc.RpcError):
            self.account_service.CreateAccount(request=self.request, context=self.context)

        self.context.abort.assert_called_once_with(
            grpc.StatusCode.INVALID_ARGUMENT,
            "Email is required",
        )

    @mock.patch("accounts.utils.creds_utils.generate_token")
    @mock.patch("accounts.service_utils.validate_required")
    def test_GetAccount_returns_account_response(self, mock_validate_required, mock_generate_token):
        mock_generate_token.return_value = "signed-token"
        self.repo.get_account_by_email.return_value = User(
            id=1,
            email=self.request.email,
            first_name=self.request.first_name,
            last_name=self.request.last_name,
            hashed_password=self.request.hashed_password,
            is_active=True,
            is_verified=False,
        )
        self.account_service.GetAccount(request=self.request, context=self.context)

    def test_UpdateAccount_account_not_found_aborts(self):
        self.request.account_id = 1
        self.repo.update_account.side_effect = AccountNotFoundError("Account not found")

        self.account_service.UpdateAccount(request=self.request, context=self.context)

        self.context.abort.assert_called_once_with(
            grpc.StatusCode.NOT_FOUND,
            "Account not found",
            account_id=self.request.account_id,
        )
        self.repo.update_account.assert_called_once()

    @mock.patch("accounts.service_utils.validate_required")
    def test_UpdateAccount_response(self, mock_validate_required):
        self.request.account_id = 1
        self.repo.update_account.return_value = User(
            id=1,
            email="test@example.com",
            first_name="Test",
            last_name="User",
            hashed_password="hashed_password",
            is_active=True,
            is_verified=False,
        )
        self.account_service.UpdateAccount(request=self.request, context=self.context)
        self.repo.update_account.assert_called_once_with(
            self.request.account_id,
            self.request.email,
            self.request.first_name,
            self.request.last_name,
            self.request.hashed_password,
        )

    def test_DeleteAccount_successful(self):
        self.request.account_id = 1

        response = self.account_service.DeleteAccount(request=self.request, context=self.context)

        self.repo.delete_account.assert_called_once_with(account_id=self.request.account_id)
        self.assertTrue(response.success)

    def test_DeleteAccount_not_found_aborts(self):
        request = mock.Mock()
        request.account_id = 999
        self.repo.delete_account.side_effect = AccountNotFoundError("Account not found")

        self.account_service.DeleteAccount(request=request, context=self.context)

        self.context.abort.assert_called_once_with(
            grpc.StatusCode.NOT_FOUND,
            "Account not found",
            account_id=request.account_id,
        )
        self.repo.delete_account.assert_called_once_with(account_id=request.account_id)
