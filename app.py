from flask import (
    Flask,
    render_template,
    request,
    flash,
    redirect,
    url_for,
    abort,
    jsonify,
)
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, migrate
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship
import random
from datetime import datetime
import os

DB_URI = os.environ.get("DB_URI")
SECRET_KEY = os.environ.get("SECRET_KEY")

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY

app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# initialize tables if they don't already exist
# db.create_all()


# User model with relationship to Reviews
class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(1000))
    name = db.Column(db.String(100))

    cafe = relationship("Cafe", back_populates="author")


# CREATE TABLE
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    author = relationship("Users", back_populates="cafe")

    def to_dict(self):
        return {
            column.name: getattr(self, column.name) for column in self.__table__.columns
        }


# Set Login manager
login_manager = LoginManager()
login_manager.init_app(app)


# Context processor for injecting variables into templates
@app.context_processor
def inject_vars():
    # Inject the 'current_user' and 'year' variables into the template context
    return dict(current_user=current_user, year=datetime.now().year)


# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)


# Decorator for restricting access to admin-only routes
def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if the current user is an admin (user ID 1)
        if current_user.id != 1:
            # If not an admin, abort the request with a 403 Forbidden status
            return abort(403)

        # If the current user is an admin, proceed with the original function
        return f(*args, **kwargs)

    # Return the decorated function
    return decorated_function


# Decorator for restricting access to logged-in routes
def logged_in_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if the current user is an admin (user ID 1)
        if not current_user.is_authenticated:
            # If not an admin, abort the request with a 403 Forbidden status
            return abort(403)

        # If the current user is an admin, proceed with the original function
        return f(*args, **kwargs)

    # Return the decorated function
    return decorated_function


@app.route("/")
def home():
    return render_template("index.html")


# Route for user signup
@app.route("/signup", methods=["POST", "GET"])
def signup():
    if current_user.is_authenticated:
        # Redirect to the homepage
        return redirect(url_for("home"))

    if request.method == "POST":
        # Retrieve user input from the signup form
        name = request.form.get("InputName")
        email = request.form.get("InputEmail")
        password = request.form.get("InputPassword")
        user = db.session.execute(db.select(Users).where(Users.email == email)).first()

        # Check if the user with the given email already exists
        if user:
            # If the user already exists, flash a warning and redirect to the login page
            flash("That email already exist, please Login.", "warning")
            return redirect(url_for("login"))
        else:
            # Create a new user and add them to the database
            user = Users(
                name=name,
                email=email,
                password=generate_password_hash(
                    password,
                    method="pbkdf2:sha256",
                    salt_length=16,
                ),
            )
            db.session.add(user)
            db.session.commit()

            # Log in the newly created user
            login_user(user)

            # Redirect to the homepage
            return redirect(url_for("home"))

    # Render the signup form template
    return render_template("signup.html")


# Route for user login
@app.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        # Redirect to the homepage
        return redirect(url_for("home"))

    if request.method == "POST":
        # Retrieve user input from the login form
        email = request.form.get("InputEmail")
        password = request.form.get("InputPassword")

        # Use the query method to get the user object
        user = Users.query.filter_by(email=email).first()

        if not user:
            # If the user does not exist, flash a warning and redirect to the login page
            flash("That email does not exist, please try again.", "warning")
            return redirect(url_for("login"))
        elif not check_password_hash(user.password, password):
            # If the password is incorrect, flash a warning and redirect to the login page
            flash("Password incorrect, please try again.", "warning")
            return redirect(url_for("login"))
        else:
            # If login is successful, log in the user and redirect to the homepage
            login_user(user)
            flash(f"Welcome {user.name}, you are now logged in.", "success")
            return redirect(url_for("home"))

    # Render the login form template
    return render_template("login.html")


# Route for user logout
@app.route("/logout")
def logout():
    if not current_user.is_authenticated:
        # Redirect to the homepage
        return redirect(url_for("home"))
    # Flash a logout message, log out the user, and redirect to the homepage
    flash(f"Goodbye {current_user.name}, you are now logged out.", "success")
    logout_user()
    return redirect(url_for("home"))


@app.route("/random")
def get_random_cafe():
    result = db.session.execute(db.select(Cafe))
    all_cafes = result.scalars().all()
    random_cafe = random.choice(all_cafes)
    return jsonify(
        cafe=random_cafe.to_dict()
        | {"author_name": random_cafe.author.name if random_cafe.author else None}
    )


@app.route("/all")
def get_all_cafes():
    result = db.session.execute(db.select(Cafe).order_by(Cafe.name))
    all_cafes = result.scalars().all()
    if all_cafes:
        return jsonify(
            cafes=[
                cafe.to_dict()
                | {"author_name": cafe.author.name if cafe.author else None}
                for cafe in all_cafes
            ]
        )
    else:
        return (
            jsonify(cafes={"error": {"Not Found": "Sorry, no cafes in the database."}}),
            404,
        )


@app.route("/search_loc")
def get_cafe_by_location():
    search_input = request.args.get("loc")
    all_cafes = (
        db.session.query(Cafe).filter(Cafe.location.ilike(f"%{search_input}%")).all()
    )
    if all_cafes:

        return jsonify(
            cafes=[
                cafe.to_dict()
                | {"author_name": cafe.author.name if cafe.author else None}
                for cafe in all_cafes
            ]
        )
    else:
        return (
            jsonify(
                cafes={
                    "error": {
                        "Not Found": "Sorry, we don't have a cafe in that location."
                    }
                }
            ),
            404,
        )


@app.route("/search_name")
def get_cafe_by_name():
    search_input = request.args.get("name")
    all_cafes = (
        db.session.query(Cafe).filter(Cafe.name.ilike(f"%{search_input}%")).all()
    )
    if all_cafes:
        return jsonify(
            cafes=[
                cafe.to_dict()
                | {"author_name": cafe.author.name if cafe.author else None}
                for cafe in all_cafes
            ]
        )
    else:
        return (
            jsonify(
                cafes={
                    "error": {
                        "Not Found": "Sorry, we don't have a cafe with that name."
                    }
                }
            ),
            404,
        )


@app.route("/add", methods=["POST"])
@logged_in_only
def post_new_cafe():
    name = request.form.get("name")
    if db.session.query(Cafe).filter(Cafe.name == name).first():
        flash(f"Sorry, a cafe with the name {name} already exists.", "warning")
        return redirect(url_for("add_cafe"))
    else:
        new_cafe = Cafe(
            name=name,
            map_url=request.form.get("map_url"),
            img_url=request.form.get("img_url"),
            location=request.form.get("loc"),
            has_sockets=bool(request.form.get("sockets")),
            has_toilet=bool(request.form.get("toilet")),
            has_wifi=bool(request.form.get("wifi")),
            can_take_calls=bool(request.form.get("calls")),
            seats=request.form.get("seats"),
            coffee_price=request.form.get("coffee_price"),
            author=current_user,
        )
        db.session.add(new_cafe)
        db.session.commit()
        flash(f"Cafe {name} have been posted.", "success")
        return redirect(url_for("home"))


@app.route("/add-cafe", methods=["POST", "GET"])
@logged_in_only
def add_cafe():
    if request.method == "GET":
        return render_template("add.html")


@app.route("/edit-cafe/<int:cafe_id>", methods=["POST", "GET"])
@logged_in_only
def edit_cafe(cafe_id):
    cafe = db.session.get(Cafe, cafe_id)
    if cafe.author_id != current_user.id and current_user.id != 1:
        return abort(403)
    if request.method == "POST":
        name = request.form.get("name")
        if db.session.query(Cafe).filter(Cafe.name == name).first():
            flash(f"Sorry, a cafe with the name {name} already exists.", "warning")
        else:
            cafe.coffee_price = f"{request.form.get("coffee_price")} {request.form.get("currency_symbol")}"
            cafe.name = name
            cafe.map_url = request.form.get("map_url")
            cafe.img_url = request.form.get("img_url")
            cafe.location = request.form.get("location")
            cafe.has_sockets = bool(request.form.get("sockets"))
            cafe.has_toilet = bool(request.form.get("toilet"))
            cafe.has_wifi = bool(request.form.get("wifi"))
            cafe.can_take_calls = bool(request.form.get("calls"))
            cafe.seats = request.form.get("seats")
            db.session.commit()
            flash(f"Cafe {name} have been updated.", "success")
            return redirect(url_for("home"))

    return render_template("edit.html", cafe=cafe)


# Deletes a cafe with a particular id. Change the request type to "Delete" in Postman
@app.route("/report-closed/<int:cafe_id>", methods=["POST"])
@admin_only
def delete_cafe(cafe_id):
    cafe = db.get(Cafe, cafe_id)
    if cafe:
        db.session.delete(cafe)
        db.session.commit()
        flash("Successfully deleted the cafe from the database.", "success")
        return redirect(url_for("home"))
    else:
        flash("Sorry a cafe with that id was not found in the database.", "warning")
        return redirect(url_for("home"))

@app.route("/api-info")
def api_info():
    return render_template("api-info.html")

if __name__ == "__main__":
    app.run(debug=True)
