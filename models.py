from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    uid = db.Column(db.String(20))
    server = db.Column(db.String(10))

class Character(db.Model):
    character_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    element = db.Column(db.String(20))
    level = db.Column(db.Integer)
    constellation = db.Column(db.String(5))
    region = db.Column(db.String(50))
    img = db.Column(db.String(300))