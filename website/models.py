from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy.orm import backref


def group_racquets_by_brand(racquets):
    racquets_by_brands = {}
    for racquet in racquets:
        if racquet.brand.name in racquets_by_brands:
            racquets_by_brands[racquet.brand.name].append(racquet)
        else:
            racquets_by_brands[racquet.brand.name] = [racquet]

    return racquets_by_brands


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(50))
    # notes = db.relationship("Note")


class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    url = db.Column(db.String(100))
    raquets = db.relationship("Racquet", backref='brand', lazy=True)

    def __repr__(self):
        return f"Brand({self.name}, {self.url})"


customer_racquet_association = db.Table('customer_racquet', db.Model.metadata,
                                        db.Column('customer_id', db.ForeignKey('customer.id'), primary_key=True),
                                        db.Column('racquet_id', db.ForeignKey('racquet.id'), primary_key=True)
                                        )


class Racquet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(100), nullable=False)
    release_year = db.Column(db.SmallInteger())
    brand_id = db.Column(db.Integer, db.ForeignKey("brand.id"), nullable=False)

    stringings = db.relationship("Stringing", backref='racquet', lazy=True)

    def __repr__(self):
        return f"Racquet({self.model}, {self.release_year})"


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    stringings = db.relationship("Stringing", backref='customer', lazy=True)
    payments = db.relationship("Payment", backref='customer', lazy=True)
    racquets = db.relationship("Racquet",
                               secondary=customer_racquet_association,
                               backref="customers")

    def __repr__(self):
        return f"Customer({self.first_name}, {self.last_name})"


class Stringing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"), nullable=False)
    racquet_id = db.Column(db.Integer, db.ForeignKey("racquet.id"), nullable=False)
    tension = db.Column(db.Float())
    string_type = db.Column(db.String(50), nullable=False)
    include_string = db.Column(db.Boolean(), nullable=False, default=False)
    price = db.Column(db.Float())
    received_date = db.Column(db.DateTime(timezone=True), nullable=False, default=func.now())
    finished_date = db.Column(db.DateTime(timezone=True))
    returned_date = db.Column(db.DateTime(timezone=True))
    payment = db.relationship("Payment", backref=backref("stringing", uselist=False), lazy=True)

    def __repr__(self):
        return f"Stringing({self.customer_id},{self.racquet_id},{self.tension},{self.string_type},{self.include_string},{self.price},{self.received_date},{self.finished_date},{self.returned_date})"


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stringing_id = db.Column(db.Integer, db.ForeignKey("stringing.id"), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"), nullable=False)
    payed = db.Column(db.Float())
    payed_date = db.Column(db.DateTime(timezone=True), nullable=False, default=func.now())
