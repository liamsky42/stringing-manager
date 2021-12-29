from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db, is_database_exists
from .form_helpers import form_value_to_string

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = form_value_to_string(request.form.get("username"))
        password = form_value_to_string(request.form.get("password"))

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Login successful", category="success")
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash("Invalid username or password", category="error")
        else:
            flash("Invalid username or password", category="error")
    elif len(User.query.all()) == 0:
        return redirect(url_for("auth.sign_up"))

    return render_template("login.jinja2", user=current_user)


@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        username = form_value_to_string(request.form.get("username"))
        name = form_value_to_string(request.form.get("name"))
        password = form_value_to_string(request.form.get("password"))
        confirmation = form_value_to_string(request.form.get("confirmation"))

        user = User.query.filter_by(username=username).first()

        if user:
            flash("Username already exists", category="error")

        if (not username) or (not password) or (not confirmation):
            flash("must fill all", category="error")
        elif password != confirmation:
            flash("the password and the confirmation should be the same", category="error")
        else:
            new_user = User(username=username, name=name, password=generate_password_hash(
                password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash("user created successfuly!", category="success")
            return redirect(url_for("views.home"))

    return render_template("sign-up.jinja2", user=current_user)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
