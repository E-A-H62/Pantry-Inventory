from project import app, db
from project.models import PantryItem, add_item, edit_item, remove_item
import sys
import unittest
sys.path.append('../SEO-Project2/project')


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
        add_item(item_name="Milk", quant=1, price=2.8)
        milk = PantryItem.query.filter_by(item="Milk").first()
        self.assertIsNotNone(milk)
        self.assertEqual(milk.quantity, 1)
        self.assertEqual(milk.price, 2.8)

    def test_edit_item(self):
        add_item(item_name="Eggs", quant=12, price=6.3)
        edit_item(item_name="Eggs", quant=10, price=3.4)
        eggs = PantryItem.query.filter_by(item="Eggs").first()
        self.assertIsNotNone(eggs)
        self.assertEqual(eggs.quantity, 22)
        self.assertEqual(eggs.price, 3.4)

    def test_remove_item(self):
        add_item(item_name="Milk", quant=1, price=2.8)
        remove_item(item_name="Milk")
        milk = PantryItem.query.filter_by(item="Milk").first()
        self.assertIsNone(milk)
