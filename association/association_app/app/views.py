# app/views.py
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from .models import User, Association, Event, Report, db
from . import db

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    associations = Association.query.all()
    return render_template('index.html', associations=associations)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:  # Vérification sans hashage
            login_user(user)
            if user.is_admin:
                return redirect(url_for('main.admin_dashboard'))
            else:
                return redirect(url_for('main.dashboard'))
        flash('Invalid username or password')
    return render_template('login.html')

@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        user = User(username=username, email=email, password=password)  # Stockage du mot de passe non hashé
        db.session.add(user)
        db.session.commit()
        flash('Registration successful, please log in.')
        return redirect(url_for('main.login'))
    return render_template('signup.html')

@bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_admin:
        return redirect(url_for('main.admin_dashboard'))
    return render_template('dashboard.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/add_user', methods=['GET', 'POST'])
@login_required
def add_user():
    if not current_user.is_admin:
        flash('Only admins can add users.')
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        user = User(username=username, email=email, password=password)  # Stockage du mot de passe non hashé
        db.session.add(user)
        db.session.commit()
        flash('User added successfully.')
        return redirect(url_for('main.dashboard'))

    return render_template('add_user.html')

@bp.route('/admin_dashboard')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash('Access denied. Only admins allowed.')
        return redirect(url_for('main.dashboard'))

    return render_template('admin_dashboard.html')

@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        current_user.username = request.form['username']
        current_user.email = request.form['email']
        db.session.commit()
        flash('Profile updated successfully')
        return redirect(url_for('main.profile'))
    return render_template('profile.html', user=current_user)

@bp.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        old_password = request.form['old_password']
        new_password = request.form['new_password']
        if current_user.password == old_password:  # Vérification sans hashage
            current_user.password = new_password  # Mise à jour du mot de passe
            db.session.commit()
            flash('Password changed successfully')
            return redirect(url_for('main.profile'))
        else:
            flash('Old password is incorrect')
    return render_template('change_password.html')

@bp.route('/events')
@login_required
def events():
    events = Event.query.all()
    return render_template('events.html', events=events)

@bp.route('/mark_attendance/<int:event_id>', methods=['POST'])
@login_required
def mark_attendance(event_id):
    event = Event.query.get(event_id)
    if event:
        event.attendees.append(current_user)
        db.session.commit()
        flash('Attendance marked successfully')
    return redirect(url_for('main.events'))

@bp.route('/reports')
@login_required
def reports():
    reports = Report.query.all()
    return render_template('reports.html', reports=reports)

