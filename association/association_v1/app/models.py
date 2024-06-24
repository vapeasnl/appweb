from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from . import db, login_manager
from sqlalchemy.orm import relationship
import os
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


user_event = db.Table(
    'user_event',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('event_id', db.Integer, db.ForeignKey('event.id'), primary_key=True)
)

class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    name = db.Column(db.String(100), nullable=True)
    address = db.Column(db.String(200), nullable=True)
    postal_address = db.Column(db.String(200), nullable=True)
    date_of_birth = db.Column(db.Date, nullable=True)
    marital_status = db.Column(db.String(50), nullable=True)
    phone = db.Column(db.String(20))
    is_admin = db.Column(db.Boolean, default=False)

    events = db.relationship('Event', secondary='user_event', backref='attendees')

    def set_password(self, password):
        self.password = password

    def check_password(self, password):
        return self.password == password

    # Flask-Login required methods
    def get_id(self):
        return str(self.id)

    @property
    def is_authenticated(self):
        # Return True if the user is authenticated, i.e., they have provided valid credentials.
        return True  # Adjust as per your application logic

    @property
    def is_active(self):
        # Return True if the user is active and should be able to log in.
        return True  # Adjust as per your application logic

    @property
    def is_anonymous(self):
        # Return True if this is an anonymous user.
        return False

class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(100), nullable=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class Media(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    file_url = db.Column(db.String(200), nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)


class Achievement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    site = db.Column(db.String(150), nullable=False)
    objectives = db.Column(db.Text, nullable=False)
    beneficiaries_kind = db.Column(db.String(150), nullable=False)
    beneficiaries_number = db.Column(db.Integer, nullable=False)
    results_obtained = db.Column(db.Text, nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Association(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)

    
class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    content = db.Column(db.Text, nullable=False)

class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_name = db.Column(db.String(100), nullable=False)
    sender_email = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)

    def formatted_sent_at(self):
        return self.sent_at.strftime('%Y-%m-%d %H:%M:%S')
        
class Attendance(db.Model):
    __tablename__ = 'attendance'
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100))
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))

    def __repr__(self):
        return f"<Attendance {self.name} - Event: {self.event_id}>"

class Event(db.Model):
    __tablename__ = 'event'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    date = db.Column(db.DateTime, nullable=False)

    attendances = db.relationship('Attendance', backref='event', lazy='dynamic')

    def __repr__(self):
        return f"<Event {self.name} - ID: {self.id}>"


class AttendanceForm(FlaskForm):
    event_id = IntegerField('Event ID', validators=[DataRequired()])
    submit = SubmitField('Submit')
