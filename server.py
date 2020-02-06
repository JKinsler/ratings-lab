"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
                   session)
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db



app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    return render_template("homepage.html")

@app.route("/users")
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)


@app.route("/register_user", methods=["GET"])
def show_form():
    """Get email and password from users."""
    
    return render_template("register_user.html")


@app.route("/register_user", methods=["POST"])
def get_user_info():
    """Get email and password from users."""
    email = request.form.get("email")
    print(email)
    password = request.form.get("password")
    print(password)

    test_email = User.query.filter_by(email=email).first()
    if test_email is None:
        user = User(email=email, password=password)
        db.session.add(user)
        db.session.commit()
    else:
        print('Please register with a different email address')

    return redirect("/")

@app.route("/register_user", methods=["POST"])
def get_user_info():
    """Get email and password from users."""
    email = request.form.get("email")
    print(email)
    password = request.form.get("password")
    print(password)

    test_email = User.query.filter_by(email=email).first()
    if test_email is None:
        user = User(email=email, password=password)
        db.session.add(user)
        db.session.commit()
    else:
        print('Please register with a different email address')

    return redirect("/")


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
