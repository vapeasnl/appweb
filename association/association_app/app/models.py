# app/models.py
from . import db
from flask_login import UserMixin

# Table d'association pour la relation many-to-many entre User et Event
attendance = db.Table('attendance',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('event_id', db.Integer, db.ForeignKey('event.id'), primary_key=True)
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)  # Stockage du mot de passe non hashé
    is_admin = db.Column(db.Boolean, default=False)
    events = db.relationship('Event', secondary=attendance, backref='attendees')

class Association(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    # Ajoutez d'autres champs selon vos besoins

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    # Ajoutez d'autres champs selon vos besoins

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    content = db.Column(db.Text, nullable=False)
    # Ajoutez d'autres champs selon vos besoins

