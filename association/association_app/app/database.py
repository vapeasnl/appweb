from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def check_database_connection():
    try:
        db.session.execute('SELECT 1')
        return True
    except Exception as e:
        print(f"Erreur de connexion à la base de données : {str(e)}")
        return False

