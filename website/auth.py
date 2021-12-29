from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db, is_database_exists, get_form_value
from flask_login import login_user, logout_user, login_required, current_user

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = get_form_value(request.form.get("username"))
        password = get_form_value(request.form.get("password"))

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
        username = get_form_value(request.form.get("username"))
        name = get_form_value(request.form.get("name"))
        password = get_form_value(request.form.get("password"))
        confirmation = get_form_value(request.form.get("confirmation"))

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
