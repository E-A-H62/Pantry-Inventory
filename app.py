from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pantry.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class PantryItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<PantryItem {self.item}>'

# Initialize the database
with app.app_context():
    # Delete existing database tables
    db.drop_all()
    # Create table
    db.create_all()

@app.route('/')
def home():
    return render_template('home.html')

# Adding item to database
@app.route('/inventory', methods=['GET', 'POST'])
def inventory():
    if request.method == 'POST':
        item = request.form['item']
        quantity = request.form['quantity']
        new_item = PantryItem(item=item, quantity=int(quantity))
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for('inventory'))
    pantry_items = PantryItem.query.all()
    return render_template('inventory.html', pantry_items=pantry_items)

# Editing item in database
@app.route('/edit', methods=['GET', 'POST'])
def edit():
    if request.method == 'POST':
        item_id = request.form['item_id']
        quantity = request.form['quantity']
        item = PantryItem.query.get(item_id)
        item.quantity = int(quantity)
        db.session.commit()
        return redirect(url_for('edit'))
    pantry_items = PantryItem.query.all()
    return render_template('edit.html', pantry_items=pantry_items)

if __name__ == '__main__':
    app.run(debug=True)
