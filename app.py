from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
import requests

app = Flask(__name__)
API_KEY = "db449bea6c7a42b1b91ea196b0cd41b1"

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/inventory", methods=["GET", "POST"])
def inventory():
    # fetch pantry items
    pantry_items = ["water", "milk"]  # temp

    if request.method == "POST":
        item = request.form["item"]

        print(item)

        # get function call to retrieve pricing from name primary key
        price = 1  # temp

        if price:
            return redirect(url_for("add", item=item))

        return redirect(url_for("edit", item=item))

    return render_template("inventory.html", pantry_items=pantry_items)


@app.route("/add/<item>", methods=["GET", "POST"])
def add(item):
    if request.method == "POST":
        quantity = request.form["quantity"]
        price = request.form["price"]

        # add item to database
        print(quantity, price)

        return redirect(url_for("inventory"))

    return render_template("add_inventory.html", item=item)


# needs work to become fully functional
@app.route("/edit/<int:item>", methods=["GET", "POST"])
def edit(item):
    if request.method == "POST":
        added = request.form["added"]
        removed = request.form["removed"]
        price = request.form["price"]

        # update item in database
        print(added, removed, price)
        print(item)
        return redirect(url_for("inventory"))

    return render_template("edit_inventory.html", item=item)

@app.route("/recipes", methods=["GET"])
def recipes():
    ingredients = 'apples,flour,sugar'  # Example ingredients
    recipe_data = get_recipes_from_api(ingredients)
    return render_template("recipes.html", recipes=recipe_data)

def get_recipes_from_api(ingredients):
    api_url = "https://api.spoonacular.com/recipes/findByIngredients"
    api_key = API_KEY
    params = {
        'apiKey': api_key,
        'ingredients': ingredients,
        'number': 4,  # Number of recipes to return
        'ranking': 1, # change to 2 if want to minimize missing ingredients
        'ignorePantry': True
    }
    response = requests.get(api_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return []

if __name__ == "__main__":
    app.run(debug=True)
