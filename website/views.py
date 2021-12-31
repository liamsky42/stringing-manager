from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import func, or_
from .models import group_racquets_by_brand, Brand, Customer, Racquet, Stringing, Payment
from . import db
from .form_helpers import form_value_to_string, form_value_to_int, form_value_to_float, form_value_to_bool, \
    form_value_to_datetime

views = Blueprint("views", __name__)


@views.route("/")
@login_required
def home():
    # Customer data
    customers = Customer.query.all()
    customers_chart_data = {
        "names": [],
        "stringings": []
    }

    for customer in customers:
        customers_chart_data["names"].append(customer.full_name())
        customers_chart_data["stringings"].append(len(customer.stringings))

    # Racquets data
    racquets = Racquet.query.join(Brand).order_by(Racquet.release_year.desc(), Brand.name, Racquet.model).all()
    racquets_by_brands = group_racquets_by_brand(racquets)

    racquets_chart_data = {
        "brands": [],
        "racquets": []
    }

    for brand_name in racquets_by_brands:
        racquets_chart_data["brands"].append(brand_name)
        racquets_chart_data["racquets"].append(len(racquets_by_brands[brand_name]))

    # Stringings data
    stringings_data = Stringing.query.with_entities(Stringing.received_date, func.count(Stringing.id)).group_by(
        func.strftime('%y', Stringing.received_date), func.strftime('%m', Stringing.received_date)).all()

    stringings_chart_data = {
        "date": [],
        "count": []
    }

    for date, count in stringings_data:
        stringings_chart_data["date"].append(date.strftime('%m/%Y'))
        stringings_chart_data["count"].append(count)

    # table data
    # stringings = Stringing.query.group_by(Stringing.customer_id).all()
    stringings = Stringing.query.join(Customer).join(Payment, isouter=True).with_entities(
        Customer,
        func.sum(Stringing.price),
        func.sum(Payment.payed),
        func.sum(Stringing.price) - func.sum(Payment.payed)
    ).having(
        or_(Payment.payed == None, func.sum(Stringing.price) != func.sum(Payment.payed))
    ).group_by(Customer.id).all()

    payment_table_data = {
        "rows": [],
        "totals": [0] * 3
    }

    for customer, total_price, total_payed, total_remaining in stringings:
        if total_payed is None:
            total_payed = 0
            total_remaining = total_price

        payment_table_data["rows"].append({
            "customer": customer.full_name(),
            "total_price": total_price,
            "total_payed": total_payed,
            "total_remaining": total_remaining
        })

        payment_table_data["totals"][0] += total_price
        payment_table_data["totals"][1] += total_payed
        payment_table_data["totals"][2] += total_remaining

    return render_template("index.jinja2", user=current_user, customers_chart_data=customers_chart_data,
                           racquets_chart_data=racquets_chart_data, stringings_chart_data=stringings_chart_data,
                           payment_table_data=payment_table_data)


@views.route("/brands", methods=["GET", "POST"])
@login_required
def brands():
    if request.method == "POST":
        name = form_value_to_string(request.form.get("name"))
        url = form_value_to_string(request.form.get("url"))

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
        first_name = form_value_to_string(request.form.get("first_name"))
        last_name = form_value_to_string(request.form.get("last_name"))
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

                db.session.add(new_customer)
                db.session.commit()

        return redirect(url_for("views.customers"))

    customers = Customer.query.all()
    racquets = Racquet.query.join(Brand).order_by(Racquet.release_year.desc(), Brand.name, Racquet.model).all()

    racquets_by_brands = group_racquets_by_brand(racquets)

    return render_template("customers.jinja2", user=current_user, customers=customers,
                           racquets_by_brands=racquets_by_brands)


@views.route("/racquets", methods=["GET", "POST"])
@login_required
def racquets():
    if request.method == "POST":
        brand_id = form_value_to_string(request.form.get("brand"))
        model = form_value_to_string(request.form.get("model"))
        release_year = form_value_to_int(request.form.get("release_year"))

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


@views.route("/stringings", methods=["GET", "POST"])
@login_required
def stringings():
    if request.method == "POST":
        customer_id = form_value_to_int(request.form.get("customer"))
        racquet_id = form_value_to_int(request.form.get("raquet"))
        tension = form_value_to_float(request.form.get("tension"))
        string_type = form_value_to_string(request.form.get("string_type"))
        include_string = form_value_to_bool(request.form.get("include_string"))
        price = form_value_to_float(request.form.get("price"))
        received_date = form_value_to_datetime(request.form.get("date_received"))
        finished_date = form_value_to_datetime(request.form.get("date_finished"))
        returned_date = form_value_to_datetime(request.form.get("date_returned"))

        if not customer_id or not racquet_id or not tension or not price or not received_date:
            flash("please fill all required fields", category="error")
        else:
            stringing = Stringing.query.filter_by(customer_id=customer_id, racquet_id=racquet_id, tension=tension,
                                                  string_type=string_type,
                                                  include_string=include_string,
                                                  price=price,
                                                  received_date=received_date,
                                                  finished_date=finished_date,
                                                  returned_date=returned_date).first()
            if stringing:
                flash("stringing already exists", category="error")
            else:
                new_stringing = Stringing(
                    customer_id=customer_id, racquet_id=racquet_id, tension=tension, string_type=string_type,
                    include_string=include_string, price=price, received_date=received_date,
                    finished_date=finished_date,
                    returned_date=returned_date)

                db.session.add(new_stringing)
                db.session.commit()

        return redirect(url_for("views.stringings"))

    stringings = Stringing.query.all()
    racquets = Racquet.query.join(Brand).order_by(Racquet.release_year.desc(), Brand.name, Racquet.model).all()
    customers = Customer.query.all()

    racquets_by_brands = group_racquets_by_brand(racquets)

    return render_template("stringings.jinja2", user=current_user, stringings=stringings, customers=customers,
                           racquets_by_brands=racquets_by_brands)


@views.route("/payments", methods=["GET", "POST"])
@login_required
def payments():
    if request.method == "POST":
        stringing_id = form_value_to_int(request.form.get("stringing"))
        payed = form_value_to_float(request.form.get("payed"))
        payed_date = form_value_to_datetime(request.form.get("date_payed"))

        if not stringing_id or not payed or not payed_date:
            flash("please fill all required fields", category="error")
        else:
            payment = Payment.query.filter_by(stringing_id=stringing_id, payed=payed, payed_date=payed_date).first()
            if payment:
                flash("payment already exists", category="error")
            else:
                new_payment = Payment(stringing_id=stringing_id, payed=payed, payed_date=payed_date)

                db.session.add(new_payment)
                db.session.commit()

    stringings = Stringing.query.all()
    payments = Payment.query.all()

    args = request.args
    print(args.get("id", default="", type=int))
    return render_template("payment.jinja2", user=current_user, stringings=stringings, payments=payments)
