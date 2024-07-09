from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# A list to store pantry items (for demonstration purposes)
pantry_items = []

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/inventory', methods=['GET', 'POST'])
def inventory():
    if request.method == 'POST':
        item = request.form['item']
        quantity = request.form['quantity']
        pantry_items.append({'item': item, 'quantity': int(quantity)})
        return redirect(url_for('inventory'))
    return render_template('inventory.html', pantry_items=pantry_items)

# needs work to become fully functional
@app.route('/edit', methods=['GET', 'POST'])
def edit():
    if request.method == 'POST':
        item = request.form['item']
        quantity = request.form['quantity']
        for entry in pantry_items:
            if entry.get(item):
                entry[item] = quantity
        return redirect(url_for('edit'))
    return render_template('edit.html', pantry_items=pantry_items)

if __name__ == '__main__':
    app.run(debug=True)