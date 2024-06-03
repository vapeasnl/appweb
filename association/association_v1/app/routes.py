from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from .models import db, User, Association, Event, Report

main_bp = Blueprint('main', __name__)
auth_bp = Blueprint('auth', __name__)
admin_bp = Blueprint('admin', __name__)

@main_bp.route('/')
def home():
    return render_template('home.html')

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
    return render_template('dashboard.html', reports=reports)

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
        report.date = request.form['date']
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

