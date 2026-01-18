import os
import tempfile
import unittest
from unittest import mock

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

from accounts.models import base, users
from accounts import repository


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
