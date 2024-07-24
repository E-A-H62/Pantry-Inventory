import git
import json
from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash,
)
from project import app, db
from project.models import (
    add_item,
    edit_item,
    remove_item,
    edit_unit,
    check_unique_email
)
from project.models import (  # noqa: F401
    PantryItem,
    SavedRecipe,
    fetch_item,
    fetch_item_id,
    fetch_items,
    fetch_user,
)
from project.budget import (
    fetch_budget,
    set_budget,
    add_budget,
    sub_budget,
    fetch_budget_id,
)
from project.recipes_api import get_recipes_from_api
from project.user import (
    sign_in,
    sign_up,
    change_email,
    change_password,
    change_username,
)


@app.route("/")
def home():
    # return render_template("home.html", user_id = user_id)
    # return render_template("register.html")
    return render_template("welcome.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")
        # hashed_password = generate_password_hash(password, method="sha256")

        if sign_up(username, password, email):
            user_id = sign_in(username, password)
            set_budget(user_id)  # noqa: F841
            flash("Account created!", category="success")
            return redirect(url_for("login"))

        flash("Error: Account already associated with this email", category="error")

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

    return render_template("inventory.html", pantry_items=pantry_items, user_id=user_id)


@app.route("/<user_id>/add/<item>", methods=["GET", "POST"])
def add(item, user_id):
    if request.method == "POST":
        quantity = request.form["quantity"]
        price = request.form["price"]
        unit = request.form["unit"]
        budget_id = fetch_budget_id(user_id)
        budget = fetch_budget(budget_id)

        if int(quantity) < 0:
            flash("Adding an invalid amount!", category="error")
            return redirect(url_for("inventory", user_id=user_id))

        if float(budget.amount) - float(price) < 0:
            flash("You will exceed your budget! Please set a new amount to your budget before proceeding.", category="error")
            return redirect(url_for("inventory", user_id=user_id))

        # add item to database
        add_item(item, quantity, price, user_id)
        item_id = fetch_item_id(item, user_id)
        flash("Item added", category="success")

        sub_budget(float(price), budget_id)

        if unit:
            edit_unit(item_id, unit)

        return redirect(url_for("inventory", user_id=user_id))

    return render_template("add_inventory.html", item=item, user_id=user_id)


# needs work to become fully functional
@app.route("/<user_id>/edit/<item_id>", methods=["GET", "POST"])
def edit(item_id, user_id):
    item_object = fetch_item(item_id)

    if request.method == "POST":
        added = int(request.form["added"])
        removed = int(request.form["removed"])
        price = float(request.form["price"])
        unit = request.form["unit"]

        # update item in database
        if item_object.quantity - removed < 0:
            flash("You do not have enough of this item to remove!", category="error")
            return redirect(url_for("inventory", user_id=user_id))

        if price < 0:
            flash("Invalid price for items", category="error")
            return redirect(url_for("inventory", user_id=user_id))

        edit_item(item_id, added - removed, price)
        flash("Item edited!", category="success")

        budget_id = fetch_budget_id(user_id)
        budget = fetch_budget(budget_id)
        sub_budget(price, budget_id)

        if budget.amount < 0:
            flash("Budget exceeded!", category="error")

        if unit:
            edit_unit(item_id, unit)

        return redirect(url_for("inventory", user_id=user_id))

    return render_template(
        "edit_inventory.html", item_id=item_id, item_object=item_object, user_id=user_id
    )


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


@app.route('/<user_id>/save_recipe', methods=['POST'])
def save_recipe(user_id):
    api_id = request.form.get('api_id')
    title = request.form.get('title')
    image = request.form.get('image')
    likes = request.form.get('likes')

    used_ingredients = json.dumps(request.form.getlist('usedIngredients'))
    missed_ingredients = json.dumps(request.form.getlist('missedIngredients'))

    existing_recipe = SavedRecipe.query.filter_by(api_id=api_id, user_id=user_id).first()
    if not existing_recipe:
        new_recipe = SavedRecipe(
            api_id=api_id, title=title, image=image, likes=likes,
            used_ingredients=used_ingredients, missed_ingredients=missed_ingredients,
            user_id=user_id
        )
        db.session.add(new_recipe)
        db.session.commit()

    flash('Recipe saved!', 'success')
    return redirect(url_for('recipes', user_id=user_id))


@app.route('/<user_id>/unsave_recipe/<int:recipe_id>', methods=['POST'])
def unsave_recipe(user_id, recipe_id):
    saved_recipe = SavedRecipe.query.filter_by(id=recipe_id, user_id=user_id).first()
    if saved_recipe:
        db.session.delete(saved_recipe)
        db.session.commit()
        flash('Recipe unsaved!', 'success')
    return redirect(url_for('saved_recipes', user_id=user_id))


@app.route('/<user_id>/saved_recipes')
def saved_recipes(user_id):
    saved_recipes = SavedRecipe.query.filter_by(user_id=user_id).all()
    recipes = [saved_recipe for saved_recipe in saved_recipes]
    return render_template('saved_recipes.html', recipes=recipes, user_id=user_id)


@app.route("/<user_id>/recipes", methods=["GET", "POST"])
def recipes(user_id):
    pantry_items = fetch_items(user_id)
    ingredients = ",".join([item.item for item in pantry_items])
    recipe_data = get_recipes_from_api(ingredients)
    return render_template("recipes.html", recipes=recipe_data, user_id=user_id)


@app.route("/<user_id>/shopping", methods=["GET", "POST"])
def shopping(user_id):
    # displays budget for user
    budget_id = fetch_budget_id(user_id)
    budget = fetch_budget(budget_id)
    pantry_items = fetch_items(user_id)

    if not budget_id:
        budget = set_budget(user_id)

    if request.method == "POST":
        return redirect(url_for("edit_budget", budget=budget, user_id=user_id))

    return render_template(
        "shopping.html", pantry_items=pantry_items, budget=budget, user_id=user_id
    )


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


@app.route("/<user_id>/profile", methods=["GET"])
def profile(user_id):
    user = fetch_user(user_id)
    return render_template(
        "user_profile.html", user_id=user_id, username=user.username, email=user.email
    )


@app.route("/<user_id>/username", methods=["GET", "POST"])
def update_username(user_id):
    user = fetch_user(user_id)

    if request.method == "POST":
        new_username = request.form["username"]
        password = request.form["password"]

        if user.password == password:
            change_username(user_id, new_username)
            return redirect(url_for("profile", user_id=user_id))

        # notify the user that the password was incorrect
        flash("Error: Invalid Password. Please try again.", category="error")

    return render_template(
        "username_change.html",
        user_id=user_id,
        username=user.username,
        email=user.email,
    )


@app.route("/<user_id>/email", methods=["GET", "POST"])
def update_email(user_id):
    user = fetch_user(user_id)

    if request.method == "POST":
        new_email = request.form["email"]
        password = request.form["password"]

        if user.password == password:
            if not check_unique_email(new_email):
                change_email(user_id, new_email)
                return redirect(url_for("profile", user_id=user_id))

            flash("Error: Email is already associated with another account", category="error")

        else:
            # notify the user that the password was incorrect
            flash("Error: Invalid Password. Please try again.", category="error")

    return render_template(
        "email_change.html", user_id=user_id, username=user.username, email=user.email
    )


@app.route("/<user_id>/password", methods=["GET", "POST"])
def update_password(user_id):
    user = fetch_user(user_id)

    if request.method == "POST":
        new_password = request.form["new_password"]
        password = request.form["password"]

        if user.password == password:
            change_password(user_id, new_password)
            return redirect(url_for("profile", user_id=user_id))

        # notify the user that the password was incorrect
        flash("Error: Invalid Password. Please try again.", category="error")

    return render_template(
        "password_change.html",
        user_id=user_id,
        username=user.username,
        email=user.email,
    )


@app.route("/<user_id>/cart", methods=["GET", "POST"])
def cart(user_id):
    # edits items in carts
    pantry_items = fetch_items(user_id)

    if request.method == "POST":
        action = request.form["action"]
        item_id = request.form["item_id"]

        if action == "Add":
            return redirect(url_for("edit", item_id=item_id, user_id=user_id))

        elif action == "Remove":
            remove_item(item_id)

        elif action == "Both":
            unit = request.form["unit"]

            if unit:
                edit_unit(item_id, unit)

        return redirect(url_for('cart', user_id=user_id))

    return render_template(
        "cart.html", pantry_items=pantry_items, user_id=user_id)


if __name__ == "__main__":
    app.run(debug=True)
