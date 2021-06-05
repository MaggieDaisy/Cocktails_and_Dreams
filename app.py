import os
from flask import Flask, flash, render_template, redirect, request, session, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

if os.path.exists("env.py"):
    import env
app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
@app.route("/index")
def index():
    """
    Users can get a general orientation about the content
    of the landing page, and read about categories
    of cocktails that are going to be a part of recipes
    """
    categories = list(mongo.db.categories.find())
    return render_template("index.html", categories=categories)


@app.route("/get_recipes")
def get_recipes():
    """
    Users can see whole collection of card panels 
    with cocktails recipes added by admin and 
    other users
    """
    recipes = list(mongo.db.recipes.find())
    return render_template("recipes.html", recipes=recipes)


@app.route("/search", methods=["GET", "POST"])
def search():
    """
    The searching bar where users can search by 
    entering cocktail names or ingredients. 
    Database text index was created for
	recipe_name and recipe_ingredients
    """
    # pulling input from searching bar
    query = request.form.get("query")
    # searching for text index
    recipes = list(mongo.db.recipes.find({"$text": {"$search": query}}))
    # bringing user to the recipes page with filtered data
    return render_template("recipes.html", recipes=recipes)


@app.route("/register", methods=["GET", "POST"])
def register():
    """
	 The registration page allows users to create 
     an account by entering a username and password 
     using the required format of the input field
	"""
    if request.method == "POST":
        # checking if username already exists in database
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()}
        )

        if existing_user:
            flash("It looks like Username already exists")
            return redirect(url_for("register"))
        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password")),
        }
        mongo.db.users.insert_one(register)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Great! It looks like your registration was successful!")
        return redirect(url_for("profile", username=session["user"]))
    return render_template("register.html")


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("user", None):
            return redirect(url_for("login"))
        return f(*args, **kwargs)

    return decorated_function


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if username exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()}
        )

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                existing_user["password"], request.form.get("password")
            ):
                session["user"] = request.form.get("username").lower()
                flash("Welcome back, {}".format(request.form.get("username")))
                return redirect(url_for("profile", username=session["user"]))
            else:
                # invalid password match
                flash("Oops, Looks like Username or/and Password is incorrect")
                return redirect(url_for("login"))
        else:
            # username does not exist
            flash("Oops, Looks like you are here first time")
            return redirect(url_for("register"))
    return render_template("login.html")


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    if session["user"]:
        recipes = list(mongo.db.recipes.find())
    if not session["user"]:
        return redirect(url_for("login"))
    user = mongo.db.users.find_one({"username": session["user"]})
    if not user:
        return redirect(url_for("register"))
    # grab the session user's username from database
    return render_template("profile.html", username=user["username"], recipes=recipes)


@app.route("/logout")
@login_required
def logout():
    # remove user form session cookies
    flash("You have been successfuly logged out")
    session.pop("user")
    return redirect(url_for("login"))


@app.route("/add_recipe", methods=["GET", "POST"])
@login_required
def add_recipe():
    if request.method == "POST":
        recipe = {
            "category_name": request.form.get("category_name"),
            "recipe_name": request.form.get("recipe_name"),
            "recipe_description": request.form.get("recipe_description"),
            "recipe_ingredients": request.form.get("recipe_ingredients"),
            "recipe_steps": request.form.get("recipe_steps"),
            "recipe_tools": request.form.get("recipe_tools"),
            "recipe_picture": request.form.get("recipe_picture"),
            "created_by": session["user"],
        }
        mongo.db.recipes.insert_one(recipe)
        flash("Your Dream Cocktail Recipe Was Successfully Added")
        return redirect(url_for("get_recipes"))
    categories = list(mongo.db.categories.find().sort("category_name", 1))
    return render_template("add_recipe.html", categories=categories)


@app.route("/edit_recipe/<recipe_id>", methods=["GET", "POST"])
@login_required
def edit_recipe(recipe_id):
    if request.method == "POST":
        submit = {
            "category_name": request.form.get("category_name"),
            "recipe_name": request.form.get("recipe_name"),
            "recipe_description": request.form.get("recipe_description"),
            "recipe_ingredients": request.form.get("recipe_ingredients"),
            "recipe_steps": request.form.get("recipe_steps"),
            "recipe_tools": request.form.get("recipe_tools"),
            "recipe_picture": request.form.get("recipe_picture"),
            "created_by": session["user"],
        }
        mongo.db.recipes.update({"_id": ObjectId(recipe_id)}, submit)
        flash("Your Dream Cocktail Recipe Was Successfully Updated")
        return redirect(url_for("get_recipes"))
    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    categories = mongo.db.categories.find().sort("category_name", 1)
    return render_template("edit_recipe.html", recipe=recipe, categories=categories)


@app.route("/delete_recipe/<recipe_id>")
@login_required
def delete_recipe(recipe_id):
    mongo.db.recipes.remove({"_id": ObjectId(recipe_id)})
    flash("Your Dream Cocktail Recipe Was Successfully Deleted")
    return redirect(url_for("get_recipes"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"), port=int(os.environ.get("PORT")), debug=True)