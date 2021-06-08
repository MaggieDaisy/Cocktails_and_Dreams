import os
from functools import wraps
from bson.objectid import ObjectId
from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_pymongo import PyMongo
from werkzeug.security import check_password_hash, generate_password_hash
if os.path.exists("env.py"):
    import env
app = Flask(__name__)
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")
mongo = PyMongo(app)


def login_required(f):
    """
    Function decorator for login required information. Brings a safety that
    current view should only be used by users that are logged in. When the user
    goes to the site and is not logged in, it should be redirected to the login
    page.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # checking if current user in session
        if not session.get("user", None):
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function


@app.route("/")
@app.route("/index")
def index():
    """
    The home page where users can get a general orientation about the content
    and idea of app, and read about categories of cocktails that are going to
    be a part of recipes
    """
    categories = list(mongo.db.categories.find())
    return render_template("index.html", categories=categories)


@app.route("/get_recipes")
def get_recipes():
    """
    The cocktails recipes page where users can see whole collection of card
    panels with dream cocktails recipes added by users
    """
    recipes = list(mongo.db.recipes.find())
    return render_template("recipes.html", recipes=recipes)


@app.route("/search", methods=["GET", "POST"])
def search():
    """
    The searching bar where users can search by entering cocktail names or
    ingredients. Database text index was created for recipe_name and
    recipe_ingredients
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
    The registration page allows users to create an account by entering a
    username and password using the required format of the input field
    """
    if request.method == "POST":
        # checking if username already exists in database
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()}
        )
        # displaying alert if username already exist
        if existing_user:
            flash("It looks like Username already exists")
            return redirect(url_for("register"))
        # taking user information and inserts them to database
        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password")),
        }
        mongo.db.users.insert_one(register)
        # putting new user into a 'session' cookie
        session["user"] = request.form.get("username").lower()
        # displaying alert if registration was successful
        flash("Great! It looks like your registration was successful!")
        # bringing user directly the profile page
        return redirect(url_for("profile", username=session["user"]))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    The login page allows users to log in to existing account by entering a
    username and password using the required format of the input field
    """
    if request.method == "POST":
        # checking if username exists in database
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()}
        )
        if existing_user:
            # ensuring that hashed password matches user input
            if check_password_hash(
                existing_user["password"], request.form.get("password")
            ):
                session["user"] = request.form.get("username").lower()
                # displaying welcoming alert for logged in user
                flash("Welcome back, {}".format(request.form.get("username")))
                # bringing user to the current user profile page
                return redirect(url_for("profile", username=session["user"]))
            # displaying alert about invalid password match
            flash("Oops, Looks like Username or/and Password is incorrect")
            # bringing user to the login page to try again
            return redirect(url_for("login"))
        # displaying alert that username does not exist
        flash("Oops, Looks like you are here first time")
        # bringing user to the registration page
        return redirect(url_for("register"))
    return render_template("login.html")


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    """
    The profile page which retrieves the current username session from the
    database. Access to this page is possible only for users with a successful
    login
    """
    # checking current session user and bringing to profile
    if session["user"]:
        recipes = list(mongo.db.recipes.find())
    # bringing user to login page if user not in session
    if not session["user"]:
        return redirect(url_for("login"))
    user = mongo.db.users.find_one({"username": session["user"]})
    # checking if not existing user then brings to register page
    if not user:
        return redirect(url_for("register"))
    # grabbing the session user's username from database
    return render_template(
        "profile.html", username=user["username"], recipes=recipes
    )


@app.route("/logout")
@login_required
def logout():
    """
    The logout function removes the current user from a session. Session
    cookies are being removed from the browser
    """
    # displaying alert about removing using from session
    flash("You have been successfuly logged out")
    session.pop("user")
    # bringing user to the login page
    return redirect(url_for("login"))


@app.route("/add_recipe", methods=["GET", "POST"])
@login_required
def add_recipe():
    """
    The add recipes page, only registered users can create a new cocktail
    recipe. After submission filled form new recipe is going to be added to the
    database
    """
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
        # displaying alert that cocktail recipe was added
        flash("Your Dream Cocktail Recipe Was Successfully Added")
        # bringing user to cocktail recipes collection
        return redirect(url_for("get_recipes"))
    # pulling categories selection from database
    categories = list(mongo.db.categories.find().sort("category_name", 1))
    return render_template("add_recipe.html", categories=categories)


@app.route("/edit_recipe/<recipe_id>", methods=["GET", "POST"])
@login_required
def edit_recipe(recipe_id):
    """
    The edit cocktail recipe page, only logged in author of recipe have a
    possibility to edit and correct it. After submission of prefilled and
    corrected form, a new recipe is going to be searched by its id in the
    database and will be updated to the requested form
    """
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
        # updating corrected recipe by using submit dictionary
        mongo.db.recipes.update({"_id": ObjectId(recipe_id)}, submit)
        # displaying alert that cocktail recipe was updated
        flash("Your Dream Cocktail Recipe Was Successfully Updated")
        return redirect(url_for("get_recipes"))
    # searching in database for corrected recipe by id
    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    categories = mongo.db.categories.find().sort("category_name", 1)
    return render_template(
        "edit_recipe.html", recipe=recipe, categories=categories
    )


@app.route("/delete_recipe/<recipe_id>")
@login_required
def delete_recipe(recipe_id):
    """
    The delete function allows author/user to remove recipe while is checked by
    specific id in the the database
    """
    mongo.db.recipes.remove({"_id": ObjectId(recipe_id)})
    # displaying alert that recipe was deleted
    flash("Your Dream Cocktail Recipe Was Successfully Deleted")
    return redirect(url_for("get_recipes"))


if __name__ == "__main__":
    app.run(
        host=os.environ.get("IP"), port=int(os.environ.get(
            "PORT")), debug=True)
