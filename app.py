from flask import Flask, render_template, request, redirect, url_for, jsonify, flash

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/inventory', methods=['GET', 'POST'])
def inventory():
    # fetch pantry items
    pantry_items = [] # temp

    if request.method == 'POST':
        item = request.form['item']

        if not item:
            flash('Invalid input for item name', "danger")
            return redirect(url_for('inventory'))
        
        # get function call to retrieve pricing from name primary key
        price = 0 # temp

        if price:
            redirect(url_for('add', item = item))
        
        redirect(url_for('edit', item = item))

    return render_template('inventory.html', pantry_items=pantry_items)

@app.route('/add/<item>', methods=['GET', 'POST'])
def add(item):
    if request.method == 'POST':
        quantity = request.form['quantity']
        price = request.form['price']

        # add item to database

        return redirect(url_for('add'), item = item)
    
    return render_template('add_inventory.html', item = item)
    

# needs work to become fully functional
@app.route('/edit/<item>', methods=['GET', 'POST'])
def edit(item):
    if request.method == 'POST':
        added = request.form['added']
        removed = request.form['removed']
        price = request.form['price']

        # update item in database

        return redirect(url_for('edit'), item = item)
    
    return render_template('edit_inventory.html', item = item)
    

if __name__ == '__main__':
    app.run(debug=True)
