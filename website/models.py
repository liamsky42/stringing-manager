from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy.orm import backref


# class Note(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     data = db.Column(db.String(10000))
#     date = db.Column(db.DateTime(timezone=True), default=func.now())
#     user_id = db.Column(db.Integer, db.ForeignKey("user.id"))


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


customer_racquet_association = db.Table('customer_racquet', db.Model.metadata,
                                     db.Column('customer_id', db.ForeignKey('customer.id'), primary_key=True),
                                     db.Column('racquet_id', db.ForeignKey('racquet.id'), primary_key=True)
                                     )


class Racquet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(100), nullable=False)
    release_year = db.Column(db.SmallInteger())
    brand_id = db.Column(db.Integer, db.ForeignKey("brand.id"), nullable=False)


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    stringings = db.relationship("Stringing", backref='customer', lazy=True)
    payments = db.relationship("Payment", backref='customer', lazy=True)
    racquets = db.relationship("Racquet",
                            secondary=customer_racquet_association,
                            backref="customers")


class Stringing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"), nullable=False)
    racquet_id = db.Column(db.Integer, db.ForeignKey("racquet.id"), nullable=False)
    received_date = db.Column(db.DateTime(timezone=True), nullable=False, default=func.now())
    finished_date = db.Column(db.DateTime(timezone=True))
    returned_date = db.Column(db.DateTime(timezone=True))
    price = db.Column(db.Float())
    tention = db.Column(db.Float())
    string_type = db.Column(db.String(50), nullable=False)
    payment = db.relationship("Payment", backref=backref("stringing", uselist=False), lazy=True)


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stringing_id = db.Column(db.Integer, db.ForeignKey("stringing.id"), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"), nullable=False)
    payed = db.Column(db.Float())
    payed_date = db.Column(db.DateTime(timezone=True), nullable=False, default=func.now())
