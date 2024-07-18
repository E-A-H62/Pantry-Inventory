from project import app, db
from project.models import add_user
import sys
import unittest

sys.path.append("../SEO-Project2/project")


class TestApp(unittest.TestCase):

    def setUp(self):
        # Set up the test client and initialize the database.
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()
        add_user(username="testuser",
                 password="password", email="test@example.com")

    def tearDown(self):
        # Remove the app context.
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_main_page(self):
        response = self.app.get("/", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_inventory_page(self):
        response = self.app.get("/<user_id>/inventory", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_add_page(self):
        response = self.app.get("/<user_id>/add/<item>", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_edit_page(self):
        response = self.app.get(
            "/<user_id>/edit/<int:item>", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_shopping_page(self):
        response = self.app.get(
            "/<user_id>/edit/<int:item>", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_budget_page(self):
        response = self.app.get(
            "/<user_id>/edit/<int:item>", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
