from flask import render_template, request, redirect, url_for, flash
from project import app, db
from project.models import PantryItem, add_item, remove_item, edit_item, fetch_item, fetch_items
from project.recipes_api import get_recipes_from_api

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/inventory", methods=["GET", "POST"])
def inventory():
    pantry_items = fetch_items()

    if request.method == "POST":
        item = request.form["item"]

        # get function call to retrieve pricing from name primary key
        item_object = fetch_item(item)
        
        if not item_object:
            return redirect(url_for("add", item=item))

        return redirect(url_for("edit", item=item))

    return render_template("inventory.html", pantry_items=pantry_items)


@app.route("/add/<item>", methods=["GET", "POST"])
def add(item):
    if request.method == "POST":
        quantity = request.form["quantity"]
        price = request.form["price"]

        # add item to database
        add_item(item, quantity, price)

        return redirect(url_for("inventory"))

    return render_template("add_inventory.html", item=item)


# needs work to become fully functional
@app.route("/edit/<item>", methods=["GET", "POST"])
def edit(item):
    item_object = fetch_item(item)

    if request.method == "POST":
        added = int(request.form["added"])
        removed = int(request.form["removed"])
        price = request.form["price"]

        # update item in database
        edit_item(item, added-removed, price)

        return redirect(url_for("inventory"))

    return render_template("edit_inventory.html", item=item, item_object=item_object)

@app.route("/recipes", methods=["GET", "POST"])
def recipes():
    pantry_items = PantryItem.query.all()
    ingredients = ",".join([item.item for item in pantry_items])
    recipe_data = get_recipes_from_api(ingredients)
    return render_template("recipes.html", recipes=recipe_data)

if __name__ == "__main__":
    app.run(debug=True)
