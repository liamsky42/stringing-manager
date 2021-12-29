from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Brand, Customer, Racquet
from . import db, get_form_value

views = Blueprint("views", __name__)

@views.route("/")
@login_required
def home():
    return render_template("index.jinja2", user=current_user)


@views.route("/brands", methods=["GET", "POST"])
@login_required
def brands():
    if request.method == "POST":
        name = get_form_value(request.form.get("name"))
        url = get_form_value(request.form.get("url"))

        if (not name) or (not url):
            flash("please fill all required fields", category="error")
        else:
            brand = Brand.query.filter_by(name=name).first()
            if brand:
                flash("brand already exists", category="error")
            else:
                new_brand = Brand(name=name, url=url)
                db.session.add(new_brand)
                db.session.commit()

        return redirect(url_for("views.brands"))

    brands = Brand.query.order_by(Brand.name).all()
    return render_template("brands.jinja2", user=current_user, brands=brands)


@views.route("/customers", methods=["GET", "POST"])
@login_required
def customers():
    if request.method == "POST":
        first_name = get_form_value(request.form.get("first_name"))
        last_name = get_form_value(request.form.get("last_name"))
        racquet_ids = [int(id) for id in request.form.getlist("raquets")]

        racquets_to_add = Racquet.query.filter(Racquet.id.in_(racquet_ids)).all()

        if (not first_name) or (not last_name) or (len(racquet_ids) == 0):
            flash("please fill all required fields", category="error")
        elif len(racquets_to_add) != len(racquet_ids):
            flash("invalid racquet id(s)", category="error")
        else:
            customer = Customer.query.filter_by(first_name=first_name, last_name=last_name).first()
            if customer:
                flash("customer already exists", category="error")
            else:
                new_customer = Customer(first_name=first_name, last_name=last_name)

                for racquet_to_add in racquets_to_add:
                    new_customer.racquets.append(racquet_to_add)

                print(new_customer.racquets)
                db.session.add(new_customer)
                db.session.commit()

        return redirect(url_for("views.customers"))

    customers = Customer.query.all()
    racquets = Racquet.query.join(Brand).order_by(Racquet.release_year.desc(), Brand.name, Racquet.model).all()

    racquets_by_brands = {}
    for racquet in racquets:
        if racquet.brand.name in racquets_by_brands:
            racquets_by_brands[racquet.brand.name].append(racquet)
        else:
            racquets_by_brands[racquet.brand.name] = [racquet]

    return render_template("customers.jinja2", user=current_user, customers=customers, racquets_by_brands=racquets_by_brands)


@views.route("/racquets", methods=["GET", "POST"])
@login_required
def racquets():
    if request.method == "POST":
        brand_id = get_form_value(request.form.get("brand"))
        model = get_form_value(request.form.get("model"))
        release_year = get_form_value(request.form.get("release_year"))

        if (not brand_id) or (not model) or (not release_year):
            flash("please fill all required fields", category="error")

        else:
            racquet = Racquet.query.filter_by(model=model, release_year=release_year, brand_id=brand_id).first()
            if racquet:
                flash("racquet already exists", category="error")
            else:
                new_racquet = Racquet(model=model, release_year=release_year, brand_id=brand_id)
                db.session.add(new_racquet)
                db.session.commit()

        return redirect(url_for("views.racquets"))

    brands = Brand.query.all()
    racquets = Racquet.query.join(Brand).order_by(Racquet.release_year.desc(), Brand.name, Racquet.model).all()
    return render_template("racquets.jinja2", user=current_user, brands=brands, racquets=racquets)
