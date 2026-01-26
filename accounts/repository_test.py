import os
import tempfile
import unittest
from unittest import mock

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from accounts import repository
from accounts.models import base, users


class TestAccountRepository(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        db_path = os.path.join(self.tmpdir.name, "test.db")
        self.engine = create_engine("sqlite:///" + db_path)
        base.Base.metadata.create_all(self.engine)

        self.Session = sessionmaker(bind=self.engine)
        self.repo = repository.AccountRepository(self.Session())

    def tearDown(self):
        self.engine.dispose()
        self.tmpdir.cleanup()
        return super().tearDown()

    def test_create_account(self):
        new_account = self.repo.create_account(
            email="test@example.com",
            first_name="Test",
            last_name="User",
            hashed_password="Test",
        )
        check_session = self.Session()
        user = check_session.query(users.User).filter_by(email="test@example.com").one_or_none()
        self.assertIsNotNone(user)
        self.assertEqual(new_account.id, user.id)
        self.assertEqual(new_account.email, user.email)
        self.assertEqual(new_account.first_name, user.first_name)
        self.assertEqual(new_account.last_name, user.last_name)
        self.assertEqual(new_account.hashed_password, user.hashed_password)

    @mock.patch.object(repository.logger, "warning")
    def test_create_account_duplicate_email(self, mock_warning_logger):
        self.repo.create_account(
            email="test@example.com",
            first_name="Test",
            last_name="User",
            hashed_password="Test",
        )
        with self.assertRaises(repository.DuplicateEmailError):
            self.repo.create_account(
                email="test@example.com",
                first_name="Test2",
                last_name="User2",
                hashed_password="Test2",
            )
        mock_warning_logger.assert_called_once_with("User already exists", email="test@example.com")

    def test_get_account_by_email(self):
        self.repo.create_account(
            email="test@email.com",
            first_name="First",
            last_name="Last",
            hashed_password="hashed_pw",
        )
        account = self.repo.get_account_by_email("test@email.com")
        self.assertIsNotNone(account)
        self.assertEqual(account.email, "test@email.com")
        self.assertEqual(account.first_name, "First")
        self.assertEqual(account.last_name, "Last")

    def test_get_account_by_email_not_found(self):
        account = self.repo.get_account_by_email("test@email.com")
        self.assertIsNone(account)

    def test_update_account(self):
        account = self.repo.create_account(
            email="test@mail.com",
            first_name="First",
            last_name="Last",
            hashed_password="hashed_password",
        )
        account.email = "updated@mail.com"
        account.first_name = "Updated"
        account.last_name = "User"
        updated_account = self.repo.update_account(
            account.id,
            account.email,
            account.first_name,
            account.last_name,
            account.hashed_password,
        )
        self.assertIsNotNone(updated_account)
        self.assertEqual(updated_account.email, "updated@mail.com")
        self.assertEqual(updated_account.first_name, "Updated")
        self.assertEqual(updated_account.last_name, "User")

    @mock.patch.object(repository.logger, "error")
    def test_update_account_not_found(self, mock_error_logger):
        fake_account = users.User(
            id=999,
            email="test@mail.com",
            first_name="First",
            last_name="Last",
            hashed_password="hashed_password",
        )
        with self.assertRaises(repository.AccountNotFoundError):
            self.repo.update_account(
                fake_account.id,
                fake_account.email,
                fake_account.first_name,
                fake_account.last_name,
                fake_account.hashed_password,
            )
        mock_error_logger.assert_called_once_with("Account not found for update", account_id=fake_account.id)
