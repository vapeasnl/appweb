from flask_login import UserMixin
from . import db, login, bcrypt

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    association_id = db.Column(db.Integer, db.ForeignKey('association.id'), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    phone_number = db.Column(db.String(15))
    cin = db.Column(db.String(8))

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"







    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    associations = db.relationship('Association', backref='admin', lazy=True)
    events = db.relationship('Event', backref='organizer', lazy=True)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Association(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    description = db.Column(db.Text)
    admin_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    members = db.relationship('AssociationMember', backref='association', lazy=True)
    events = db.relationship('Event', backref='association', lazy=True)
class AssociationMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    association_id = db.Column(db.Integer, db.ForeignKey('association.id'), nullable=False)
    date_joined = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text)
    date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(256))
    association_id = db.Column(db.Integer, db.ForeignKey('association.id'), nullable=False)
    organizer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

