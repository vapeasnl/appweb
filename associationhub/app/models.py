from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    # Ajoutez d'autres champs selon vos besoins

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Association(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    adresse = db.Column(db.String(200), nullable=True)
    president = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f"Association('{self.nom}')"

class Evenement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    lieu = db.Column(db.String(200), nullable=True)
    detail = db.Column(db.Text, nullable=True)
    association_id = db.Column(db.Integer, db.ForeignKey('association.id'), nullable=False)

    def __repr__(self):
        return f"Evenement('{self.nom}', '{self.date}')"

