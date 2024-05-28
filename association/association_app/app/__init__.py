from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'd2b548b5c6bffe75c7450a4e9e8d77abc0cd620cb161cb49'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:01031991@localhost/association'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)

    from .models import User
    from .views import bp as main_bp
    app.register_blueprint(main_bp)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('500.html'), 500

    return app
