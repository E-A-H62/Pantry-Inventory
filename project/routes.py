import git
from flask import render_template, request, redirect, url_for, flash  # noqa: F401, E501
from project import app, db  # noqa: F401
from project.models import add_item, edit_item, remove_item  # noqa: F401
from project.models import PantryItem, fetch_item, fetch_item_id, fetch_items
from project.budget import fetch_budget, set_budget, add_budget, sub_budget, fetch_budget_id  # noqa: E501
from project.recipes_api import get_recipes_from_api
from project.authentication import sign_in, sign_up


@app.route("/")
def home():
    # return render_template("home.html", user_id = user_id)
    return render_template("register.html")  # just for now


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")
        # hashed_password = generate_password_hash(password, method="sha256")

        if sign_up(username, password, email):
            user_id = sign_in(username, password)
            budget = set_budget(user_id)  # noqa: F841
            flash("Account created!", category="success")
            return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user_id = sign_in(username, password)

        if user_id:
            return redirect(url_for("inventory", user_id=user_id))

        flash("Create account to login!", category="error")

    return render_template("login.html")


@app.route("/<user_id>/inventory", methods=["GET", "POST"])
def inventory(user_id):
    pantry_items = fetch_items(user_id)

    if request.method == "POST":
        item = request.form["item"]

        item = item.capitalize()

        # get function call to retrieve pricing from name primary key
        item_id = fetch_item_id(item, user_id)

        if not item_id:
            return redirect(url_for("add", item=item, user_id=user_id))

        return redirect(url_for("edit", item_id=item_id, user_id=user_id))

    return render_template("inventory.html",
                           pantry_items=pantry_items, user_id=user_id)


@app.route("/<user_id>/add/<item>", methods=["GET", "POST"])
def add(item, user_id):
    if request.method == "POST":
        quantity = request.form["quantity"]
        price = request.form["price"]

        # add item to database
        add_item(item, quantity, price, user_id)
        flash("Item added", category="success")

        budget_id = fetch_budget_id(user_id)
        budget = fetch_budget(budget_id)
        sub_budget(float(price), budget_id)

        if budget.amount < 0:
            flash("Budget exceeded!", category="error")

        return redirect(url_for("inventory", user_id=user_id))

    return render_template("add_inventory.html", item=item, user_id=user_id)


# needs work to become fully functional
@app.route("/<user_id>/edit/<item_id>", methods=["GET", "POST"])
def edit(item_id, user_id):
    item_object = fetch_item(item_id)

    if request.method == "POST":
        added = int(request.form["added"])
        removed = int(request.form["removed"])
        price = request.form["price"]

        # update item in database
        edit_item(item_id, added - removed, price)
        flash("Item edited!", category="success")

        budget_id = fetch_budget_id(user_id)
        budget = fetch_budget(budget_id)
        sub_budget(float(price), budget_id)

        if budget.amount < 0:
            flash("Budget exceeded!", category="error")

        return redirect(url_for("inventory", user_id=user_id))

    return render_template("edit_inventory.html", item_id=item_id,
                           item_object=item_object, user_id=user_id)


@app.route("/update_server", methods=["POST"])
def webhook():
    user_name = "Your Name"
    user_email = "your.email@example.com"

    if request.method == "POST":
        try:
            repo = git.Repo("/home/PantryInventory/SEO-Project2")

            with repo.config_writer() as git_config:
                git_config.set_value("user", "name", user_name)
                git_config.set_value("user", "email", user_email)

            origin = repo.remotes.origin
            origin.pull()
            return "Updated PythonAnywhere successfully", 200
        except Exception as e:
            print(origin)
            print(e)

    return "Wrong event type", 400


@app.route("/<user_id>/recipes", methods=["GET", "POST"])
def recipes(user_id):
    pantry_items = PantryItem.query.all()
    ingredients = ",".join([item.item for item in pantry_items])
    recipe_data = get_recipes_from_api(ingredients)
    return render_template(
        "recipes.html", recipes=recipe_data, user_id=user_id)


@app.route("/<user_id>/shopping", methods=["GET", "POST"])
def shopping(user_id):
    budget_id = fetch_budget_id(user_id)
    budget = fetch_budget(budget_id)
    pantry_items = fetch_items(user_id)

    if not budget_id:
        budget = set_budget(user_id)

    if request.method == "POST":
        return redirect(url_for(
            "edit_budget", budget=budget, user_id=user_id))

    return render_template("shopping.html", pantry_items=pantry_items,
                           budget=budget, user_id=user_id)


@app.route("/<user_id>/edit_budget/<budget>", methods=["GET", "POST"])
def edit_budget(budget, user_id):

    if request.method == "POST":
        # edit budget here
        action = request.form["action"]
        amount = float(request.form["amount"])

        if action == "Add":
            add_budget(amount, user_id)

        elif action == "Remove":
            sub_budget(amount, user_id)

        return redirect(url_for("shopping", user_id=user_id))

    return render_template("edit_budget.html", budget=budget, user_id=user_id)


if __name__ == "__main__":
    app.run(debug=True)
