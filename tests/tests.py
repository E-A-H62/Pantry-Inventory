from project import app, db
from project.models import User, PantryItem
from project.models import (
    add_item,
    edit_item,
    remove_item,
    fetch_item,
    fetch_item_id,
    fetch_user_id,
    add_user,
)  # noqa: E501
import sys
import unittest

sys.path.append("../SEO-Project2/project")


class TestModels(unittest.TestCase):
    def setUp(self):
        # Set up the test client and initialize the database.
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()

    def tearDown(self):
        # Remove the app context.
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    # Testing the database functions
    def test_add_item(self):
        add_item(item_name="Milk", quant=1, price=2.8, user_id=123)
        milk = PantryItem.query.filter_by(item="Milk").first()
        self.assertIsNotNone(milk)
        self.assertEqual(milk.quantity, 1)
        self.assertEqual(milk.price, 2.8)
        self.assertEqual(milk.user_id, 123)

    def test_edit_item(self):
        add_item(item_name="Milk", quant=1, price=2.8, user_id=123)
        milk = PantryItem.query.filter_by(item="Milk").first()
        item_id = milk.id

        edit_item(item_id=item_id, quant=2, price=3.5)
        edited_milk = PantryItem.query.get(item_id)
        self.assertEqual(edited_milk.quantity, 3)
        self.assertEqual(edited_milk.price, 3.5)

    def test_remove_item(self):
        add_item(item_name="Milk", quant=1, price=2.8, user_id=123)
        milk = PantryItem.query.filter_by(item="Milk").first()
        item_id = milk.id

        remove_item(item_id=item_id)
        removed_milk = PantryItem.query.get(item_id)
        self.assertIsNone(removed_milk)

    def test_fetch_item(self):
        add_item(item_name="Milk", quant=1, price=2.8, user_id=123)
        milk = PantryItem.query.filter_by(item="Milk").first()
        item_id = milk.id
        fetched_item = fetch_item(item_id=item_id)

        self.assertEqual(fetched_item.item, "Milk")
        self.assertEqual(fetched_item.quantity, 1)
        self.assertEqual(fetched_item.price, 2.8)

    def test_fetch_item_id(self):
        add_item(item_name="Milk", quant=1, price=2.8, user_id=123)
        item_id = fetch_item_id(item_name="Milk", user_id=123)
        self.assertIsNotNone(item_id)

    def test_fetch_user_id(self):
        add_user(username="testuser", password="password", email="test@example.com")
        user_id = fetch_user_id(username="testuser", password="password")
        self.assertIsNotNone(user_id)

    def test_add_user(self):
        result = add_user(
            username="newuser", password="newpassword", email="new@example.com"
        )
        self.assertTrue(result)
        new_user = User.query.filter_by(username="newuser").first()
        self.assertIsNotNone(new_user)
