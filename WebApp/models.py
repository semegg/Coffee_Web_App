import datetime
import os

import pandas as pd
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()


class Coffee(db.Model):
    __tablename__ = 'coffee'
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def __str__(self):
        return f'ID: {self.id}\nFull name:{self.name}\nPrice: {self.price}\n'


class IceCoffee(db.Model):
    __tablename__ = 'ice coffee'
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def __str__(self):
        return f'ID: {self.id}\nFull name:{self.name}\nPrice: {self.price}\n'


class Other(db.Model):
    __tablename__ = 'other'
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def __str__(self):
        return f'ID: {self.id}\nFull name:{self.name}\nPrice: {self.price}\n'


class Sweets(db.Model):
    __tablename__ = 'sweets'
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def __str__(self):
        return f'ID: {self.id}\nFull name:{self.name}\nPrice: {self.price}\n'


class SuccessfulPurchase(db.Model):
    __tablename__ = 'successful_purchases'
    id = db.Column(db.Integer, primary_key=True)
    user_profile_url = db.Column(db.String(128), nullable=False)
    user_name = db.Column(db.String(50), nullable=False)
    order = db.Column(db.String(128), nullable=False)
    total_amount = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String(30), nullable=False)


class Admin(db.Model, UserMixin):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    last_login = db.Column(db.String, nullable=False)
    super_admin = db.Column(db.Boolean, default=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @staticmethod
    def update_last_login(admin):
        admin.last_login = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        db.session.commit()

    @staticmethod
    def register_admin(username, password):
        db.session.add(Admin(
            username=username,
            password=generate_password_hash(password)
        ))
        db.session.commit()


class Tables:
    categories = (
        'coffee', 'ice coffee', 'other', 'sweets'
    )
    table_classes = {'coffee': Coffee,
                     'ice coffee': IceCoffee,
                     'sweets': Sweets,
                     'other': Other}


def add_product_to_database(table, id, name, price):
    new_product = table(id=id, name=name, price=price)
    db.session.add(new_product)
    db.session.commit()


def save_uploaded_image(uploaded_file, id):
    upload_folder = 'static/coffee_pics'
    filename = os.path.join(upload_folder, f"{id}.png")
    uploaded_file.save(filename)


# ...

def export_successful_purchases_to_csv(period):
    periods = {
        '1_day': datetime.timedelta(days=1),
        '1_week': datetime.timedelta(weeks=1),
        '1_month': datetime.timedelta(days=30),
        'all_time': None
    }

    period_duration = periods.get(period, None)

    if period_duration is not None:
        start_date = datetime.datetime.now() - period_duration
    else:
        start_date = None

    if start_date is not None:
        purchases = db.session.query(SuccessfulPurchase).filter(
            SuccessfulPurchase.date >= start_date.strftime("%Y-%m-%d %H:%M:%S")
        ).all()
    else:
        purchases = db.session.query(SuccessfulPurchase).all()

    data = {
        'ID': [purchase.id for purchase in purchases],
        'User Profile URL': [purchase.user_profile_url for purchase in purchases],
        'User Name': [purchase.user_name for purchase in purchases],
        'Order': [purchase.order for purchase in purchases],
        'Total Amount': [purchase.total_amount for purchase in purchases],
        'Date': [purchase.date for purchase in purchases]
    }

    df = pd.DataFrame(data)

    csv_filename = f'successful_purchases_{period}.csv'
    df.to_csv(csv_filename, index=False)

    return csv_filename
