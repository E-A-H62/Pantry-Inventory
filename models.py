from flask_sqlalchemy import SQLAlchemy
from app import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pantry.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class PantryItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable = False)

    def __repr__(self):
        return f'<PantryItem {self.item} (x{self.quantity}) cost ${self.price}>'
    

def add_item(item_name, quant, price):
    new_item = PantryItem(item=item_name, quantity=int(quant), price=price)
    db.session.add(new_item)
    db.session.commit()
    

def edit_item(item_name, quant):
    item = db.session.query(PantryItem).filter_by(item=item_name).first()
    if item:
        item.quantity = int(quant)
        db.session.commit()
    else:
        print("Item not found.")
    

def remove_item(item_name):
    item = db.session.query(PantryItem).filter_by(item=item_name).first()
    db.session.delete(item)
    db.session.commit()


# Initialize the database
with app.app_context():
    # Delete existing database tables
    db.drop_all()
    # Create table
    db.create_all()

    # Testing the database functions
    add_item(item_name="Milk", quant=1, price=2.8)
    add_item(item_name="Eggs", quant=12, price=6.3)
    print(PantryItem.query.all())

    edit_item(item_name="Eggs", quant=10)
    print(PantryItem.query.all())

    remove_item(item_name="Milk")
    print(PantryItem.query.all())
