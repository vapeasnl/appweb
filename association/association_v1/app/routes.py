from flask import Blueprint, render_template, request, redirect, url_for, flash, g, current_app
from flask_login import login_user, logout_user, login_required, current_user
from .models import db, User, Association, News, Event, Report, Achievement, Media, ContactMessage, Attendance
from datetime import datetime
from sqlalchemy import func
import os
from flask import Flask
from werkzeug.utils import secure_filename
from . import db
from flask import jsonify



main_bp = Blueprint('main', __name__)
auth_bp = Blueprint('auth', __name__)
admin_bp = Blueprint('admin', __name__)
profile_bp = Blueprint('profile', __name__)
news_bp = Blueprint('news', __name__)

# Static routes
@profile_bp.before_request
def before_request():
    if current_user.is_authenticated:
        g.unread_count = ContactMessage.query.filter_by(is_read=False).count()
    else:
        g.unread_count = 0




@profile_bp.context_processor
def inject_unread_count():
    return dict(unread_count=g.get('unread_count', 0))


@admin_bp.before_request
def before_request():
    if current_user.is_authenticated:
        g.unread_count = ContactMessage.query.filter_by(is_read=False).count()
    else:
        g.unread_count = 0

@admin_bp.context_processor
def inject_unread_count():
    return dict(unread_count=g.get('unread_count', 0))


@main_bp.before_request
def before_request():
    if current_user.is_authenticated:
        g.unread_count = ContactMessage.query.filter_by(is_read=False).count()
    else:
        g.unread_count = 0

@main_bp.context_processor
def inject_unread_count():
    if 'unread_count' in g:
        return dict(unread_count=g.unread_count)
    return {}



@main_bp.route('/about')
def about():
    return render_template('about.html')

@main_bp.route('/activities')
def activities():
    return render_template('activities.html')

@main_bp.route('/partners')
def partners():
    return render_template('partners.html')

@main_bp.route('/help')
def help():
    return render_template('help.html')

@main_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        sender_name = request.form['name']
        sender_email = request.form['email']
        subject = request.form['subject']
        content = request.form['content']
        
        new_message = ContactMessage(
            sender_name=sender_name,
            sender_email=sender_email,
            subject=subject,
            content=content,
            sent_at=datetime.utcnow()
        )
        
        db.session.add(new_message)
        db.session.commit()
        
        flash('Your message has been sent successfully!', 'success')
        return redirect(url_for('main.contact'))
    
    return render_template('contact.html')
    
# Route pour afficher les messages pour l'administrateur
@main_bp.route('/messages', methods=['GET'])
@login_required
def admin_messages():
    if not current_user.is_admin:
        flash('You do not have access to this page.', 'danger')
        return redirect(url_for('main.home'))
    
    page = request.args.get('page', 1, type=int)
    messages = ContactMessage.query.order_by(ContactMessage.sent_at.desc()).paginate(page=page, per_page=10)
    return render_template('messages.html', messages=messages.items, pagination=messages, unread_count=g.unread_count)


@main_bp.route('/messages/mark/<int:message_id>', methods=['POST'])
@login_required
def admin_mark_message(message_id):
    if not current_user.is_admin:
        flash('You do not have access to this page.', 'danger')
        return redirect(url_for('main.home'))
    
    message = ContactMessage.query.get_or_404(message_id)
    message.is_read = not message.is_read
    db.session.commit()
    return redirect(url_for('main.admin_messages'))

@main_bp.route('/messages/delete/<int:message_id>', methods=['POST'])
@login_required
def admin_delete_message(message_id):
    if not current_user.is_admin:
        flash('You do not have access to this page.', 'danger')
        return redirect(url_for('main.home'))
    
    message = ContactMessage.query.get_or_404(message_id)
    db.session.delete(message)
    db.session.commit()
    return redirect(url_for('main.admin_messages'))

@main_bp.route('/')
def home():
    # Récupérer uniquement les événements futurs
    upcoming_events = Event.query.filter(Event.date >= datetime.utcnow()).order_by(Event.date.asc()).all()
    news = News.query.order_by(News.date.desc()).all()
    return render_template('home.html', events=upcoming_events, news=news)


@admin_bp.route('/events/<int:event_id>/register-attendance', methods=['GET', 'POST'])
def register_attendance(event_id):
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        
        # Determine user_id
        if current_user.is_authenticated:
            user_id = current_user.id  # Assuming you're using Flask-Login
        else:
            user_id = 999  # Default user ID for non-logged-in users

        # Create attendance object
        attendance = Attendance(
            event_id=event_id,
            user_id=user_id,
            name=name,
            email=email,
            phone=phone
        )

        # Add to database session and commit
        db.session.add(attendance)
        db.session.commit()

        flash('Attendance registered successfully', 'success')
        return redirect(url_for('event_details', event_id=event_id))

    return render_template('register_attendance.html', event_id=event_id)




@main_bp.route('/events/<int:event_id>/attend', methods=['POST'])
@login_required
def attend_event(event_id):
    event = Event.query.get_or_404(event_id)
    if event:
        new_attendance = Attendance(event_id=event.id, user_id=current_user.id, name=current_user.name, email=current_user.email, phone=current_user.phone)
        db.session.add(new_attendance)
        db.session.commit()
        flash('You have marked your attendance for the event.', 'success')
    return redirect(url_for('main.home'))

@main_bp.route('/attend_event/<int:event_id>', methods=['POST'])
def attend_event_form(event_id):
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

@profile_bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

@profile_bp.route('/manage_profile', methods=['GET', 'POST'])
@login_required
def manage_profile():
    if request.method == 'POST':
        current_user.name = request.form['name']
        current_user.address = request.form['address']
        current_user.postal_address = request.form['postal_address']
        current_user.email = request.form['email']
        current_user.date_of_birth = request.form['date_of_birth']
        current_user.marital_status = request.form['marital_status']
        db.session.commit()
        flash('Profile updated successfully.')
        return redirect(url_for('profile.profile'))
    return render_template('manage_profile.html', user=current_user, unread_count=g.unread_count)




@admin_bp.route('/dashboard')
@login_required
def dashboard():
    if not current_user.is_admin:
        return redirect(url_for('main.home'))
    
    # Pagination variables
    page_reports = request.args.get('page_reports', 1, type=int)
    page_users = request.args.get('page_users', 1, type=int)
    page_events = request.args.get('page_events', 1, type=int)
    page_news = request.args.get('page_news', 1, type=int)
    page_achievements = request.args.get('page_achievements', 1, type=int)
    page_media = request.args.get('page_media', 1, type=int)

    # Querying data with pagination
    reports = Report.query.paginate(page=page_reports, per_page=5)
    users = User.query.paginate(page=page_users, per_page=5)
    events = Event.query.paginate(page=page_events, per_page=5)
    news_list = News.query.paginate(page=page_news, per_page=5)
    achievements_pagination = Achievement.query.paginate(page=page_achievements, per_page=5)
    media_list = Media.query.paginate(page=page_media, per_page=10)

    # Check if the request is an Ajax request (XHR request)
    if request.is_json:
        # Example for users section
        if request.args.get('section') == 'users':
            users_data = [{'username': user.username, 'email': user.email} for user in users.items]
            return jsonify(users=users_data)
        
        # Example for events section
        if request.args.get('section') == 'events':
            events_data = [{'name': event.name, 'date': event.date} for event in events.items]
            return jsonify(events=events_data)
        
        # Handle reports section
        if request.args.get('section') == 'reports':
            reports_data = [{'title': report.title, 'description': report.description} for report in reports.items]
            return jsonify(reports=reports_data)
        
        # Handle news section
        if request.args.get('section') == 'news':
            news_data = [{'title': news.title, 'content': news.content} for news in news_list.items]
            return jsonify(news=news_data)
        
        # Handle achievements section
        if request.args.get('section') == 'achievements':
            achievements_data = [{'name': achievement.name, 'description': achievement.description} for achievement in achievements_pagination.items]
            return jsonify(achievements=achievements_data)
        
        if request.args.get('section') == 'media':
            media_data = [{'title': media.title, 'description': media.description} for media in media_list.items]
            return jsonify(media=media_data)
            
    print("Media list:", media_list.items)
    # For rendering the HTML template
    achievement_names = [achievement.name for achievement in achievements_pagination.items]
    beneficiaries_numbers = [achievement.beneficiaries_number for achievement in achievements_pagination.items]

    event_names = [event.name for event in events.items]
    attendance_counts = [Attendance.query.filter_by(event_id=event.id).count() for event in events.items]

    attendances = Attendance.query.all()

    return render_template('dashboard.html', 
                           reports=reports, 
                           users=users, 
                           events=events, 
                           news_list=news_list, 
                           achievements=achievements_pagination, 
                           media_list=media_list, 
                           event_names=event_names, 
                           attendance_counts=attendance_counts, 
                           attendances=attendances,
                           unread_count=g.unread_count, 
                           achievement_names=achievement_names, 
                           beneficiaries_numbers=beneficiaries_numbers)






# Report routes
@admin_bp.route('/reports/create', methods=['POST'])
@login_required
def create_report():
    if not current_user.is_admin:
        flash('You do not have permission to create reports.', 'error')
        return redirect(url_for('main.home'))
        
    title = request.form.get('title')
    date = request.form.get('date')
    content = request.form.get('content')
    section = request.args.get('section', 'reports')
  
    if not title or not date or not content:
        flash('Title, date, and content are required.', 'error')
        return redirect(url_for('admin.dashboard', section='reports'))

    try:
        report = Report(title=title, date=date, content=content)
        db.session.add(report)
        db.session.commit()
        flash('Report added successfully.', 'success')
    except Exception as e:
        flash(f'Failed to add report. Error: {str(e)}', 'error')
        db.session.rollback()

    return redirect(url_for('admin.dashboard', section='reports'))

@admin_bp.route('/reports/<int:report_id>', methods=['POST'])
@login_required
def update_report(report_id):
    if not current_user.is_admin:
        return redirect(url_for('main.home'))
    
    # Récupère le rapport existant depuis la base de données
    report = Report.query.get(report_id)
    section = request.args.get('section', 'reports')
    if report:
        # Met à jour les champs du rapport avec les données du formulaire
        report.title = request.form['title']
        report.content = request.form['content']
        
        # Gestion de la date
        date_str = request.form['date']
        
        try:
            # Essaye de parser la date au format YYYY-MM-DD
            date = datetime.strptime(date_str, '%Y-%m-%d')
            report.date = date
        except ValueError:
            flash('Invalid date format. Please use YYYY-MM-DD format.')
            return redirect(url_for('admin.dashboard', section='reports'))  # Redirige vers le tableau de bord en cas d'erreur
        
        # Sauvegarde les modifications dans la base de données
        db.session.commit()
        flash('Report updated successfully.')
    
    # Redirige vers le tableau de bord une fois la mise à jour effectuée
    return redirect(url_for('admin.dashboard', section='reports'))  # Redirige vers le tableau de bord en cas d'erreur

@admin_bp.route('/reports/<int:report_id>/delete', methods=['POST'])
@login_required
def delete_report(report_id):
    if not current_user.is_admin:
        return redirect(url_for('main.home'))
    report = Report.query.get(report_id)
    section = request.args.get('section', 'reports')

    if report:
        db.session.delete(report)
        db.session.commit()
    return redirect(url_for('admin.dashboard', section='reports'))

@admin_bp.route('/events', methods=['POST'])
@login_required
def create_event():
    if not current_user.is_admin:
        flash('You do not have permission to create events.', 'error')
        return redirect(url_for('main.home'))

    name = request.form.get('name')
    date_str = request.form.get('date')
    section = request.args.get('section', 'events')

    if not name or not date_str:
        flash('Name and date are required fields.', 'error')
        return redirect(url_for('admin.dashboard', section='events'))

    try:
        date = datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        flash('Invalid date format. Please use YYYY-MM-DD format.', 'error')
        return redirect(url_for('admin.dashboard', section='events'))

    try:
        new_event = Event(name=name, date=date)
        db.session.add(new_event)
        db.session.commit()
        flash('New event added successfully.', 'success')
    except Exception as e:
        flash(f'Failed to add event. Error: {str(e)}', 'error')
        db.session.rollback()

    return redirect(url_for('admin.dashboard', section='events'))

@admin_bp.route('/events/<int:event_id>/update', methods=['POST'])
@login_required
def update_event(event_id):
    if not current_user.is_admin:
        flash('You do not have permission to update events.', 'error')
        return redirect(url_for('main.home'))
    event = Event.query.get(event_id)
    section = request.args.get('section', 'events')

    if event:
        event.name = request.form['name']
        event.date = request.form['date']
        db.session.commit()
        flash('Event updated successfully.', 'success')
    return redirect(url_for('admin.dashboard', section='events'))

@admin_bp.route('/events/<int:event_id>/delete', methods=['POST'])
@login_required
def delete_event(event_id):
    if not current_user.is_admin:
        flash('You do not have permission to delete events.', 'error')
        return redirect(url_for('main.home'))

    event = Event.query.get_or_404(event_id)
    section = request.args.get('section', 'events')

    try:
        # Supprimer d'abord les enregistrements associés dans attendance
        Attendance.query.filter_by(event_id=event_id).delete()
        db.session.commit()

        # Ensuite, supprimer l'événement
        db.session.delete(event)
        db.session.commit()

        flash('Event deleted successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting event: {str(e)}', 'error')

    return redirect(url_for('admin.dashboard', section=section))


# User routes
@admin_bp.route('/users', methods=['POST'])
@login_required
def create_user():
    if not current_user.is_admin:
        flash('You do not have permission to create users.', 'error')
        return redirect(url_for('main.home'))
    
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    is_admin = request.form.get('is_admin') == 'on'
    section = request.args.get('section', 'users')
    # Vérification des champs requis
    if not username or not email or not password:
        flash('Username, email, and password are required fields.', 'error')
        return redirect(url_for('admin.dashboard', section='users'))

    # Vérification de l'unicité de l'email
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        flash('Email address is already in use. Please use a different email.', 'error')
        return redirect(url_for('admin.dashboard', section='users'))

    # Création du nouvel utilisateur
    new_user = User(username=username, email=email, is_admin=is_admin)
    new_user.set_password(password)
    
    # Ajout à la base de données
    db.session.add(new_user)
    db.session.commit()

    flash('New user added successfully.', 'success')
    return redirect(url_for('admin.dashboard', section='users'))

@admin_bp.route('/users/<int:user_id>/update', methods=['POST'])
@login_required
def update_user(user_id):
    if not current_user.is_admin:
        flash('You do not have permission to update users.', 'error')
        return redirect(url_for('admin.dashboard', section='users'))
   
    section = request.args.get('section', 'users')
    user = User.query.get(user_id)
    if user:
        user.username = request.form['username']
        user.email = request.form['email']
        user.is_admin = 'is_admin' in request.form  # Check if checkbox is checked
        
        new_password = request.form.get('password')
        if new_password:
            user.set_password(new_password)  # Update password if provided
        
        db.session.commit()
        flash('User updated successfully.', 'success')
        
    return redirect(url_for('admin.dashboard', section='users'))

@admin_bp.route('/users/<int:user_id>/delete', methods=['POST'])
@login_required
def delete_user(user_id):
    if not current_user.is_admin:
        flash('You do not have permission to delete users.', 'error')
        return redirect(url_for('main.home'))
    
    user = User.query.get(user_id)
    section = request.args.get('section', 'users')
    
    if user:
        # Supprimer les enregistrements associés dans attendance
        Attendance.query.filter_by(user_id=user_id).delete()
        db.session.delete(user)
        db.session.commit()
        flash('User deleted successfully.', 'success')
    
    return redirect(url_for('admin.dashboard', section='users'))

# News routes
@news_bp.route('/news', methods=['GET'])
def view_news():
    news = News.query.order_by(News.date.desc()).all()
    return render_template('news.html', news=news)

@news_bp.route('/news/add', methods=['GET', 'POST'])
@login_required
def add_news():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        image_url = request.form.get('image_url')
        section = request.args.get('section', 'news')

        if not title or not content or not image_url:
            flash('Please fill out all fields.', 'danger')
            return redirect(url_for('news.add_news'))

        news = News(title=title, content=content, image_url=image_url)
        db.session.add(news)
        db.session.commit()
        flash('News added successfully.', 'success')
        return redirect(url_for('news.view_news'))

    return render_template('add_news.html')




@admin_bp.route('/news/<int:news_id>/update', methods=['POST'])
@login_required
def update_news(news_id):
    if not current_user.is_admin:
        flash('You do not have permission to update news.', 'error')
        return redirect(url_for('main.home'))
    news = News.query.get(news_id)
    section = request.args.get('section', 'news')

    if news:
        news.title = request.form['news_title']
        news.content = request.form['news_content']
        db.session.commit()
        flash('News updated successfully.', 'success')
    return redirect(url_for('admin.dashboard', section='news'))

@admin_bp.route('/news/<int:news_id>/delete', methods=['POST'])
@login_required
def delete_news(news_id):
    if not current_user.is_admin:
        flash('You do not have permission to delete news.', 'error')
        return redirect(url_for('main.home'))
    news = News.query.get(news_id)
    section = request.args.get('section', 'news')

    if news:
        db.session.delete(news)
        db.session.commit()
        flash('News deleted successfully.', 'success')
    return redirect(url_for('admin.dashboard', section='news'))

@admin_bp.route('/news/create', methods=['POST'])
@login_required
def create_news():
    if not current_user.is_admin:
        flash('You do not have permission to create news.', 'error')
        return redirect(url_for('main.home'))

    title = request.form.get('news_title')
    content = request.form.get('news_content')
    section = request.args.get('section', 'news')
    # Vérification des champs requis
    if not title or not content:
        flash('Title and content are required.', 'error')
        return redirect(url_for('admin.dashboard', section='news'))

    try:
        # Création de la nouvelle
        news = News(title=title, content=content)
        db.session.add(news)
        db.session.commit()
        flash('News added successfully.', 'success')
    except Exception as e:
        flash(f'Failed to add news. Error: {str(e)}', 'error')
        db.session.rollback()

    return redirect(url_for('admin.dashboard', section='news'))
    
# Achievement routes
@main_bp.route('/achievements', methods=['GET', 'POST'])
def achievements():
    years = [year[0] for year in db.session.query(func.extract('year', Achievement.start_date)).distinct()]
    selected_year = request.form.get('year')
    if selected_year:
        achievements = Achievement.query.filter(func.extract('year', Achievement.start_date) == int(selected_year)).all()
    else:
        achievements = Achievement.query.all()
    return render_template('achievements.html', achievements=achievements, years=years, selected_year=selected_year)

@admin_bp.route('/achievements/create', methods=['POST'])
@login_required
def create_achievement():
    if not current_user.is_admin:
        flash('You do not have permission to create achievements.', 'error')
        return redirect(url_for('main.home'))

    name = request.form['name']
    start_date_str = request.form['start_date']
    end_date_str = request.form['end_date']
    site = request.form['site']
    objectives = request.form['objectives']
    beneficiaries_kind = request.form['beneficiaries_kind']
    beneficiaries_number = request.form['beneficiaries_number']
    results_obtained = request.form['results_obtained']
    section = request.args.get('section', 'achievements')

    # Vérification des champs requis
    if not name or not start_date_str or not end_date_str or not site or not objectives:
        flash('All fields are required.', 'error')
        return redirect(url_for('admin.dashboard', section='achievements'))

    try:
        # Conversion des dates
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

        # Création de la nouvelle réalisation
        new_achievement = Achievement(
            name=name, start_date=start_date, end_date=end_date, site=site,
            objectives=objectives, beneficiaries_kind=beneficiaries_kind,
            beneficiaries_number=beneficiaries_number, results_obtained=results_obtained
        )
        db.session.add(new_achievement)
        db.session.commit()
        flash('New achievement added successfully.', 'success')

    except ValueError:
        flash('Invalid date format. Please use YYYY-MM-DD format.', 'error')
    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'error')
        db.session.rollback()

    return redirect(url_for('admin.dashboard', section='achievements'))

@admin_bp.route('/achievements/<int:achievement_id>/update', methods=['POST'])
@login_required
def update_achievement(achievement_id):
    if not current_user.is_admin:
        return redirect(url_for('main.home'))
    achievement = Achievement.query.get(achievement_id)
    section = request.args.get('section', 'achievements')
    if achievement:
        achievement.name = request.form['name']
        achievement.start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d')
        achievement.end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d')
        achievement.site = request.form['site']
        achievement.objectives = request.form['objectives']
        achievement.beneficiaries_kind = request.form['beneficiaries_kind']
        achievement.beneficiaries_number = request.form['beneficiaries_number']
        achievement.results_obtained = request.form['results_obtained']
        db.session.commit()
    return redirect(url_for('admin.dashboard', section='achievements'))

@admin_bp.route('/achievements/<int:achievement_id>/delete', methods=['POST'])
@login_required
def delete_achievement(achievement_id):
    if not current_user.is_admin:
        return redirect(url_for('main.home'))
    achievement = Achievement.query.get(achievement_id)
    section = request.args.get('section', 'achievements')
    if achievement:
        db.session.delete(achievement)
        db.session.commit()
    return redirect(url_for('admin.dashboard', section='achievements'))




# Ensure you have an event_attendance.html template or update the redirect accordingly.
@main_bp.route('/event_attendance')
def event_attendance():
    events = Event.query.all()
    return render_template('event_attendance.html', events=events)


@admin_bp.route('/attendance')
@login_required
def admin_attendance():
    if not current_user.is_admin:
        flash('You do not have access to this page.', 'danger')
        return redirect(url_for('main.home'))
    
    events = Event.query.all()
    return render_template('admin_attendance.html', events=events)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/img'  # Set your upload folder path
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'mp4', 'mov'}

@main_bp.route('/media', methods=['GET'])
def view_media():
    media_list = Media.query.all()
    return render_template('media.html', media_list=media_list)


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'mp4', 'mov'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@admin_bp.route('/loader')
@login_required
def loader():
    if not current_user.is_admin:
        return redirect(url_for('main.home'))
    
    return redirect(url_for('admin.dashboard', section='loader'))



#media

@admin_bp.route('/media/create', methods=['POST'])
@login_required
def create_media():
    if not current_user.is_admin:
        flash('You do not have permission to add media.', 'error')
        return redirect(url_for('main.home'))

    title = request.form['title']
    description = request.form['description']
    file = request.files['file']
    section = request.args.get('section', 'media')

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        try:
            file.save(file_path)
            file_url = url_for('static', filename=os.path.join('uploads', filename))
            new_media = Media(title=title, description=description, file_url=file_url)
            db.session.add(new_media)
            db.session.commit()
            flash(f'New media added successfully. File saved to {file_path}', 'success')
        except Exception as e:
            flash(f'Failed to save file. Error: {str(e)}', 'error')
            db.session.rollback()
    else:
        flash('Invalid file type or no file uploaded.', 'error')

    return redirect(url_for('admin.dashboard', section='media'))

@admin_bp.route('/media/<int:media_id>/delete', methods=['POST'])
@login_required
def delete_media(media_id):
    if not current_user.is_admin:
        flash('You do not have permission to delete media.', 'error')
        return redirect(url_for('main.home'))
    
    media = Media.query.get_or_404(media_id)
    section = request.args.get('section', 'media')
    try:
        db.session.delete(media)
        db.session.commit()
        flash('Media deleted successfully.', 'success')
    except Exception as e:
        flash(f'Failed to delete media. Error: {str(e)}', 'error')
        db.session.rollback()

    return redirect(url_for('admin.dashboard', section='media'))


@admin_bp.route('/media/update/<int:media_id>', methods=['POST'])
@login_required
def update_media(media_id):
    if not current_user.is_admin:
        flash('You do not have permission to update media.', 'error')
        return redirect(url_for('main.home'))

    media = Media.query.get_or_404(media_id)
    media.title = request.form.get('title')
    media.description = request.form.get('description')
    section = request.args.get('section', 'media')
    
    file = request.files.get('file')
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        try:
            file.save(file_path)
            media.file_url = url_for('static', filename=os.path.join('uploads', filename))
        except Exception as e:
            flash(f'Failed to update file. Error: {str(e)}', 'error')
            db.session.rollback()

    try:
        db.session.commit()
        flash('Media updated successfully.', 'success')
    except Exception as e:
        flash(f'Failed to update media. Error: {str(e)}', 'error')
        db.session.rollback()

    return redirect(url_for('admin.dashboard', section='media'))
