from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from .models import db, User, Association, News, Event, Report
from datetime import datetime

main_bp = Blueprint('main', __name__)
auth_bp = Blueprint('auth', __name__)
admin_bp = Blueprint('admin', __name__)
profile_bp = Blueprint('profile', __name__)
news_bp = Blueprint('news', __name__)

#static route

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

@main_bp.route('/contact')
def contact():
    return render_template('contact.html')

@main_bp.route('/')
def home():
    events = Event.query.all()
    news = News.query.order_by(News.date.desc()).all()
    return render_template('home.html', events=events, news=news)
    
@main_bp.route('/events/<int:event_id>/attend', methods=['POST'])
@login_required
def attend_event(event_id):
    event = Event.query.get(event_id)
    if event:
        current_user.attend(event)
        db.session.commit()
        flash('You have marked your attendance for the event.')
    return redirect(url_for('main.home'))

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
    return render_template('manage_profile.html', user=current_user)
@admin_bp.route('/achievements', methods=['GET', 'POST'])
@login_required
def manage_achievements():
    if not current_user.is_admin:
        return redirect(url_for('main.home'))

    if request.method == 'POST':
        name = request.form['name']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        site = request.form['site']
        objectives = request.form['objectives']
        beneficiaries_kind = request.form['beneficiaries_kind']
        beneficiaries_number = request.form['beneficiaries_number']
        results_obtained = request.form['results_obtained']

        new_achievement = Achievement(
            name=name, 
            start_date=start_date, 
            end_date=end_date, 
            site=site, 
            objectives=objectives, 
            beneficiaries_kind=beneficiaries_kind, 
            beneficiaries_number=beneficiaries_number, 
            results_obtained=results_obtained
        )
        db.session.add(new_achievement)
        db.session.commit()
        flash('Achievement added successfully.', 'success')

    achievements = Achievement.query.all()
    return render_template('manage_achievements.html', achievements=achievements)

@admin_bp.route('/achievements/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_achievement(id):
    if not current_user.is_admin:
        return redirect(url_for('main.home'))

    achievement = Achievement.query.get_or_404(id)
    if request.method == 'POST':
        achievement.name = request.form['name']
        achievement.start_date = request.form['start_date']
        achievement.end_date = request.form['end_date']
        achievement.site = request.form['site']
        achievement.objectives = request.form['objectives']
        achievement.beneficiaries_kind = request.form['beneficiaries_kind']
        achievement.beneficiaries_number = request.form['beneficiaries_number']
        achievement.results_obtained = request.form['results_obtained']
        db.session.commit()
        flash('Achievement updated successfully.', 'success')
        return redirect(url_for('admin.manage_achievements'))

    return render_template('edit_achievement.html', achievement=achievement)

@main_bp.route('/projects')
def projects():
    return redirect(url_for('admin.manage_achievements'))

@main_bp.route('/mediatheque')
def mediatheque():
    media_list = Media.query.all()
    return render_template('mediatheque.html', media_list=media_list)



@admin_bp.route('/dashboard')
@login_required
def dashboard():
    if not current_user.is_admin:
        return redirect(url_for('main.home'))
    reports = Report.query.all()
    users = User.query.all()
    events = Event.query.all()
    news_list = News.query.all()
    return render_template('dashboard.html', reports=reports, users=users, events=events, news_list=news_list)
    
#report

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

#event

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

#user

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

#news

@news_bp.route('/news', methods=['GET'])
def view_news():
    news = News.query.order_by(News.date.desc()).all()
    return render_template('news.html', news=news)

@news_bp.route('/news/add', methods=['GET', 'POST'])
@login_required
def add_news():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        image_url = request.form['image_url']
        news = News(title=title, content=content, image_url=image_url)
        db.session.add(news)
        db.session.commit()
        flash('News added successfully.', 'success')
        return redirect(url_for('news.view_news'))
    return render_template('add_news.html')

@news_bp.route('/news/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_news(id):
    news = News.query.get_or_404(id)
    if request.method == 'POST':
        news.title = request.form['title']
        news.content = request.form['content']
        news.image_url = request.form['image_url']
        db.session.commit()
        flash('News updated successfully.', 'success')
        return redirect(url_for('news.view_news'))
    return render_template('edit_news.html', news=news)

@news_bp.route('/news/delete/<int:id>', methods=['POST'])
@login_required
def delete_news(id):
    news = News.query.get_or_404(id)
    db.session.delete(news)
    db.session.commit()
    flash('News deleted successfully.', 'success')
    return redirect(url_for('news.view_news'))
@admin_bp.route('/news/<int:news_id>/update', methods=['POST'])
@login_required
def update_news(news_id):
    if not current_user.is_admin:
        return redirect(url_for('main.home'))
    news = News.query.get(news_id)
    if news:
        news.title = request.form['news_title']
        news.content = request.form['news_content']
        db.session.commit()
        flash('News updated successfully.', 'success')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/news/<int:news_id>/delete', methods=['POST'])
@login_required
def delete_news(news_id):
    if not current_user.is_admin:
        return redirect(url_for('main.home'))
    news = News.query.get(news_id)
    if news:
        db.session.delete(news)
        db.session.commit()
        flash('News deleted successfully.', 'success')
    return redirect(url_for('admin.dashboard'))
@admin_bp.route('/news/create', methods=['POST'])
@login_required
def create_news():
    if not current_user.is_admin:
        return redirect(url_for('main.home'))
    title = request.form['news_title']
    content = request.form['news_content']
    news = News(title=title, content=content)
    db.session.add(news)
    db.session.commit()
    flash('News added successfully.', 'success')
    return redirect(url_for('admin.dashboard'))







