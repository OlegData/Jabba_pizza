import structlog

from sqlalchemy.exc import IntegrityError, OperationalError, SQLAlchemyError
from sqlalchemy.orm import Session

from accounts.models.users import User

logger = structlog.get_logger()


class DuplicateEmailError(Exception):
    pass


class DatabaseError(Exception):
    pass


class AccountRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_account(
        self,
        email: str,
        first_name: str,
        last_name: str,
        hashed_password: str,
    ) -> User:
        with self.session as session:
            existing_user = session.query(User).filter_by(email=email).first()
            if existing_user:
                logger.warning("User already exists", email=email)
                raise DuplicateEmailError("Email already exists")

            new_account = User(
                email=email,
                first_name=first_name,
                last_name=last_name,
                hashed_password=hashed_password,
            )
            session.add(new_account)
            try:
                session.commit()
            except IntegrityError as exc:
                session.rollback()
                logger.error("Failed to create account", error=str(exc), new_account=new_account)
                raise
            session.refresh(new_account)
        return new_account

    def get_account_by_email(self, email: str):
        try:
            with self.session as session:
                account = session.query(User).filter_by(email=email).first()
        except SQLAlchemyError as exc:
            logger.error("Database error while fetching account", error=str(exc), email=email)
            raise DatabaseError("Database error") from exc
        return account
