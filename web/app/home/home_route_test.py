from web.app import base


class HomeRouteTest(base.WebBaseTest):

    def test_home_returns_message(self):
        response = self.client.get("/api/home")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Hello, in Jabba pizza"})
