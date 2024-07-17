from project import app
import sys
import unittest

sys.path.append("../SEO-Project2/project")


class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_main_page(self):
        response = self.app.get("/", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_inventory_page(self):
        response = self.app.get("/inventory", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_add_page(self):
        response = self.app.get("/add/<item>", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_edit_page(self):
        response = self.app.get("/edit/<int:item>", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
