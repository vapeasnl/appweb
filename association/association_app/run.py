from app import create_app, db

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crée les tables si elles n'existent pas encore
        try:
            db.engine.connect()
            print("La connexion à la base de données est active.")
        except Exception as e:
            print(f"Erreur de connexion à la base de données : {str(e)}")
        app.run(debug=True, port=8000)  # Changer le port si nécessaire

