from flask import Flask, render_template, request, redirect, url_for, jsonify, flash

app = Flask(__name__)


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

@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":

        # something

        # redirect
        return redirect(url_for("search"))
    
    # return the render template


if __name__ == "__main__":
    app.run(debug=True)
