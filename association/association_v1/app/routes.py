from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from .models import db, User, Association, Event, Report
from datetime import datetime

main_bp = Blueprint('main', __name__)
auth_bp = Blueprint('auth', __name__)
admin_bp = Blueprint('admin', __name__)

@main_bp.route('/')
def home():
    events = Event.query.all()
    return render_template('home.html', events=events)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('main.home'))
        flash('Invalid credentials')
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    if not current_user.is_admin:
        return redirect(url_for('main.home'))
    reports = Report.query.all()
    users = User.query.all()
    events = Event.query.all()
    return render_template('dashboard.html', reports=reports, users=users, events=events)

@admin_bp.route('/reports', methods=['POST'])
@login_required
def create_report():
    if not current_user.is_admin:
        return redirect(url_for('main.home'))
    title = request.form['title']
    date = request.form['date']
    content = request.form['content']
    report = Report(title=title, date=date, content=content)
    db.session.add(report)
    db.session.commit()
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/reports/<int:report_id>', methods=['POST'])
@login_required
def update_report(report_id):
    if not current_user.is_admin:
        return redirect(url_for('main.home'))
    
    report = Report.query.get(report_id)
    if report:
        report.title = request.form['title']
        date_str = request.form['date']
        try:
            date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M')
            report.date = date
        except ValueError:
            flash('Invalid date format. Please use YYYY-MM-DDTHH:MM format.')
            return redirect(url_for('admin.dashboard'))
        
        report.content = request.form['content']
        db.session.commit()
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/reports/<int:report_id>/delete', methods=['POST'])
@login_required
def delete_report(report_id):
    if not current_user.is_admin:
        return redirect(url_for('main.home'))
    report = Report.query.get(report_id)
    if report:
        db.session.delete(report)
        db.session.commit()
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/events', methods=['POST'])
@login_required
def create_event():
    if not current_user.is_admin:
        return redirect(url_for('main.home'))
    name = request.form['name']
    date_str = request.form['date']
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d')
        new_event = Event(name=name, date=date)
        db.session.add(new_event)
        db.session.commit()
        flash('New event added successfully.')
    except ValueError:
        flash('Invalid date format. Please use YYYY-MM-DD format.')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/events/<int:event_id>/update', methods=['POST'])
@login_required
def update_event(event_id):
    if not current_user.is_admin:
        return redirect(url_for('main.home'))
    event = Event.query.get(event_id)
    if event:
        event.name = request.form['name']
        event.date = request.form['date']
        db.session.commit()
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/events/<int:event_id>/delete', methods=['POST'])
@login_required
def delete_event(event_id):
    if not current_user.is_admin:
        return redirect(url_for('main.home'))
    event = Event.query.get(event_id)
    if event:
        db.session.delete(event)
        db.session.commit()
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/users', methods=['POST'])
@login_required
def create_user():
    if not current_user.is_admin:
        return redirect(url_for('main.home'))
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    is_admin = request.form.get('is_admin', False)
    new_user = User(username=username, email=email, is_admin=is_admin)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    flash('New user added successfully.')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/users/<int:user_id>/update', methods=['POST'])
@login_required
def update_user(user_id):
    if not current_user.is_admin:
        return redirect(url_for('main.home'))
    user = User.query.get(user_id)
    if user:
        user.username = request.form['username']
        user.email = request.form['email']
        user.is_admin = 'is_admin' in request.form
        if request.form['password']:
            user.set_password(request.form['password'])
        db.session.commit()
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/users/<int:user_id>/delete', methods=['POST'])
@login_required
def delete_user(user_id):
    if not current_user.is_admin:
        return redirect(url_for('main.home'))
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
    return redirect(url_for('admin.dashboard'))

@main_bp.route('/events/<int:event_id>/attend', methods=['POST'])
@login_required
def attend_event(event_id):
    event = Event.query.get(event_id)
    if event:
        current_user.attend(event)
        db.session.commit()
        flash('You have marked your attendance for the event.')
    return redirect(url_for('main.home'))

