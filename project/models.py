from project import app, db


class PantryItem(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    unit = db.Column(db.String(100), nullable=False)
    expiration = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"{self.item}"


class User(db.Model):
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)


class Budget(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    amount = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"{self.amount:.2f}"


class SavedRecipe(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    api_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(250), nullable=False)
    image = db.Column(db.String(250), nullable=False)
    likes = db.Column(db.Integer, nullable=False)
    used_ingredients = db.Column(db.Text, nullable=False)  # Store as JSON string
    missed_ingredients = db.Column(db.Text, nullable=False)  # Store as JSON string
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    user = db.relationship('User', backref=db.backref('saved_recipes', lazy=True))

    
def add_item(item_name, quant, price, user_id):
    new_item = PantryItem(
        item=item_name, quantity=int(quant), price=float(price), user_id=user_id, unit="(Unit not yet set)", expiration="(Expiration not yet set)"
    )
    db.session.add(new_item)
    db.session.commit()


def edit_item(item_id, quant, price):
    item = fetch_item(item_id)
    if item:
        item.quantity += quant
        item.price = float(price)
        db.session.commit()
    else:
        print("Item not found.")


def edit_unit(item_id, unit):
    item = fetch_item(item_id)
    if item:
        item.unit = unit
        db.session.commit()


def edit_expiration(item_id, expiration):
    item = fetch_item(item_id)
    if item:
        item.expiration = expiration
        db.session.commit()


def remove_item(item_id):
    item = fetch_item(item_id)
    db.session.delete(item)
    db.session.commit()


def fetch_item(item_id):
    return db.session.get(PantryItem, item_id)


def fetch_item_id(item_name, user_id):
    item = (
        db.session.query(PantryItem).filter_by(item=item_name, user_id=user_id).first()
    )

    return item.id if item else item


def fetch_items(user_id):
    return db.session.query(PantryItem).filter_by(user_id=user_id).all()


def fetch_user(user_id):
    return db.session.get(User, user_id)


def fetch_user_id(username, password):
    user = (
        db.session.query(User).filter_by(username=username, password=password).first()
    )

    return user.user_id if user else user


def add_user(username, password, email):
    if not fetch_user_id(username, password):
        new_user = User(username=username, password=password, email=email)
        db.session.add(new_user)
        db.session.commit()
        return True

    return False


# Initialize the database
with app.app_context():
    # Delete existing database tables
    # db.drop_all()
    # Create table
    db.create_all()
