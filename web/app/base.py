import unittest

from fastapi.testclient import TestClient

from web.app.main import create_app


class WebBaseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app = create_app()
        cls.client = TestClient(app)
