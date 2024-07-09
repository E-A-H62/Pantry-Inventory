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
        return f'<PantryItem {self.item}>'
    

    def add_item(self, item_name, quant, price):
        new_item = PantryItem(item=item_name, quantity=int(quant), price=price)
        db.session.add(new_item)
        db.session.commit()
    

    def edit_item(self, item_name, quant):
        item = PantryItem.query.get(item_name)
        item.quantity = int(quant)
        db.session.commit()
    

    def remove_item(self, item_name):
        item = PantryItem.query.get_or_404(item_name)
        db.session.delete(item)
        db.session.commit()


# Initialize the database
with app.app_context():
    # Delete existing database tables
    db.drop_all()
    # Create table
    db.create_all()
