from flask import Flask
from database import db, check_database_connection

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'

# Initialisation de la base de données
db.init_app(app)

if __name__ == '__main__':
    with app.app_context():
        if check_database_connection():
            print("La connexion à la base de données est active.")
        else:
            print("La connexion à la base de données a échoué.")

