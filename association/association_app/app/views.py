# app/views.py
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from .models import User, Association, Event
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
        if user and user.check_password(password):
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
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful, please log in.')
        return redirect(url_for('main.login'))
    return render_template('signup.html')

@bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_admin:
        # Logique pour l'admin
        pass
    else:
        # Logique pour l'utilisateur normal
        pass
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
        user = User(username=username, email=email)
        user.set_password(password)
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

