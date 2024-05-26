from functools import wraps
from flask import Blueprint, render_template, request, session, redirect, url_for

auth = Blueprint('auth', __name__)
main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/associations')
def associations():
    return render_template('associations.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        selected_association = request.form.get('association')
        username = request.form.get('username')
        password = request.form.get('password')

        # Vérifier les informations d'identification dans votre base de données
        # Si les informations d'identification sont valides, authentifiez l'utilisateur
        # Vous pouvez également vérifier le type d'utilisateur (admin ou membre) à ce stade

        session['association'] = selected_association
        session['username'] = username
        session['logged_in'] = True

        return redirect(url_for('main.index'))  # Rediriger vers une page appropriée après la connexion

    # Renvoyer le template d'authentification avec le formulaire de sélection de l'association
    return render_template('login.html')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('auth.login'))  # Rediriger vers la page de connexion si l'utilisateur n'est pas authentifié
        return f(*args, **kwargs)
    return decorated_function

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@auth.route('/logout')
def logout():
    session.clear()  # Effacer les données de session
    return redirect(url_for('auth.login'))  # Rediriger vers la page de connexion

