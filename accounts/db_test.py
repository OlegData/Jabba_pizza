import os

import unittest
from sqlalchemy.engine import URL

os.environ["DB_URL"] = "sqlite:///:memory:"
from accounts import db


class TestDatabase(unittest.TestCase):
    def test_database_connection(self):
        engine = db.create_engine("sqlite:///:memory:")
        Session = db.sessionmaker(bind=engine)
        session = Session()

        self.assertIsNotNone(session)

        session.close()

    def test_get_db_url(self):
        expected_url = URL.create(
            "mysql+pymysql",
            username="jabba",
            password="hutt",
            host="127.0.0.1",
            port="3306",
            database="accounts",
        )
        url = db.get_db_url()
        self.assertEqual(url, expected_url)
