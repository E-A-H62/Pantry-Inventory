from project import app, db

class PantryItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable = False)

    def __repr__(self):
        return f'<PantryItem {self.item} (x{self.quantity}) cost ${self.price}>'
    

def add_item(item_name, quant, price):
    new_item = PantryItem(item=item_name, quantity=int(quant), price=float(price))
    db.session.add(new_item)
    db.session.commit()
    

def edit_item(item_name, quant, price):
    item = db.session.query(PantryItem).filter_by(item=item_name).first()
    if item:
        item.quantity += quant
        item.price = float(price)
        db.session.commit()
    else:
        print("Item not found.")
    

def remove_item(item_name):
    item = db.session.query(PantryItem).filter_by(item=item_name).first()
    db.session.delete(item)
    db.session.commit()

def fetch_item(item_name): 
    return db.session.query(PantryItem).filter_by(item=item_name).first()

def fetch_items():
    return db.session.query(PantryItem).all()


# Initialize the database
with app.app_context():
    # Delete existing database tables
    # db.drop_all()
    # Create table
    db.create_all()

'''
    # Testing the database functions
    add_item(item_name="Milk", quant=1, price=2.8)
    add_item(item_name="Eggs", quant=12, price=6.3)
    print(PantryItem.query.all())

    edit_item(item_name="Eggs", quant=10)
    print(PantryItem.query.all())

    remove_item(item_name="Milk")
    print(PantryItem.query.all())
'''