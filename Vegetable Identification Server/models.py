import datetime
from extension import db

class Vegetable(db.Model):
    __tablename__ = 'vegetable_massage'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    time = db.Column(db.DateTime, default=datetime.datetime.now)
    vegetable_name = db.Column(db.String(255), nullable=False)
    vegetable_sold = db.Column(db.Integer, nullable=False)
    vegetable_inventory = db.Column(db.Integer, nullable=False)
    vegetable_price = db.Column(db.Float, nullable=False)

class Vegetable_2(db.Model):
    __tablename__ = 'vegetable_stock'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    vegetable_name = db.Column(db.String(255), nullable=False)
    vegetable_sold = db.Column(db.Integer, nullable=False)
    vegetable_inventory = db.Column(db.Integer, nullable=False)
