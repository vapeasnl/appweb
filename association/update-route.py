from flask import Flask, request, redirect, url_for, flash, render_template
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from .models import Media
from . import db

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'path/to/your/upload/folder'  # Set your upload folder path
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'mp4', 'mov'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@admin_bp.route('/media', methods=['POST'])
@login_required
def create_media():
    if not current_user.is_admin:
        return redirect(url_for('main.home'))

    title = request.form['title']
    description = request.form['description']
    file = request.files['file']

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        file_url = url_for('static', filename=os.path.join('uploads', filename))
        
        new_media = Media(title=title, description=description, file_url=file_url)
        db.session.add(new_media)
        db.session.commit()
        flash('New media added successfully.', 'success')
    else:
        flash('Invalid file type or no file uploaded.', 'error')

    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/statistics')
@login_required
def admin_statistics():
    if not current_user.is_admin:
        flash('You do not have access to this page.', 'danger')
        return redirect(url_for('main.home'))
    
    events = Event.query.all()
    return render_template('admin_statistics.html', events=events)

@admin_bp.route('/attendance')
@login_required
def admin_attendance():
    if not current_user.is_admin:
        flash('You do not have access to this page.', 'danger')
        return redirect(url_for('main.home'))
    
    events = Event.query.all()
    return render_template('admin_attendance.html', events=events)


@admin_bp.route('/dashboard')
@login_required
def dashboard():
    if not current_user.is_admin:
        return redirect(url_for('main.home'))
    
    # Fetch data for attendance and statistics
    attendances = Attendance.query.all()
    events = Event.query.all()
    
    event_names = [event.name for event in events]
    attendance_counts = [Attendance.query.filter_by(event_id=event.id).count() for event in events]
    
    return render_template('dashboard.html', 
                           reports=reports, 
                           users=users, 
                           events=events, 
                           news_list=news_list, 
                           achievements=achievements, 
                           media_list=media_list, 
                           attendances=attendances, 
                           event_names=event_names, 
                           attendance_counts=attendance_counts)


@main_bp.route('/attend_event/<int:event_id>', methods=['POST'])
@login_required
def attend_event(event_id):
    event = Event.query.get_or_404(event_id)
    
    if current_user.is_authenticated:
        name = current_user.name
        email = current_user.email
        phone = current_user.phone
    else:
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
    
    attendance = Attendance(event_id=event_id, name=name, email=email, phone=phone)
    db.session.add(attendance)
    db.session.commit()
    
    flash('Your attendance has been marked.', 'success')
    return redirect(url_for('main.home'))

###############
from flask import Blueprint, render_template, request, redirect, url_for, flash, g
from flask_login import current_user, login_required
from app.models import db, Event, Attendance
from datetime import datetime

main_bp = Blueprint('main', __name__)

@main_bp.route('/attend_event/<int:event_id>', methods=['POST'])
def attend_event(event_id):
    event = Event.query.get_or_404(event_id)
    
    if current_user.is_authenticated:
        name = current_user.name
        email = current_user.email
        phone = current_user.phone
    else:
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
    
    new_attendance = Attendance(event_id=event.id, name=name, email=email, phone=phone)
    db.session.add(new_attendance)
    db.session.commit()
    
    flash('Your attendance has been marked successfully.', 'success')
    return redirect(url_for('main.event_attendance'))

# Ensure you have an event_attendance.html template or update the redirect accordingly.
@main_bp.route('/event_attendance')
def event_attendance():
    events = Event.query.all()
    return render_template('event_attendance.html', events=events)


from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, g
from flask_login import current_user, login_required
from datetime import datetime
from app.models import db, Event, Attendance, ContactMessage

main_bp = Blueprint('main', __name__)

@main_bp.route('/events', methods=['GET', 'POST'])
def attend_event(event_id):
    if request.method == 'POST':
        if not current_user.is_authenticated:
            flash('You need to be logged in to mark your attendance.', 'error')
            return redirect(url_for('main.events'))

        event = Event.query.get_or_404(event_id)
        attendance = Attendance(user_id=current_user.id, event_id=event.id)
        db.session.add(attendance)
        db.session.commit()
        flash('Your attendance has been marked.', 'success')
        return redirect(url_for('main.events'))

    events = Event.query.filter(Event.date >= datetime.utcnow()).all()
    return render_template('events.html', events=events)

@main_bp.route('/attend_event_modal', methods=['POST'])
def attend_event_modal():
    event_id = request.form.get('event_id')
    name = request.form.get('name')
    email = request.form.get('email')
    address = request.form.get('address')
    phone = request.form.get('phone')

    # Save these details to the new database table if necessary
    contact_message = ContactMessage(name=name, email=email, address=address, phone=phone, event_id=event_id)
    db.session.add(contact_message)
    db.session.commit()

    flash('Your attendance has been marked.', 'success')
    return redirect(url_for('main.events'))
